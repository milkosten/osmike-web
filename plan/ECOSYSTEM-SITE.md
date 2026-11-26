# www.osmike.com: from phones and laptops to the OsMike ecosystem + white label (plan, 2026-11-26, waiting for Mike's go)

Mike: "it is focused on phones and laptops (remove that), change it to be more about the ecosystem of services that we
are offering. And the possibility to white label for companies."

## 1. What the site is today
- One static page + a "Platform" page (repo `osmike-web`, FastAPI static), hosted on **Railway** (auto-deploy from `main`),
  the only OsMike site still there. Last change 4 Nov.
- Brand **"MikeOS"** (every service says **"OsMike"**: OsMike CRM, OsMike Documents …).
- Content: "the AI-first phone and computer". Hero "Order now", 2 phones (€799 / €1,099) and 2 computers (€1,299 / €1,599),
  "MikeCloud" storage prices (€2.99–14.99 / month), a no-ads promise, a lifestyle photo gallery. **We sell none of this**:
  the order buttons lead nowhere, and we have no paid services.
- Nothing about what actually runs: ~45 live services under one account, AI agents (Mesh), the personal API, and a
  proven white-label copy (frilans.osmike.com for Frilans Finans).
- It is also the **design reference**: its `:root` colour/font tokens are copied by mail, chat and the starter kit. Those
  tokens must stay.

## 2. What we can honestly show (checked live 26 Nov: all answer 200)
**Work:** CRM · Contracts · Sign (e-signatures) · Leads (Swedish companies) · Documents · Spreadsheets · Presentations ·
Calendar · Meetings (video, transcripts + summaries) · Mail · Files · Tasks.
**AI agents:** Mesh (your own agents that act across every service, by chat or Telegram) · Skillz · Rolez (ready roles
for 20 work teams) · Connect (Google etc.) · Personal API / bring your own agent · Decision Deck.
**Everyday:** Photos · Maps · Weather · News · Search · Translate · Voice · Music · Stories · Shopping · Recipes · Products ·
Local · Guide · Trips · Budget · Body · DNA · Devices · Mind · Stocks.
Common facts worth saying: one sign-in for everything; services work directly (no activation); agents work across the
services for their own person only; no ads; data on our own servers (Hetzner + our own machines; a few services still on Railway; the exact
"EU only" claim is verified before it goes on the page); data controller
Ryan AI AB; contact info@osmike.com.

## 3. New site
Name **OsMike** everywhere. Same warm design and tokens; real screenshots of the services instead of phone photos
(light + dark, taken with the existing screens script). English (+ Swedish, decision D).

1. **Home** `/`
   - Hero: "One account. All your services. AI agents that do the work." Buttons: **Create a free account**
     (account.osmike.com sign-up) · **OsMike for companies**.
   - "Everything works together": 3 groups (Work, AI agents, Everyday) with 4–6 service cards each, link to /services.
   - "Agents that act for you": Mesh, one example across services (a meeting → notes → CRM follow-up → calendar).
   - "Works directly": no setup, no activation, one sign-in.
   - Trust: no ads ever, your data is yours (export/delete), EU servers, who runs it (Ryan AI AB).
   - Companies teaser → /business.
2. **Services** `/services`: every public service as a card (icon, one line, link), grouped and filterable.
3. **For companies** `/business` (white label)
   - What a company gets: **its own branded OsMike** for its members or customers: name, logo, colours, font, language,
     its own sign-in page, its own catalogue of ready agents and a start package; all services underneath.
   - Example: a freelance payroll company gives every member a job coach, assignment finder, receipt and invoice agents
     (frilans.osmike.com; named only with their OK, decision C).
   - How it works: 1 talk → 2 we set up your brand (days, not months) → 3 your members sign in → 4 you choose the agents.
   - What is shared and what is yours (honest: one OsMike account per person across brands, see §5).
   - Contact: a short form that lands as a **lead in Mike's CRM** + bell (OsMike sends no e-mail), plus info@osmike.com.
4. **Developers** `/developers` (replaces "Platform"): personal API, bring your own agent, MCP, the `osmike` CLI, Skillz.
5. Footer: Services · Companies · Developers · Privacy · Terms · Ryan AI AB · info@osmike.com.

**Removed:** phones, laptops, all prices, "Order now", MikeCloud storage tiers, "MikeOS Certified", the phone/laptop
journeys gallery, the device copy on the Platform page. `/order`-style anchors redirect to `/`.

## 4. How it is built and shipped
- Same repo, rewritten pages; keep `:root` tokens byte-identical (other sites copy them). Static HTML stays (no login on
  the public site), except the contact form endpoint.
- Service list in one `services.json` (name, group, one line, url, icon, public yes/no), so the app switcher, /services
  and later the brand catalogue can share it.
- Screens 390 / 1280 px, light + dark, looked at; links checked (all 200); Lighthouse-style check of size/speed.
- Hosting (decision E): move from Railway to 242 like the rest (container `osmike-web`, Caddy block for osmike.com +
  www, Cloudflare A records), then pause the Railway service.
- The design agent (mikeos-design-pattern) reviews before it goes live.

## 5. What white label needs so the page doesn't over-promise (product, after the site)
Today only **Mesh** can be branded, through a separate git branch + container per brand, on a `*.osmike.com` name.
1. **Brand as configuration** on Mesh `main` (one image, brand folder + config), not a branch per customer.
2. **Brand the core services** a company's members see: Documents, Spreadsheets, Calendar, Meetings, CRM (logo, colours,
   name, app switcher) through the shared design tokens.
3. **The company's own domain** (e.g. `ai.company.se` by CNAME), with automatic certificates.
4. **Company admin**: members, which agents and services are on, usage.
5. Optional later: company-owned accounts (own tenant) for companies that need it; billing when paid plans exist.
The /business page describes 1–3 as "how it works" only once they exist; until then it says "we set it up for you".

## 6. Decisions for Mike
- **A. Name:** OsMike everywhere (MikeOS goes)?
- **B. Which services are public:** all ~40, or a curated set (hide early or sensitive ones: DNA, Body, Budget, Stocks,
  Devices, Mind) with "and more" — recommend curated.
- **C. Frilans Finans** as a named example (needs their OK) or anonymous?
- **D. Languages:** English only, or English + Swedish?
- **E. Hosting:** move osmike.com from Railway to 242?
- **F. Contact for companies:** form → lead in your CRM + bell (recommended), or just info@osmike.com?
- **G. Audience order:** companies first (white label is the business), or people first with a companies section?
