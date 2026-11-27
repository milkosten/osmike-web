#!/usr/bin/env python3
"""Generate the static pages of www.osmike.com (header/footer shared). Output goes to public/."""
import json, os, html, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import icons

PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public")
ROOT = open(os.path.join(os.path.dirname(__file__), "root.css")).read()
SIGNUP = "https://account.osmike.com/register"
SIGNIN = "https://account.osmike.com/"

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E"
           "%3ClinearGradient id='g' x1='0' y1='1' x2='1' y2='0'%3E%3Cstop offset='0' stop-color='%23FF8A5B'/%3E"
           "%3Cstop offset='.5' stop-color='%23FF6FA5'/%3E%3Cstop offset='1' stop-color='%237C7CFF'/%3E"
           "%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='9' fill='%23FBFAF7'/%3E"
           "%3Ccircle cx='16' cy='16' r='8' fill='url(%23g)'/%3E%3C/svg%3E")


def head(title, desc, path):
    url = "https://www.osmike.com" + path
    t, d = html.escape(title), html.escape(desc)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{t}</title>
<meta name="description" content="{d}" />
<meta name="theme-color" content="#FBFAF7" media="(prefers-color-scheme: light)" />
<meta name="theme-color" content="#14110d" media="(prefers-color-scheme: dark)" />
<meta name="color-scheme" content="light dark" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="OsMike" />
<meta property="og:url" content="{url}" />
<meta property="og:title" content="{t}" />
<meta property="og:description" content="{d}" />
<meta property="og:image" content="https://www.osmike.com/img/hero-overlook.jpg" />
<meta property="og:image:alt" content="A woman with a warm coffee watching the dawn break over the sea from a cliff" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{t}" />
<meta name="twitter:description" content="{d}" />
<meta name="twitter:image" content="https://www.osmike.com/img/hero-overlook.jpg" />
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png" />
<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png" />
<link rel="icon" href="{FAVICON}" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  /* OsMike design tokens (reference copy; keep byte-identical). The rest is in /site.css. */
{ROOT}</style>
<link rel="stylesheet" href="/site.css" />
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="dawn" aria-hidden="true"></div>
<div class="content">
<div class="wrap">
"""


def header(active):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""
  <header class="top">
    <a class="logo" href="/" aria-label="OsMike home"><span class="mark"></span>OsMike</a>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <nav class="menu" id="menu" aria-label="Main">
      {a("/services", "Services", "services")}
      {a("/integrations", "Integrations", "integrations")}
      {a("/business", "Companies", "business")}
      {a("/developers", "Developers", "developers")}
      <a class="cta" href="{SIGNIN}">Sign in</a>
    </nav>
  </header>
"""


FOOTER = """
  <footer>
    <a class="logo" href="/"><span class="mark"></span>OsMike</a>
    <nav class="links" aria-label="Footer">
      <a href="/services">Services</a>
      <a href="/integrations">Integrations</a>
      <a href="/business">Companies</a>
      <a href="/developers">Developers</a>
      <a href="/support">Help</a>
      <a href="/privacy">Privacy</a>
      <a href="/terms">Terms</a>
    </nav>
    <div class="legal"><span>© 2026 Ryan AI AB</span><a href="mailto:info@osmike.com">info@osmike.com</a></div>
  </footer>

</div>
</div>
"""

COMMON_JS = """
<script>
  (function(){
    var b=document.querySelector('.burger'),m=document.getElementById('menu');
    if(b&&m){b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});
      document.addEventListener('keydown',function(e){if(e.key==='Escape'&&m.classList.contains('open')){m.classList.remove('open');b.setAttribute('aria-expanded','false');b.focus();}});}
    var els=[].slice.call(document.querySelectorAll('.rv'));
    if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')});return;}
    var io=new IntersectionObserver(function(en){
      en.forEach(function(x){ if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);} });
    },{threshold:.08,rootMargin:'0px 0px -6% 0px'});
    els.forEach(function(e){io.observe(e)});
  })();
</script>
"""


_ALTS = sorted(((re.escape(k[:-1]) if k.endswith("\ufe0f") else re.escape(k)) + "\ufe0f?" for k in icons.EMOJI), key=len, reverse=True)
EMOJI_RX = re.compile('(aria-hidden="true">)(' + "|".join(_ALTS) + ')(<)')
EMOJI_NAME = {k.replace("\ufe0f", ""): v for k, v in icons.EMOJI.items()}


def iconize(html_text):
    """Emoji in icon slots -> line icons (emoji are empty squares without a colour-emoji font, e.g. Chrome on Linux)."""
    return EMOJI_RX.sub(lambda m: m.group(1) + icons.use(EMOJI_NAME[m.group(2).replace("\ufe0f", "")]) + m.group(3), html_text)


def page(name, title, desc, path, active, body, extra_js=""):
    out = head(title, desc, path) + icons.sprite() + header(active) + '\n  <main id="main">\n' + iconize(body) + "\n  </main>\n" + FOOTER + COMMON_JS + extra_js + "</body>\n</html>\n"
    with open(os.path.join(PUB, name), "w") as f:
        f.write(out)


SERVICES = json.load(open(os.path.join(PUB, "services.json")))
BYID = {s["id"]: s for s in SERVICES["services"]}
GROUPS = SERVICES["groups"]


