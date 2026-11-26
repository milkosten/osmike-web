"""osmike-web — the public site www.osmike.com (OsMike: online services + AI agents, white label for companies).

A tiny FastAPI app that serves the static `public/` site. No database, no secrets.
Nixpacks-only; the port comes from $PORT (never hardcoded).
"""
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="osmike-web", docs_url=None, redoc_url=None, openapi_url=None)

PUBLIC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public"))

# Clean page routes -> static HTML files in public/.
PAGES = {"services": "services.html", "business": "business.html", "developers": "developers.html"}


@app.get("/api/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "service": "osmike-web"})


def _page(filename: str):
    async def handler() -> FileResponse:
        return FileResponse(os.path.join(PUBLIC, filename), media_type="text/html")
    return handler


def _to(target: str):
    async def handler() -> RedirectResponse:
        return RedirectResponse(target, 301)
    return handler


for _route, _file in PAGES.items():
    app.add_api_route(f"/{_route}", _page(_file), methods=["GET", "HEAD"], include_in_schema=False)
    app.add_api_route(f"/{_route}/", _to(f"/{_route}"), methods=["GET", "HEAD"], include_in_schema=False)


# Old addresses from the device-era site.
@app.get("/platform", include_in_schema=False)
@app.get("/platform.html", include_in_schema=False)
async def platform() -> RedirectResponse:
    return RedirectResponse("/developers", 301)


@app.get("/order", include_in_schema=False)
async def order() -> RedirectResponse:
    return RedirectResponse("/", 301)


# Serve the static site at the root; index.html is the default document.
# POST /api/contact: the "OsMike for companies" form -> a lead in Mike's CRM (server/contact.py). Before the static mount.
from server.contact import router as contact_router  # noqa: E402
app.include_router(contact_router)

app.mount("/", StaticFiles(directory=PUBLIC, html=True), name="static")
