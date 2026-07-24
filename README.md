# osmike-web

The public marketing site for **MikeOS** — the AI-first phone and computer for a freer, smoother life.

- **Live:** https://www.osmike.com (+ apex https://osmike.com)
- **Story:** MikeOS is a complete new end-user experience — a consumer alternative to Apple/Google
  phones + OS + computers, where AI isn't an app, it's the whole experience. Sells **freedom + AI +
  a life that just flows** — deliberately non-technical (the platform/backend is a quiet "Platform"
  footer link for the ~3% who want it).
- **Stack:** FastAPI serving `public/` (static). Nixpacks-only, `$PORT` from env, no DB, no secrets.
- **Deploy:** Railway (workspace SaaSRyan), auto-deploys from `main`. DNS: Cloudflare — see
  `mikeos-architecture/docs/domain-management.md`.

```
public/index.html        the site (self-contained HTML/CSS + Google Fonts)
server/http_server.py     tiny FastAPI static server + /api/health
```

Design: warm, luminous, editorial — a "new dawn" sunrise gradient, Fraunces display + Manrope body,
big emotional headlines, generous space. Edit `public/index.html` and push to redeploy.