def mini(ids):
    rows = []
    for i in ids:
        s = BYID[i]
        assert s["public"], i
        rows.append(f'<li><a href="{s["url"]}"><span class="ico" aria-hidden="true">{icons.use(s["icon"])}</span>'
                    f'<span><b>{html.escape(s["name"])}</b><span class="l">{html.escape(s["line"])}</span></span></a></li>')
    return "\n          ".join(rows)


def esc(s):
    return html.escape(s)


# ---------------------------------------------------------------- Home
GLINE = {g["id"]: g for g in GROUPS}
home_groups = [
    ("work", "/img/journey-work.webp", "A person absorbed in writing at a sunlit café window seat",
     ["calendar", "documents", "meetings", "crm", "tasks"]),
    ("agents", "/img/journey-morning.webp", "A woman with a warm mug by a sunlit window in the early morning light",
     ["mesh", "rolez", "skillz", "connect"]),
    ("everyday", "/img/journey-cooking.webp", "Friends cooking together around a warm kitchen island",
     ["photos", "recipes", "shopping", "weather", "translate"]),
]
gcards = ""
for gid, img, alt, ids in home_groups:
    g = GLINE[gid]
    gcards += f"""
      <article class="group rv">
        <div class="g-media"><img src="{img}" width="1280" height="720" loading="lazy" decoding="async" alt="{esc(alt)}"></div>
        <div class="g-body">
          <h3>{esc(g["name"])}</h3>
          <p class="g-line">{esc(g["line"])}</p>
          <ul class="mini">
          {mini(ids)}
          </ul>
        </div>
      </article>"""


FACTS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "facts.json")))
INTEG = json.load(open(os.path.join(PUB, "integrations.json")))
JOBS, COMPANIES = FACTS["jobs_open"], FACTS["companies_active"]
CHIPS = "".join('<span class="chip">%s</span>' % html.escape(x["name"]) for g in INTEG["groups"] for x in g["items"] if x.get("chip"))

n_public = sum(1 for s in SERVICES["services"] if s["public"])

