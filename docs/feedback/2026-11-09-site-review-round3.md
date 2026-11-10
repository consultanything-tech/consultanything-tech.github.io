# CATech Website — Dev Feedback Round 3
**Review Date:** 9 November 2026  
**Reviewer:** Kiro (AI Design & Code Review)  
**Precondition:** All Round 1 (8 items) and Round 2 (9 items) verified ✅ closed.  
**Status:** Open

---

## Summary

The site is in strong shape after two rounds. All major branding, language, colour, structural, and accessibility issues are resolved. What remains is minor polish — a few phrases and tech tags that still lean technical.

**Verified clean:**
- ✅ Zero indigo brand colour remnants
- ✅ Zero slate background remnants (all zinc)
- ✅ All internal anchor links match section IDs (no broken jumps)
- ✅ All `<img>` tags have alt text
- ✅ Both `role="tablist"` elements have `aria-label`
- ✅ Both tab panels have `aria-labelledby`
- ✅ Contact form has all Web3Forms hidden fields (access_key, subject, from_name, redirect, botcheck)
- ✅ Web3Forms JS handler intact in main.js
- ✅ Form labels use plain language ("Email address", not "Work Email")
- ✅ Team profiles use role-based icons, no placeholder initials
- ✅ Team bios written in plain outcome-focused language
- ✅ Hero console replaced with real client project showcases
- ✅ Hero headline reads "We Build the Tech. You Run the Business."
- ✅ Console label reads "Live Client Projects"
- ✅ Micro-CTA reads "Want to build something like this? Let's talk"

---

## Priority 1 — Conversion-critical path

### 1. Engagement process step 3 — "daily commits" is git jargon
**Location:** `index.html` — Contact section, engagement process, step 3  
**Current:** `Direct private communication channel, daily commits, and test-verified code shipped from day one.`  
**Problem:** "Daily commits" means nothing to a non-technical founder. They don't know what a commit is.  
**Fix:** `Direct private communication channel, daily progress updates, and tested code delivered from day one.`

---

## Priority 2 — Nice to have

### 2. Engagement process step 1 — "Architecture Discovery" slightly technical
**Location:** `index.html` — Contact section, engagement process, step 1  
**Current:** `30-Min Architecture Discovery`  
**Problem:** "Architecture" is a software engineering term. The subtext explains it well enough, but the heading itself could be clearer.  
**Fix:** `30-Min Project Discovery` or `30-Min Discovery Call`

### 3. Capabilities/Tech section — 3 jargon tech tags
**Location:** `index.html` — Technologies section, "AI & Security" card  
**Current tags:** `LLM Orchestration`, `Zero-Trust Architecture`, `eBPF Monitoring`  
**Problem:** These are deeply technical terms that even tech-adjacent buyers won't recognise. The Technologies section is inherently more technical (it's a tool list), but these three are opaque.  
**Suggested replacements:**
- `LLM Orchestration` → `AI Model Pipelines` or `AI Integration`
- `Zero-Trust Architecture` → `Network Security`
- `eBPF Monitoring` → `System Monitoring`

---

## Priority 3 — Cosmetic

### 4. HTML comment references old console name
**Location:** `index.html` line 181  
**Current:** `<!-- Right Column: Interactive Local-First & Systems Architecture Console -->`  
**Problem:** Invisible to users, but references the old jargon-heavy console that was replaced.  
**Fix:** `<!-- Right Column: Live Client Projects Console -->` or just delete the comment.

### 5. HTML comment references old section name
**Location:** `index.html` line 1556  
**Current:** `<!-- Senior Engineering Leadership & Accountability -->`  
**Problem:** Invisible to users. The visible heading is now "Who Builds Your Software" which is good. The comment is stale.  
**Fix:** Update comment to match, or delete it.

---

## Won't Fix / Acknowledged (carried forward)
- **Gmail address in contact section and JSON-LD** — intentional, update when custom domain email is live
- **Screenshot images** — confirmed present, no action needed
- **GitHub org** — kept as `consultanything-tech` intentionally
- **Cyan as secondary accent** — intentional design choice for card category differentiation, not the old indigo brand colour
