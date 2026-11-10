# CATech Website — Dev Feedback Round 2
**Review Date:** 9 November 2026  
**Reviewer:** Kiro (AI Design & Code Review)  
**Precondition:** All Round 1 items verified ✅ closed.  
**Status:** Open

---

## Priority 1 — Audience Mismatch (still technical language in new sections)

### 1. Team profile cards — engineering jargon for non-tech buyers
**Location:** `index.html` — Team / About section, profile cards  
**Problem:** The team bios and tech tags are written for a technical peer audience, not the startup founders and SME owners who are the primary buyers:
- "12+ years designing distributed backends, zero-downtime database migrations, and edge replication topologies"
- "high-throughput network programming, Kubernetes cluster hardening, and low-latency APIs"
- "Obsessed with sub-second interaction speed, WCAG accessibility, and client-side reactive state machines"
- Tags: `Distributed Systems`, `Rust / Tokio`, `CRDT Sync`

A business owner reading this doesn't know what it means and doesn't need to. What they need to know is: *can these people solve my problem?*

**Fix:** Rewrite bios around outcomes, not tools. Example:  
*Before:* "Specialises in high-throughput network programming, Kubernetes cluster hardening, and low-latency APIs"  
*After:* "Builds the backend systems that keep your product running fast under heavy traffic — and fixes them when they don't"

Tags like `CRDT Sync` and `Rust / Tokio` are fine in a tech portfolio but jarring in a buyer-facing about section. Keep the tool names but drop the internal jargon combinations.

---

### 2. SpendWise hero console panel — "zero cloud egress" and "0ms Local Write"
**Location:** `index.html` — Hero console, SpendWise panel  
**Problem:** 
- `"0ms Local Write"` as a headline metric — meaningless to a non-technical user
- `"zero cloud egress on private financial transactions"` — cloud egress is a billing concept, not a user benefit
- `"Local-First"` badge — no non-tech user understands what local-first architecture means

**Fix:**
- `0ms Local Write` → `Instant Response`  
- `zero cloud egress on private financial transactions` → `your financial data never leaves your device`
- `Local-First` badge → `Privacy First` or `Your data stays on your device`

---

### 3. SpendWise Outcomes card — "Local-First" label
**Location:** `index.html` — Client Outcomes section, SpendWise card  
**Current:** `spendwise.experthub.store • Local-First`  
**Fix:** `spendwise.experthub.store • Privacy First`

---

## Priority 2 — Trust & Credibility

### 4. Team profile placeholder initials with no names
**Location:** `index.html` — Team section, profile cards  
**Problem:** Profiles use placeholder initials (`SA`, `LP`) with generic role titles ("Lead Product & Mobile Engineer"). No actual names are shown. This weakens the trust argument — the whole point of the section is "you work directly with real senior people." Anonymous placeholders undercut that completely.  
**Fix options:**
- Add real first names (even first name only is enough)
- If anonymity is required, remove the initials avatars and use the role title + expertise summary only — no fake person indicators
- Or remove the team section until real names can be shown

---

### 5. "Direct Commit Access" footer on team cards
**Location:** `index.html` — Team profile cards, bottom row  
**Current:** `Direct Commit Access`  
**Problem:** "Commit access" is a git term. Buyers don't know what it means and it sounds like an internal access control note, not a trust signal.  
**Fix:** `Works directly on your project` or just remove the row — it's not adding value for a non-tech audience.

---

### 6. Outcomes section has "FinTech & Data Engine" badge on SpendWise card
**Location:** `index.html` — Client Outcomes section, SpendWise card, category badge  
**Current:** `FinTech & Data Engine`  
**Problem:** This was flagged in Round 1 for the Products section and fixed there, but the same jargon reappears in the Outcomes section which was added after Round 1.  
**Fix:** `Finance App` or `Personal Finance`

---

## Priority 3 — Polish

### 7. "Active Senior Lead" status label on team cards
**Location:** `index.html` — Team section, profile card bottom row  
**Current:** `Active Senior Lead`  
**Problem:** Reads like an internal HR status tag, not something meaningful to a client.  
**Fix:** Remove, or replace with something client-relevant like `Available for projects`

### 8. Hero console right-column label "Interactive System Monitor"
**Location:** `index.html` — Hero section, above the console widget  
**Current:** `Interactive System Monitor`  
**Problem:** Even though the console content is now client projects (good), the label above it still says "Interactive System Monitor" — sounds like a DevOps dashboard, not a portfolio.  
**Fix:** `Live Client Projects` or `What We've Built`

### 9. Hero console micro-CTA copy
**Location:** `index.html` — Below the hero console widget  
**Current:** `Want this engineering rigor in your product? Talk to our engineers →`  
**Problem:** "Engineering rigor" is jargon that slipped back in. Also "Talk to our engineers" is slightly cold.  
**Fix:** `Want to build something like this? Let's talk →`

---

## Won't Fix / Acknowledged (carried from Round 1)
- **Gmail address in JSON-LD** — intentional, update when custom domain email is live
- **Screenshot images** — confirmed present, no action needed
- **GitHub org** — kept as `consultanything-tech` intentionally