home = f"""
  <section class="hero">
    <p class="eyebrow rv"><span class="d"></span>OsMike · online services with AI agents</p>
    <h1 class="rv">One account. All your services. <em class="grad-text">Agents that do the&nbsp;work.</em></h1>
    <p class="sub rv">Calendar, mail, documents, photos, maps and {n_public - 5} more services under one sign-in, and
      <b>your own AI agents</b> that work across them for you.</p>
    <div class="actions rv">
      <a class="btn" href="{SIGNUP}">Create a free account</a>
      <a class="btn ghost" href="/business">OsMike for companies</a>
    </div>
    <div class="hero-media rv">
      <img src="/img/hero-overlook.webp" width="1280" height="720" fetchpriority="high" decoding="async"
        alt="A woman with a warm coffee watching the dawn break over the sea from a cliff">
    </div>
  </section>

  <section class="band" id="services">
    <div class="head-row">
      <div>
        <p class="kicker rv">Everything works together</p>
        <h2 class="title rv">Work, agents and everyday life, in one place.</h2>
      </div>
      <a class="more rv" href="/services">See all {n_public} services →</a>
    </div>
    <div class="groups">{gcards}
    </div>
  </section>

  <section class="band" style="padding-top:0" id="agents">
    <div class="one">
      <div class="one-grid">
        <div>
          <p class="kicker rv">Agents that act for you</p>
          <h2 class="rv">Say what you want done. Your agents do it.</h2>
          <p class="rv">In <b style="color:var(--on-dark)">Mesh</b> you get your own AI agents. Talk to them in Mesh or on
            Telegram. They work across your calendar, mail, files, tasks, CRM and the other services, and
            they answer you when the job is done.</p>
          <p class="rv">Ask for help with a wish and Mesh puts the right agents on it, or pick a ready team
            of five from Rolez.</p>
          <div class="pills rv">
            <span class="pill">Chat in Mesh</span><span class="pill">Telegram</span><span class="pill">Works across services</span>
          </div>
        </div>
        <div class="example rv">
          <img src="/img/journey-road.webp" width="1280" height="720" loading="lazy" decoding="async"
            alt="Two friends laughing at a mountain viewpoint on a golden-hour road trip">
          <div class="ex-body">
            <p class="bubble">“We're driving to the mountains on Saturday. Get us ready.”</p>
            <ol class="steps">
              <li><span aria-hidden="true">📅</span><span><b>Calendar:</b> checks that Saturday is free and blocks the day.</span></li>
              <li><span aria-hidden="true">🌦️</span><span><b>Weather:</b> looks up the forecast for the place.</span></li>
              <li><span aria-hidden="true">🛒</span><span><b>Shopping:</b> puts a packing and food list on your shared list.</span></li>
              <li><span aria-hidden="true">💬</span><span><b>Telegram:</b> sends you a short summary.</span></li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  </section>


  <section class="band" style="padding-top:0" id="find">
    <p class="kicker rv">Find work. Find customers.</p>
    <h2 class="title rv">The Swedish job market and every Swedish company, searchable.</h2>
    <div class="dev">
      <div class="card rv" id="jobs">
        <span class="ico" aria-hidden="true">💼</span><h3>Find a job</h3>
        <p>About {JOBS} open jobs in Sweden from Platsbanken and six other job sites, with copies of the same job
          merged. Ask your agent: it searches by words, occupation, employer or near where you are, and tells
          you when new jobs match.</p>
        <ul>
          <li>"Find nursing jobs within 30 km of Gothenburg"</li>
          <li>"Tell me when a new developer job is posted in Uppsala"</li>
        </ul>
        <a class="more" href="https://mesh.osmike.com/">Ask your agents in Mesh →</a>
      </div>
      <div class="card rv" id="leads">
        <span class="ico" aria-hidden="true">🎯</span><h3>Find customers</h3>
        <p>Search {COMPANIES} active Swedish companies by industry, size, turnover, place, age and who is hiring
          right now, then add them to your CRM as prospects or call lists. Contact details from the company
          register where they exist.</p>
        <ul>
          <li>"IT consultants in Uppsala with 10-49 employees that are hiring"</li>
          <li>Companies that said no to direct marketing are left out</li>
        </ul>
        <a class="more" href="https://leads.osmike.com/">Open Leads →</a>
      </div>
    </div>
  </section>
  <section class="band" style="padding-top:0" id="direct">
    <p class="kicker rv">Works directly</p>
    <h2 class="title rv">Sign in once. Everything is already there.</h2>
    <div class="trio">
      <div class="card rv"><span class="ico" aria-hidden="true">🔑</span><h3>One sign-in</h3>
        <p>One OsMike account opens every service. No separate accounts, no extra passwords.</p></div>
      <div class="card rv"><span class="ico" aria-hidden="true">⚡</span><h3>No setup</h3>
        <p>Nothing to install or activate. Open a service and start using it.</p></div>
      <div class="card rv"><span class="ico" aria-hidden="true">🔗</span><h3>Connected</h3>
        <p>Your services know about each other, so your agents can use them together.</p></div>
    </div>
  </section>


  <section class="band" style="padding-top:0" id="integrations">
    <div class="head-row">
      <div>
        <p class="kicker rv">Integrations</p>
        <h2 class="title rv">Connects to what you already use.</h2>
      </div>
      <a class="more rv" href="/integrations">See all integrations →</a>
    </div>
    <p class="intro rv">Connect your Google accounts and Telegram, or any other service with an API: give your agent
      the key in the chat and the integration is built for you, often within minutes. The key goes to your own
      vault; your agents never see it.</p>
    <div class="chips rv">{CHIPS}</div>
  </section>
  <section class="band" style="padding-top:0" id="trust">
    <div class="promise rv">
      <p class="kicker">Our promise</p>
      <h2 class="title">Your things are <span class="grad-text">yours</span>.</h2>
      <div class="promise-grid">
        <div><h3>No ads. Ever.</h3><p>OsMike services never show you ads. Your attention is not for sale.</p></div>
        <div><h3>Your agents see only your things</h3><p>Your agents work for <b>you</b>. They can only use your own
          data, never anyone else's.</p></div>
        <div><h3>Run by Ryan AI AB</h3><p>OsMike is run by <b>Ryan AI AB</b> in Sweden, the data controller. Questions:
          <a href="mailto:info@osmike.com" style="color:var(--accent)">info@osmike.com</a>.</p></div>
      </div>
    </div>
  </section>

  <section class="band" style="padding-top:0" id="companies">
    <div class="teaser rv">
      <div class="t-body">
        <p class="kicker">For companies</p>
        <h2 class="title">Your own OsMike, with your name on it.</h2>
        <p class="intro">Give your members or customers their own branded OsMike: your logo, colours and sign-in
          page, and ready AI agents chosen by you. We set it up for you.</p>
        <div class="actions"><a class="btn" href="/business">OsMike for companies</a></div>
      </div>
      <div class="t-media"><img src="/img/journey-dinner.webp" width="1280" height="720" loading="lazy" decoding="async"
        alt="A couple at a candlelit garden restaurant at dusk"></div>
    </div>
  </section>

  <section class="close">
    <h2 class="rv">Let your agents do the <em class="grad-text">busywork</em>.</h2>
    <p class="rv">Create a free OsMike account and every service is ready when you sign in.</p>
    <div class="actions rv">
      <a class="btn" href="{SIGNUP}">Create a free account</a>
      <a class="btn ghost" href="/services">Browse the services</a>
    </div>
  </section>
"""
page("index.html", "OsMike — one account, all your services, AI agents that do the work",
     "OsMike is one account for calendar, mail, documents, photos, maps and many more online services, with your own AI agents that work across them. No ads, ever.",
     "/", "home", home)

# ---------------------------------------------------------------- Services
chips = '<button class="chip" type="button" data-group="all" aria-pressed="true">All</button>' + "".join(
    f'<button class="chip" type="button" data-group="{g["id"]}" aria-pressed="false">{esc(g["name"])}</button>' for g in GROUPS)
