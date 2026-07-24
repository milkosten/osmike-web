"""osmike-web — the public landing page for OSMike.

A tiny FastAPI app that serves the static `public/` site. No database, no secrets.
Nixpacks-only; the port comes from $PORT (never hardcoded).
"""
import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="osmike-web", docs_url=None, redoc_url=None)

PUBLIC = os.path.join(os.path.dirname(__file__), "..", "public")


@app.get("/api/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "service": "osmike-web"})


# Serve the static site at the root; index.html is the default document.
app.mount("/", StaticFiles(directory=PUBLIC, html=True), name="static")
