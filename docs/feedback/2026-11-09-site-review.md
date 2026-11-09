# CATech Website — Dev Feedback & Action Items
**Review Date:** 9 November 2026  
**Reviewer:** Kiro (AI Design & Code Review)  
**Status:** Open

---

## Priority 1 — Critical

### 1. Hero interactive console — replace or simplify
**Location:** `index.html` — Hero section, right column (`lg:col-span-6`)  
**Problem:** The terminal widget (tabs: "Local-First Sync", "AI Agent Trace", "Native Engine") contains heavy engineering jargon — "CRDT Delta Sync Rail", "Context RAG", "Vector similarity scan (cos: 0.94)", "Async Tokio engine", "Memory RSS", "Epoll / Kqueue non-blocking I/O". This is the most visible element on the page and contradicts all the plain-language work done across the rest of the site. A non-technical founder or SME owner will not understand it and will disengage immediately.  
**Fix options (pick one):**
- Replace with a simple animated "project journey" visual — e.g. 3 steps: Brief → Build → Launch
- Replace with a rotating client outcome card (real stats from SPSLNT, The 1494, SpendWise)
- Replace with a compact "what we've built" visual — logos/names of live projects with status badges
- If keeping the console concept, rewrite all tab labels and content in plain English (no metrics, no latency numbers, no system internals)

---

### 2. Hero headline — soften for non-technical audience
**Location:** `index.html` — `<h1>` in hero section  
**Current:** `Your Product, Shipped. Senior Engineering for High-Growth Teams`  
**Problem:** "Senior Engineering" and "High-Growth Teams" are positioning terms aimed at people who already know the vocabulary. A regular business owner doesn't identify as a "high-growth team".  
**Suggested alternatives:**
- `We Build the Tech. You Run the Business.`
- `From Idea to Live Product — Without the Headaches`
- `Reliable Software, Built Fast, By People Who Give a Damn`

---

## Priority 2 — Important

### 3. "Work Email" label on contact form
**Location:** `index.html` — Contact section, email field label  
**Current:** `Work Email`  
**Problem:** Implies you only want to hear from corporate contacts. Startups and SMEs (your primary audience) often reach out from personal emails. Creates unnecessary friction.  
**Fix:** Change to `Email address`

### 4. Service card tech tags — mismatched with service description
**Location:** `index.html` — Services section  
**Problem:**
- Card 2 (Websites, Web Apps & Mobile Apps) shows `WebAssembly` and `Rust` — these are low-level tools invisible and irrelevant to someone shopping for a website or app
- Card 1 (Cloud Infrastructure) shows `Kafka` — meaningless to a non-technical buyer
**Fix:** Replace with outcome-oriented or recognisable tags:
- Card 1: swap `Kafka` → `Auto-scaling` or just remove it
- Card 2: swap `WebAssembly` and `Rust` → `iOS` / `Android` or remove; keep `React`, `Next.js`, `Swift`

### 5. "FinTech & Data Engine" badge in Outcomes section
**Location:** `index.html` — Client Outcomes section, SpendWise card  
**Problem:** Jargon badge that crept back in after the plain-language pass on the Products section.  
**Fix:** Change to `Finance App` or `Personal Finance` to match the Products section treatment.

---

## Priority 3 — Polish

### 6. Hero CTA secondary button
**Location:** `index.html` — Hero section  
**Current:** `See What We Do`  
**Suggestion:** Consider `View Our Work` to direct attention to the portfolio/outcomes sections which are the strongest trust-building content on the page.

### 7. "Direct Contact Number" label in Contact section
**Location:** `index.html` — Contact section, left column  
**Current:** `Direct Contact Number`  
**Fix:** Just `Phone` — the word "Direct" is filler.

### 8. AI Agent Trace panel has `bg-indigo-600` button
**Location:** `index.html` — Hero console, Panel 2 ("AI Agent Trace"), Run Trace button  
**Problem:** `bg-indigo-600` and `shadow-indigo-600/30` — the old brand colour crept back in on this one button. Should be `bg-teal-600` and `shadow-teal-600/30` to stay consistent with the new palette.

---

## Won't Fix / Acknowledged

- **Gmail address in JSON-LD structured data** — intentionally left as `consultanythingtech@gmail.com` for now. Update to `hello@catech.dev` when the custom domain email is live.
- **Screenshot images** — confirmed present in `assets/images/screenshots/`. No action needed.
- **GitHub org** — kept as `consultanything-tech` intentionally (existing repos). No migration needed.

---

## Notes for Dev
- The site is a single static HTML file: `index.html`
- Styles: `assets/css/styles.css`
- JS: `assets/js/main.js`
- All Tailwind classes are applied inline via CDN — no build step required
- Test locally with `python3 -m http.server 8080` from the project root
