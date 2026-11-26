# osmike-web — www.osmike.com

The public site for **OsMike**: one account for ~40 online services, with your own AI agents that work
across them (people first), and **OsMike for companies** (white label). Plan: `plan/ECOSYSTEM-SITE.md`.

- **Stack:** FastAPI serving `public/` (static). `$PORT` from env, no DB, no secrets.
- **Deploy:** Railway auto-deploys from `main` (moving to relay 242). Don't push before hosting moves.

```
public/index.html         Home (people first; companies teaser)
public/services.html      /services: every public service, grouped + filter; reads services.json
public/services.json      the service list (id, name, group, icon, line, url, keywords, public)
public/business.html      /business: white label + contact form (POST /api/contact, JSON)
public/developers.html    /developers: Personal API, bring your own agent, osmike CLI + MCP, Skillz
public/site.css           shared styles; starts with the OsMike design tokens
public/img/               lifestyle photography (WebP) + og/favicon assets
server/http_server.py     static server, clean routes, /platform -> /developers, /api/health
```

Rules: the `:root` token block (top of `site.css` and inline in every page) is copied by other OsMike
sites: keep it byte-identical; add new tokens in the second `:root` block. Name is **OsMike** everywhere.
No hardware, prices or orders. No external scripts except Google Fonts. Each page must work at 390 px.
To add or hide a service, edit `services.json` (`public: false` hides it).