services_body = f"""
  <section class="page-head">
    <p class="eyebrow rv"><span class="d"></span>Services</p>
    <h1 class="rv">Every OsMike service.</h1>
    <p class="sub rv">All of them open with one OsMike account. Your agents can use them too.</p>
  </section>

  <section aria-label="Services">
    <div class="filters" role="search">
      {chips}
      <input class="search" type="search" id="q" placeholder="Search services" aria-label="Search services" autocomplete="off">
    </div>
    <div id="list" aria-live="polite"><p class="empty">Loading services…</p></div>
    <noscript><p class="empty">This list needs JavaScript. The raw list is at <a href="/services.json">/services.json</a>.</p></noscript>
  </section>

  <section class="close">
    <h2 class="rv">One account opens them all.</h2>
    <div class="actions rv"><a class="btn" href="{SIGNUP}">Create a free account</a></div>
  </section>
"""
services_js = r"""
<script>
(function(){
  var list=document.getElementById('list'),q=document.getElementById('q'),chips=[].slice.call(document.querySelectorAll('.chip'));
  var data=null,group='all';
  function esc(s){return String(s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
  function host(u){try{return new URL(u).host}catch(e){return u}}
  function render(){
    if(!data)return;
    var term=(q.value||'').trim().toLowerCase(),out='',n=0;
    data.groups.forEach(function(g){
      if(group!=='all'&&group!==g.id)return;
      var items=data.services.filter(function(s){
        if(!s.public||s.group!==g.id)return false;
        if(!term)return true;
        return (s.name+' '+s.line+' '+s.id+' '+(s.keywords||'')).toLowerCase().indexOf(term)>=0;
      });
      if(!items.length)return;
      n+=items.length;
      out+='<section class="svc-group"><h2>'+esc(g.name)+'</h2><p class="g-line">'+esc(g.line)+'</p><div class="svc-grid">'+
        items.map(function(s){return '<a class="svc" href="'+esc(s.url)+'"><span class="ico" aria-hidden="true"><svg class="i" aria-hidden="true" focusable="false"><use href="#i-'+esc(s.icon)+'"/></svg></span><span><h3>'+esc(s.name)+'</h3><p>'+esc(s.line)+'</p><span class="host">'+esc(host(s.url))+'</span></span></a>'}).join('')+
        '</div></section>';
    });
    list.innerHTML=n?out:'<p class="empty">No service matches “'+esc(term)+'”.</p>';
  }
  chips.forEach(function(c){c.addEventListener('click',function(){group=c.getAttribute('data-group');
    chips.forEach(function(x){x.setAttribute('aria-pressed',x===c?'true':'false')});render();});});
  q.addEventListener('input',render);
  fetch('/services.json',{cache:'no-cache'}).then(function(r){if(!r.ok)throw new Error(r.status);return r.json()})
    .then(function(d){data=d;render();})
    .catch(function(){list.innerHTML='<p class="empty">The list could not be loaded. Try again, or open <a href="/services.json">/services.json</a>.</p>';});
})();
</script>
"""
page("services.html", "Services — OsMike",
     f"Every OsMike service: work, AI agents and everyday. {n_public} online services under one OsMike account.",
     "/services", "services", services_body, services_js)

