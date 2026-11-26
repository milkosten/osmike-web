"""POST /api/contact — the "OsMike for companies" form on /business (Mike 2026-11-26).

Every enquiry is first appended to /data/contact/submissions.jsonl (RAID6 on 242), then turned into a lead in Mike's
CRM by his agent `mike-osmike-web`: a company (status lead, tags website,white-label), the person, a note with the
message, and a follow-up due today, which is what the CRM bell shows. OsMike sends no e-mail.
If the CRM is unreachable the enquiry stays pending and is retried on the next submission and at start-up.

Env: OSMIKE_WEB_A2A_KEY (the agent's bus key), A2A_API, ACCOUNT_URL, CRM_URL, CONTACT_DIR.
"""
import datetime as dt
import json
import os
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections import defaultdict, deque

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()
KEY = os.environ.get("OSMIKE_WEB_A2A_KEY", "")
ACCOUNT = os.environ.get("ACCOUNT_URL", "https://account.osmike.com").rstrip("/")
CRM = os.environ.get("CRM_URL", "https://crm.osmike.com").rstrip("/")
DIR = os.environ.get("CONTACT_DIR", "/data/contact")
SIZES = ("1-10", "11-50", "51-250", "251-1000", "1000+")
EMAIL = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,190}\.[^@\s]{2,}$")
PER_IP_HOUR, PER_DAY = 5, 200
_ip = defaultdict(deque)
_day = deque()
_lock = threading.Lock()


def _clean(v, n):
    return re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", str(v or "")).strip()[:n]


def _limited(ip):
    now = time.time()
    with _lock:
        q = _ip[ip]
        while q and now - q[0] > 3600:
            q.popleft()
        while _day and now - _day[0] > 86400:
            _day.popleft()
        if len(q) >= PER_IP_HOUR or len(_day) >= PER_DAY:
            return True
        q.append(now)
        _day.append(now)
        return False


def _append(path, row):
    os.makedirs(DIR, mode=0o700, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(fd, "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _http(method, url, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    h = dict(headers or {}, **({"Content-Type": "application/json"} if data is not None else {}))
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    return json.loads(raw) if raw else {}


def _token():
    req = urllib.request.Request(ACCOUNT + "/oauth/agent-token", b"", {"X-A2A-KEY": KEY}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["access_token"]


def to_crm(e):
    """One enquiry -> lead in Mike's CRM. Returns the customer link."""
    h = {"Authorization": "Bearer " + _token()}
    found = _http("GET", CRM + "/api/agent/customers?" + urllib.parse.urlencode({"q": e["company"]}), headers=h).get("customers") or []
    same = [c for c in found if (c.get("name") or "").strip().lower() == e["company"].lower()]
    if same:
        cust = same[0]
    else:
        cust = _http("POST", CRM + "/api/agent/customers", {
            "name": e["company"], "status": "lead", "email": e["email"], "phone": e["phone"], "tags": "website,white-label",
            "notes": "Enquiry from the OsMike for companies form on www.osmike.com."}, h)
    cid = cust["id"]
    _http("POST", CRM + "/api/agent/customers/%s/people" % cid,
          {"name": e["name"], "email": e["email"], "phone": e["phone"], "role": "Contact (website form)"}, h)
    _http("POST", CRM + "/api/agent/customers/%s/note" % cid, {"kind": "note", "text": "Website enquiry (%s people) from %s <%s>%s:\n\n%s" % (
        e["size"] or "size not given", e["name"], e["email"], (", " + e["phone"]) if e["phone"] else "", e["message"] or "(no message)")}, h)
    _http("POST", CRM + "/api/agent/customers/%s/followup" % cid,
          {"title": "Answer the website enquiry from %s (%s)" % (e["name"], e["company"]), "due": dt.date.today().isoformat()}, h)
    return cust.get("link") or (CRM + "/c/" + cid)


def _pending():
    """Enquiries whose CRM step has not succeeded yet (latest status per id)."""
    path = os.path.join(DIR, "submissions.jsonl")
    if not os.path.exists(path):
        return []
    rows, state = {}, {}
    with open(path) as f:
        for line in f:
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("type") == "enquiry":
                rows[r["id"]] = r
            elif r.get("type") == "crm":
                state[r["id"]] = r.get("ok")
    return [r for i, r in rows.items() if not state.get(i)]


_push_lock = threading.Lock()


def push_pending():
    if not KEY or not _push_lock.acquire(blocking=False):
        return
    try:
        for e in _pending():
            try:
                link = to_crm(e)
                _append(os.path.join(DIR, "submissions.jsonl"), {"type": "crm", "id": e["id"], "ok": True, "link": link, "at": time.time()})
            except Exception as x:  # network/CRM down: stays pending, retried later
                _append(os.path.join(DIR, "submissions.jsonl"), {"type": "crm", "id": e["id"], "ok": False,
                                                                  "error": "%s" % getattr(x, "code", type(x).__name__), "at": time.time()})
    finally:
        _push_lock.release()


@router.on_event("startup")
def _retry_on_start():
    threading.Thread(target=push_pending, daemon=True).start()


@router.post("/api/contact")
async def contact(request: Request):
    raw = await request.body()
    if len(raw) > 20000:
        raise HTTPException(413, "That message is too long.")
    try:
        b = json.loads(raw or b"{}")
        assert isinstance(b, dict)
    except Exception:
        raise HTTPException(400, "Could not read the form. Please try again.")
    if _clean(b.get("website"), 200):        # honeypot: bots fill it, people never see it
        return {"ok": True}
    e = {"name": _clean(b.get("name"), 120), "company": _clean(b.get("company"), 160), "email": _clean(b.get("email"), 200).lower(),
         "phone": _clean(b.get("phone"), 40), "size": _clean(b.get("size"), 12), "message": _clean(b.get("message"), 4000)}
    if not e["name"]:
        raise HTTPException(422, "Please tell us your name.")
    if not e["company"]:
        raise HTTPException(422, "Please tell us your company.")
    if not EMAIL.match(e["email"]):
        raise HTTPException(422, "Please check your e-mail address.")
    if e["size"] and e["size"] not in SIZES:
        e["size"] = ""
    ip = (request.headers.get("x-forwarded-for") or (request.client.host if request.client else "") or "?").split(",")[0].strip()
    if _limited(ip):
        raise HTTPException(429, "Thank you, we already have your message. Please try again later or write to info@osmike.com.")
    e.update(type="enquiry", id=uuid.uuid4().hex, at=time.time())
    try:
        _append(os.path.join(DIR, "submissions.jsonl"), e)
    except OSError:
        raise HTTPException(503, "We could not save your message. Please write to info@osmike.com.")
    threading.Thread(target=push_pending, daemon=True).start()
    return {"ok": True}
