# osmike-web

The public landing page for **OSMike** — the self-hosted planet OpenStreetMap stack
(Overpass · Nominatim · OSRM · vector tiles) that powers MikeMaps & MikeGuide.

- **Live:** https://www.osmike.com
- **Stack:** FastAPI serving `public/` (static). Nixpacks-only, `$PORT` from env, no DB, no secrets.
- **Deploy:** Railway (workspace SaaSRyan). DNS: Cloudflare (see `mikeos-architecture/docs/domain-management.md`).

```
public/index.html        the site (self-contained HTML/CSS)
server/http_server.py     tiny FastAPI static server + /api/health
```

The OSM APIs themselves live on the Hetzner box (`osm.` / `tiles.osmike.com`) — see
`mikeos-architecture/docs/services/osm.md`. This repo is just the marketing front page.