# ---------------------------------------------------------------- Business
business_body = f"""
  <section class="page-head">
    <p class="eyebrow rv"><span class="d"></span>OsMike for companies</p>
    <h1 class="rv">Your own OsMike, with <em class="grad-text">your&nbsp;name</em> on it.</h1>
    <p class="sub rv">Give your members or customers a branded OsMike with ready AI agents, and every OsMike
      service underneath. We set it up for you.</p>
    <div class="actions rv">
      <a class="btn" href="#contact">Talk to us</a>
      <a class="btn ghost" href="/services">See the services</a>
    </div>
  </section>

  <section class="band" id="gets">
    <p class="kicker rv">What your company gets</p>
    <h2 class="title rv">Your brand on the outside. All of OsMike inside.</h2>
    <div class="gets">
      <div class="card rv"><span class="ico" aria-hidden="true">🎨</span><h3>Your brand</h3>
        <p>Your name, logo, colours, font and language, and your own sign-in page.</p></div>
      <div class="card rv"><span class="ico" aria-hidden="true">🤖</span><h3>Your agents</h3>
        <p>Your own catalogue of ready AI agents, made for the people you serve.</p></div>
      <div class="card rv"><span class="ico" aria-hidden="true">🎁</span><h3>A start package</h3>
        <p>New members get the agents you choose automatically, the moment they sign in.</p></div>
      <div class="card rv"><span class="ico" aria-hidden="true">🧩</span><h3>All OsMike services</h3>
        <p>Calendar, documents, mail, files, tasks, CRM and the rest work underneath, with no extra setup.</p></div>
    </div>
  </section>

  <section class="band" style="padding-top:0" id="example">
    <div class="case rv">
      <div class="c-media"><img src="/img/journey-work.webp" width="1280" height="720" loading="lazy" decoding="async"
        alt="A person absorbed in writing at a sunlit café window seat"></div>
      <div class="c-body">
        <p class="kicker">Example</p>
        <h2 class="title">A freelance payroll company in Sweden.</h2>
        <p class="intro">They gave every member their own branded OsMike, in Swedish, with four agents ready on the
          first day:</p>
        <ul class="agents-list">
          <li><span class="ico" aria-hidden="true">🧭</span>A job coach</li>
          <li><span class="ico" aria-hidden="true">🔎</span>An assignment finder</li>
          <li><span class="ico" aria-hidden="true">🧾</span>A receipt agent</li>
          <li><span class="ico" aria-hidden="true">💶</span>An invoice helper</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="band" style="padding-top:0" id="how">
    <p class="kicker rv">How it works</p>
    <h2 class="title rv">Four steps. We do the setting up.</h2>
    <ol class="how">
      <li class="rv"><h3>Talk</h3><p>Tell us who your members or customers are and what they need help with.</p></li>
      <li class="rv"><h3>We set up your brand</h3><p>We set up your name, logo, colours, language and sign-in page for you.</p></li>
      <li class="rv"><h3>Your members sign in</h3><p>They sign in on your page and find everything ready.</p></li>
      <li class="rv"><h3>You choose the agents</h3><p>Pick the agents for your catalogue and the start package.</p></li>
    </ol>
    <p class="note rv"><b>Good to know:</b> we set it up for you; there is no self-service setup yet. Each person
      has one OsMike account, so a member who already uses OsMike signs in with the same account.</p>
  </section>

  <section class="band" style="padding-top:0" id="contact">
    <div class="contact">
      <div>
        <p class="kicker rv">Contact</p>
        <h2 class="title rv">Tell us about your company.</h2>
        <p class="intro rv">We answer within a few working days. You can also write to us directly.</p>
        <p class="mail-line rv">E-mail: <a href="mailto:info@osmike.com">info@osmike.com</a></p>
      </div>
      <div id="form-box">
        <form class="lead" id="lead" novalidate>
          <div class="row2">
            <label>Name<input name="name" type="text" autocomplete="name" required maxlength="200"></label>
            <label>Company<input name="company" type="text" autocomplete="organization" required maxlength="200"></label>
          </div>
          <div class="row2">
            <label>Work e-mail<input name="email" type="email" autocomplete="email" required maxlength="254"></label>
            <label><span>Phone <span class="opt">(optional)</span></span><input name="phone" type="tel" autocomplete="tel" maxlength="50"></label>
          </div>
          <label>Number of people
            <select name="size" required>
              <option value="" selected disabled>Choose</option>
              <option>1-10</option><option>11-50</option><option>51-250</option><option>251-1000</option><option>1000+</option>
            </select>
          </label>
          <label>Message<textarea name="message" required maxlength="5000" placeholder="Who would use it, and what should the agents help with?"></textarea></label>
          <div class="hp" aria-hidden="true">
            <label>Website<input name="website" type="text" tabindex="-1" autocomplete="off"></label>
          </div>
          <p class="consent">We use your details only to answer you. Ryan AI AB.</p>
          <p class="form-err" id="form-err" role="alert" hidden></p>
          <div><button class="btn" type="submit" id="send">Send</button></div>
        </form>
      </div>
    </div>
  </section>
"""
business_js = r"""
<script>
(function(){
  var f=document.getElementById('lead'),err=document.getElementById('form-err'),btn=document.getElementById('send'),box=document.getElementById('form-box');
  function showErr(m){err.textContent=m;err.hidden=false;}
  f.addEventListener('submit',function(e){
    e.preventDefault();err.hidden=true;
    if(!f.checkValidity()){
      var bad=f.querySelector(':invalid');
      showErr('Please fill in '+(bad&&bad.name==='email'?'a valid work e-mail':'all fields except phone')+'.');
      if(bad)bad.focus();return;
    }
    var v=function(n){return (f.elements[n].value||'').trim()};
    var body={name:v('name'),company:v('company'),email:v('email'),phone:v('phone'),size:v('size'),message:v('message'),website:v('website')};
    btn.disabled=true;btn.textContent='Sending…';
    fetch('/api/contact',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
      .then(function(r){return r.json().catch(function(){return {}}).then(function(j){return {ok:r.ok,j:j}})})
      .then(function(x){
        if(x.ok){
          box.innerHTML='<div class="thanks" tabindex="-1"><h3>Thank you.</h3><p>We have your message and will answer you at the e-mail you gave us.</p></div>';
          box.firstChild.focus();return;
        }
        var d=x.j&&x.j.detail;
        if(Array.isArray(d))d=d.map(function(i){return i.msg||''}).join(' ');
        showErr(d||'Something went wrong. Please try again, or write to info@osmike.com.');
      })
      .catch(function(){showErr('Could not send. Check your connection and try again, or write to info@osmike.com.');})
      .then(function(){btn.disabled=false;btn.textContent='Send';});
  });
})();
</script>
"""
page("business.html", "OsMike for companies — your own branded OsMike",
     "White label: give your members or customers their own branded OsMike with ready AI agents and every OsMike service underneath. We set it up for you.",
     "/business", "business", business_body, business_js)

# ---------------------------------------------------------------- Developers
dev_body = """
  <section class="page-head">
    <p class="eyebrow rv"><span class="d"></span>Developers</p>
    <h1 class="rv">Use OsMike from your own code.</h1>
    <p class="sub rv">Talk to your agents from scripts, bring an agent that runs on your own computer, or give
      your agents new skills.</p>
  </section>

  <section class="band" style="padding-top:30px">
    <div class="dev">
      <div class="card rv">
        <span class="ico" aria-hidden="true">🔌</span><h3>Personal API</h3>
        <p>Mesh without the screen. Make a key in Mesh → Settings → API and send it as
          <code>Authorization: Bearer osm_…</code>. Each key does only what you tick, for the agents you choose.</p>
        <ul>
          <li>Agents, messages, files, tasks, calendar and contacts</li>
          <li>Deletes need the header <code>X-Confirm: delete</code></li>
          <li>Base address <code>https://personal-api.osmike.com</code></li>
        </ul>
        <a class="more" href="https://mesh.osmike.com/api/docs">Read the API docs →</a>
      </div>
      <div class="card rv">
        <span class="ico" aria-hidden="true">🛰️</span><h3>Bring your own agent</h3>
        <p>An agent that runs on your own computer or server can join your OsMike team. Make it in Mesh →
          Settings → Bring your own agent and give it an agent key (<code>osa_…</code>). It gets exactly
          the rights of one agent.</p>
        <ul>
          <li>WebSocket: <code>wss://personal-api.osmike.com/v1/stream</code>, messages pushed as they arrive</li>
          <li>Or webhooks: each message is POSTed to your https address, signed</li>
        </ul>
        <a class="more" href="https://mesh.osmike.com/api/docs">How it works →</a>
      </div>
      <div class="card rv">
        <span class="ico" aria-hidden="true">⌨️</span><h3>The <code>osmike</code> command line and MCP</h3>
        <p>Open source (MIT), no dependencies. Your agents from the terminal, and as an MCP server for your
          AI tools.</p>
        <pre>npm install -g osmike --registry https://git.osmike.com/api/packages/osmike/npm/
osmike send my-agent "Hi" --wait</pre>
        <ul>
          <li>Local MCP: <code>osmike mcp</code></li>
          <li>Remote MCP: <code>https://mesh.osmike.com/mcp</code> with your key</li>
        </ul>
        <a class="more" href="https://git.osmike.com/osmike/osmike-cli-js">Source code →</a>
      </div>
      <div class="card rv">
        <span class="ico" aria-hidden="true">🧠</span><h3>Skillz</h3>
        <p>A public library of skills for agents: instructions, references and scripts in one package.
          Every skill is reviewed before it is listed. Rolez bundles them into ready roles and teams.</p>
        <a class="more" href="https://skillz.osmike.com">Browse Skillz →</a>
      </div>
    </div>
  </section>
"""
page("developers.html", "Developers — OsMike",
     "Build on OsMike: the Personal API, bring your own agent over WebSocket or webhooks, the open-source osmike command line and MCP server, and Skillz.",
     "/developers", "developers", dev_body)

def int_group(g):
    if g.get("style") == "chips":
        chips = "".join('<span class="chip" title="%s">%s</span>' % (html.escape(x["line"]), html.escape(x["name"])) for x in g["items"])
        return ('\n  <section class="band" style="padding-top:30px" id="%s">\n    <p class="kicker rv">%s</p>\n    <h2 class="title rv">%s</h2>\n'
                '    <p class="intro rv">%s</p>\n    <div class="chips rv">%s</div>\n  </section>\n') % (g["id"], html.escape(g["kicker"]), html.escape(g["title"]), g["intro"], chips)
    cards = []
    for x in g["items"]:
        link = ('<a class="more" href="%s">%s →</a>' % (x["url"], html.escape(x.get("link", "Open")))) if x.get("url") else ""
        cards.append('<div class="card rv"%s><span class="ico" aria-hidden="true">%s</span><h3>%s</h3><p>%s</p>%s</div>' % (
            (' id="%s"' % x["id"]) if x.get("id") else "", icons.use(x["icon"]) if x.get("icon") else "", html.escape(x["name"]), x["line"], link))
    return ('\n  <section class="band" style="padding-top:30px" id="%s">\n    <p class="kicker rv">%s</p>\n    <h2 class="title rv">%s</h2>\n'
            '    <p class="intro rv">%s</p>\n    <div class="dev">%s</div>\n  </section>\n') % (g["id"], html.escape(g["kicker"]), html.escape(g["title"]), g["intro"], "\n".join(cards))


int_body = """
  <section class="page-head">
    <p class="eyebrow rv"><span class="d"></span>Integrations</p>
    <h1 class="rv">Your agents work with the services you already use.</h1>
    <p class="sub rv">Connect your accounts, use the data sources built into OsMike, or ask for any service with an
      API and it is built for you. You decide, per connection, whether your agents may change anything there.</p>
  </section>
""" + "".join(int_group(g) for g in INTEG["groups"]) + """
  <section class="band" style="padding-top:30px">
    <div class="card rv"><span class="ico" aria-hidden="true">🛠️</span><h3>Building on OsMike yourself?</h3>
      <p>The Personal API, bring your own agent, the <code>osmike</code> command line and MCP are on the developers page.</p>
      <a class="more" href="/developers">For developers →</a></div>
  </section>
"""
page("integrations.html", "Integrations — OsMike",
     "Connect Google and Telegram, search Swedish jobs and companies, and any service with an API: OsMike builds the integration and keeps your keys in your own vault.",
     "/integrations", "integrations", int_body)

print("ok")

# ---------------------------------------------------------------- Privacy, terms, support (Mike 2026-11-26: App Store needs them)
UPDATED = "26 November 2026"

privacy_body = """
  <section class="page-head">
    <p class="eyebrow rv"><span class="d"></span>Privacy</p>
    <h1 class="rv">Your data is yours.</h1>
    <p class="sub rv">What OsMike keeps about you, why, where it is processed, and how you get it out or delete it.</p>
  </section>
  <section class="prose">
    <p class="meta">Last updated """ + UPDATED + """. Applies to every OsMike service, the OsMike apps and Mesh.</p>

    <h2>Who is responsible</h2>
    <p>OsMike is run by <strong>Ryan AI AB</strong>, Sweden, which is the data controller for your account and the data
      you keep in OsMike. Questions, requests and complaints: <a href="mailto:info@osmike.com">info@osmike.com</a>.</p>

    <h2>What we keep</h2>
    <ul>
      <li><strong>Your account:</strong> username and OsMike e-mail address, a backup e-mail address, your password (only
        as a hash), and when you accepted the terms.</li>
      <li><strong>What you put in the services:</strong> for example your messages to agents, mail, files, documents,
        calendar, contacts, tasks and photos. You decide what goes in.</li>
      <li><strong>Your agents:</strong> their instructions, their conversations with you and the notes they keep so they
        can help you over time.</li>
      <li><strong>Voice messages</strong> in the apps: the recording is turned into text on our own computers and then
        deleted. Only the text is kept, as an ordinary message.</li>
      <li><strong>Technical logs:</strong> sign-ins, errors and usage counts, to keep the services safe and working.
        Logs are kept for a limited time.</li>
    </ul>

    <h2>What we never do</h2>
    <ul>
      <li>No ads, and no selling or renting of your data.</li>
      <li>No tracking across other companies' apps or websites.</li>
      <li>Your agents work for you only. An agent someone shares with you cannot read the owner's mail, files, calendar,
        photos or location on your behalf, and the other way round.</li>
    </ul>

    <h2>Why we process it</h2>
    <p>To give you the services you asked for (the agreement with you), to keep them secure and fix faults (our
      legitimate interest), and when the law requires it. Connections to other services, such as Google, happen only
      when you turn them on, and you can turn them off again.</p>

    <h2>Where it is processed</h2>
    <table>
      <tr><th>Who</th><th>What for</th><th>Where</th></tr>
      <tr><td>Hetzner</td><td>Our servers: the services, databases and files</td><td>Germany (EU)</td></tr>
      <tr><td>Ryan AI AB's own computers</td><td>The agents (their memory and conversations), speech to text and some AI
        models</td><td>Sweden</td></tr>
      <tr><td>OpenAI</td><td>The AI model your agents think with: the messages and data an agent works on are sent to it
        for that task</td><td>USA</td></tr>
      <tr><td>Z.ai</td><td>Some AI features, such as choosing which agent a message is for, and translations</td>
        <td>Outside the EU</td></tr>
      <tr><td>Railway</td><td>A few services that have not moved to our own servers yet</td><td>USA</td></tr>
      <tr><td>GitHub</td><td>Stores each agent's workspace in a private repository, including the agent's brief, which
        can contain your own words (what you asked for help with)</td><td>USA</td></tr>
      <tr><td>Google, Telegram, your bank (via Enable Banking)</td><td>Only if you connect them</td><td>Per that service</td></tr>
    </table>
    <p>Some of the services above are outside the EU (in the USA, and Z.ai outside the EU), so data you send to your
      agents may be processed there. We only send what the task needs.</p>

    <h2>How long we keep it</h2>
    <p>As long as you have your account. When you delete something, it is deleted. When you delete your account,
      the account and your agents are deleted at once, and your data in the other OsMike services normally within the
      hour (at the latest within 30 days). A single agent you delete is removed within 24 hours. Backups exist only to
      recover from a breakdown and are kept at most 30 days, and a restored backup never brings a deleted account
      back. We keep only what the law
      requires.</p>

    <h2>Your rights</h2>
    <ul>
      <li><strong>Get a copy</strong> of your account data (profile, linked devices, sign-ins and connected apps):
        <a href="https://account.osmike.com">account.osmike.com</a> → Privacy &amp; your data → Export. For a copy of
        anything else (messages, files, documents, mail…), write to <a href="mailto:info@osmike.com">info@osmike.com</a>.</li>
      <li><strong>Delete your account:</strong> in the OsMike app (menu → Delete account) or at account.osmike.com.</li>
      <li><strong>Correct, restrict or object:</strong> write to <a href="mailto:info@osmike.com">info@osmike.com</a>.</li>
      <li>You can complain to the Swedish Authority for Privacy Protection (IMY), <a href="https://www.imy.se">imy.se</a>.</li>
    </ul>

    <h2>Children</h2>
    <p>OsMike is not meant for children under 13.</p>

    <h2>Changes</h2>
    <p>When this policy changes, the date at the top changes.</p>
  </section>
"""
page("privacy.html", "Privacy — OsMike", "How OsMike handles your data: what we keep, why, where it is processed, and your rights.",
     "/privacy", "", privacy_body)

terms_body = """
  <section class="page-head">
    <p class="eyebrow rv"><span class="d"></span>Terms</p>
    <h1 class="rv">Terms of use</h1>
    <p class="sub rv">The agreement between you and Ryan AI AB when you use OsMike.</p>
  </section>
  <section class="prose">
    <p class="meta">Last updated """ + UPDATED + """.</p>
    <h2>The service</h2>
    <p>OsMike is a set of online services under one account, with AI agents that work for you, provided by Ryan AI AB,
      Sweden. The services are free today. We develop them continuously, so features may change, and we may pause or
      end a service; if that affects your data, we tell you first so you can export it.</p>
    <h2>Your account</h2>
    <p>Keep your password to yourself. You are responsible for what happens in your account, including what your agents
      do on your instructions. You must be at least 13 years old.</p>
    <h2>Your content</h2>
    <p>What you put in OsMike stays yours. You give us the right to store and process it only to run the services for
      you, as described in the <a href="/privacy">privacy policy</a>.</p>
    <h2>AI agents</h2>
    <p>Agents can be wrong. Check what matters before you rely on it, especially health, legal and money questions.
      Agents act only within the access you give them.</p>
    <h2>Fair use</h2>
    <p>Do not use OsMike to break the law, to harm others, to send spam, or to attack or overload the services.
      We may stop accounts that do.</p>
    <h2>Liability</h2>
    <p>The services are provided as they are. We do our best to keep them running and your data safe, but we are not
      liable for indirect losses, as far as the law allows. Your rights as a consumer under Swedish law are not limited.</p>
    <h2>Ending</h2>
    <p>You can delete your account at any time, in the app or at account.osmike.com. Swedish law applies.</p>
    <h2>Contact</h2>
    <p><a href="mailto:info@osmike.com">info@osmike.com</a></p>
  </section>
"""
page("terms.html", "Terms — OsMike", "The terms of use for OsMike.", "/terms", "", terms_body)

support_body = """
  <section class="page-head">
    <p class="eyebrow rv"><span class="d"></span>Help</p>
    <h1 class="rv">How can we help?</h1>
    <p class="sub rv">Write to <a href="mailto:info@osmike.com">info@osmike.com</a>. A person answers, usually within a working day.</p>
  </section>
  <section class="prose">
    <h2>Getting started</h2>
    <p>Create a free account at <a href="https://account.osmike.com">account.osmike.com</a>, or in the OsMike app.
      Then say what you want help with, by typing or speaking, and OsMike makes the right agents for you.</p>
    <h2>Talking to your agents</h2>
    <p>Open an agent and write, or tap the microphone, speak, and tap again to send. Your agents also work across your
      calendar, mail, files and the other OsMike services, and you can reach them on the web at
      <a href="https://mesh.osmike.com">mesh.osmike.com</a>.</p>
    <h2>Forgot your password</h2>
    <p>Write to <a href="mailto:info@osmike.com">info@osmike.com</a> from the backup e-mail address you gave when you
      signed up, and we help you get back in.</p>
    <h2>Delete your account</h2>
    <p>In the OsMike app: menu (the round logo, top right) → <strong>Delete account</strong>, then type your e-mail
      address to confirm. Or at account.osmike.com. This deletes your account and everything in it and cannot be undone.</p>
    <h2>Your data</h2>
    <p>See the <a href="/privacy">privacy policy</a>. You can export a copy of your data at account.osmike.com.</p>
  </section>
"""
page("support.html", "Help — OsMike", "Help with OsMike: getting started, agents, password, deleting your account.", "/support", "", support_body)

delete_body = """
  <section class="page-head">
    <p class="eyebrow rv"><span class="d"></span>Your account</p>
    <h1 class="rv">Delete your OsMike account</h1>
    <p class="sub rv">How to delete your account in the OsMike apps or on the web, what is deleted, and what is kept.</p>
  </section>
  <section class="prose">
    <p class="meta">Applies to the OsMike app for iPhone and Android, the other OsMike apps and every OsMike service.
      OsMike is run by Ryan AI AB, Sweden.</p>
    <h2>In the OsMike app</h2>
    <ol>
      <li>Open the OsMike app and tap the round OsMike logo at the top right.</li>
      <li>Tap <strong>Delete account…</strong></li>
      <li>Type your e-mail address to confirm and tap <strong>Delete my account</strong>.</li>
    </ol>
    <h2>Without the app</h2>
    <p>Sign in at <a href="https://account.osmike.com">account.osmike.com</a> and delete the account under
      <em>Privacy &amp; your data</em>, or write to <a href="mailto:info@osmike.com">info@osmike.com</a> from the
      backup e-mail address of your account and we delete it for you.</p>
    <h2>What is deleted</h2>
    <ul>
      <li>At once: your account (name, e-mail, phone, password) and your agents, so nothing can use them any more.</li>
      <li>Normally within the hour, and at the latest within 30 days: everything else you kept in OsMike — your agents'
        memory, chats and work, files, documents, spreadsheets, photos, mail, calendar, tasks, contacts, meetings and
        location history. Each deletion is recorded and checked afterwards, so nothing is left behind by mistake.</li>
      <li>Voice messages are never kept: they are turned into text and the recording is deleted straight away.</li>
    </ul>
    <h2>What is kept, and for how long</h2>
    <ul>
      <li>Backups exist only to recover from a breakdown and are kept at most 30 days, so your data is gone from them
        within 30 days too. If a backup is ever restored, deleted accounts are deleted again straight away, so nothing
        comes back.</li>
      <li>Technical logs (sign-ins, errors) are deleted after at most 90 days.</li>
      <li>Only what the law requires us to keep (for example bookkeeping records) is kept longer, and only for as long as
        the law requires.</li>
    </ul>
    <h2>Delete only some data</h2>
    <p>You don't have to delete the whole account: you can delete single agents (agent settings → Delete agent; it
      stops at once and is removed with its memory and chats within 24 hours) and
      files (Files screen) in the app at any time.</p>
    <p>Questions: <a href="mailto:info@osmike.com">info@osmike.com</a>. See also the <a href="/privacy">privacy policy</a>.</p>
  </section>
"""
page("delete-account.html", "Delete your account — OsMike",
     "How to delete your OsMike account in the app or on the web, what is deleted and what is kept.", "/delete-account", "", delete_body)
