# Readiness audit — autonomous page-sync automation

**Audited** 2026-08-06 against `AUTOMATION.md` at `a699e3b`, `.claude/skills/potomac-elementor/SKILL.md`,
`reference/*`, `tools/validate_spec.py`, the Orca automation `Potomac - Claude to WP`, the queued
input `Potomac Laser.zip` on `origin/project-zip`, and the live site via read-only Novamira calls.

**Current as of** `08c4e58`. Fixes from this audit landed in `16417be`, `eddf406`, `e11ae43`,
`3751dab`, `08c4e58`; live-site figures re-read 2026-08-06 11:29 UTC.

**Verdict: NOT READY — keep the schedule disabled.** Five blockers were found; **four are fixed in
the repo**. What remains is B4 (pattern budget and arity) and C6 (the inline interactive cluster) —
together they are what stands between a passing pre-flight and a useful run. Nothing has been written
to production by this pipeline: zero posts carry `_pl_auto_page`, zero `pl-auto-` attachments exist,
and `build-state.json` is still `{"processed_zips": []}`.

## Status at a glance

| # | Finding | Status |
|---|---|---|
| B1 | Backup is weekly; the §0 gate needs < 24 h | Fixed `08c4e58` — §0 now takes its own db backup |
| B2 | Page enumeration had no working exclusion rule | Fixed `16417be`; manifest committed at `manifests/potomac-laser.txt` |
| B3 | 7 of 11 pages skipped for the wrong reason; wrong post type | Fixed `eddf406`, `3751dab` |
| B4 | §7 pattern budget exhausted; arity changes fail the validator | Mitigated `de2d385` — run 1 phased to 5 service pages |
| B5 | No provenance marker, so identity was inferred from the slug | Fixed `eddf406` |
| B6 | Export ships design-time scaffolding (Tailwind CDN, React dev, Babel, tweaks panel) | Fixed `2032075` |
| B7 | The design's why-us team photo has no slot in its matched fragment | Fixed `15ff654` — image coverage is now part of the match |
| B8 | A section carries the explorer's JS template literals as if they were copy | Fixed `5aad50a` — found by dry run |
| B9 | The legends strip HTML, so legend-sourced token values ship truncated | Fixed `35e3e36` — found by write phase |
| B10 | CCIT's FAQ answers are JS-rendered, not markup — `faq-toggle` needs static pairs | **OPEN** — affects run 3 |
| B11 | Quote sections are unwired forms (CCIT **and** all 5 service pages) | **Part-fixed** `6111139` — `quote-form-hubspot` is now a library pattern, so the 4 siblings need only copy; CCIT's own form shape is still open |
| B12 | `why-choose-inset-cta` carried a hardcoded photo URL, untokenised — and PATTERNS.md called it an empty spacer | Fixed `583270f`, proven on 12239 — page now 12/12 sections |
| B13 | Elementor 4.x caches rendered HTML per post; regenerating CSS does not invalidate it | Fixed `32f4ffa` — four-step per-post invalidation now in SKILL.md §4 and AUTOMATION.md §3.c.v |
| B14 | §3.c.vi's visual verify needs an authenticated browser; an unattended run has none | **OPEN** — decision required before enabling the schedule |
| B15 | No gate tests behaviour — an inert form screenshots identically to a working one | **OPEN** — cost a real defect this session |
| C1 | §7 vs SKILL.md §8 (authoring / appending forbidden) | Fixed `16417be` |
| C2 | §7 vs TRANSLATE.md §5 ("stop and report") | Fixed `16417be` |
| C3 | TRANSLATE.md §10's blocking human review vs full autonomy | Fixed `2032075` |
| C4 | §2 delta rule excluded every status it defines | Fixed `16417be` |
| C5 | Arity guidance differs between AUTOMATION.md and TRANSLATE.md | Fixed `2032075` |
| C6 | §3.c.iv looked for the interactive asset in the wrong place | Fixed `36c65bb` — resolved from the server |
| C7 | Broken `PATTERNS.md` links and HTML entities in AUTOMATION.md | Fixed `16417be` |
| D1–D5 | Deployment gaps (branch, MCP config, agent type, localhost entry, report field) | Fixed `2032075` |

---

## Open: B4 — the pattern budget is exhausted by this zip, and arity changes fail the validator

**Budget.** §7.9 caps new patterns at 8 per zip, then fails the remaining pages with
`pattern-budget-exhausted`. All 10 library patterns are service-page shapes extracted from post 12133,
so anything that isn't a service page is mostly unmatched:

| Page(s) | Sections | Estimated new patterns |
|---|---|---|
| CNC Micromachining, Rapid Prototyping, Laser Micromachining, Micro-Hole Drilling, 3D Printing | 12 each | **2** total — a services card grid (`#services`) and a quote-form block (`#quote`); on 12133 the quote form lived inside the interactive iframe, so no fragment covers it. §7's dedupe means the first page mints and the rest reuse |
| CCIT | 9 | ~5 — leak-test science explainer, method selector, packaging showcase, validation-documentation block, related-applications strip |
| sector-medical-potomac | 6 | ~2–3 |
| About Our Group, Contact, Project Gallery, Services & Applications | 4/4/3/6 | ~4–6 between them |

That is 12–14 candidates against a cap of 8. The cap trips mid-run, and which pages die depends on
file iteration order.

**Arity.** §3.c.ii says to match "on structure, not count" wherever PATTERNS.md Notes mark a count
adjustable — and they do, e.g. the hero's "add/remove sibling containers in pairs". But
`validate_spec.py` checks token coverage **exactly, in both directions**: a 4-pair hero omits
`heading_11/12` → `ERROR fragment tokens with no spec key`; supplying extras →
`ERROR spec keys with no fragment slot`. Any count change therefore fails the gate §7.8 requires, and
a validator failure is defined as a §7 failure — discard the pattern, fail the page.

Fragment arity against what the design actually ships (measured on the CNC page):

| Pattern | Fragment count | CNC design | Verdict |
|---|---|---|---|
| `spec-table-dark` | 8 label/value rows | 8 | matches |
| `process-comparison-cards` | 3 cards | 3 | matches |
| `process-steps-numbered` | 5 steps | 5 | matches |
| `hero-dark-stat-strip` | 5 stat pairs, 2 buttons + text link | 2 buttons + 1 text link | matches |
| `faq-toggle` | repeater, count free | — | no constraint |

So the trap is **latent, not immediately fatal** for the service pages. It bites the moment a design
ships a different count.

**Fix (human, pick one):** raise or lift the cap for a first real run and accept a long report; or
curate the zip so it fits (service pages only); or make arity a first-class spec feature — declare
each repeating unit's count in `spec.yaml`, have the assembler add and remove sibling containers, and
have the validator check coverage against the *resolved* fragment rather than the file on disk. Until
one of those, counts must stay identical to the fragments.

---

## Readiness verdict — 2026-08-06, after the supervised run

**Not ready to enable the schedule.** Every pre-flight gate now passes unaided and one page was built
end to end, but the evidence from doing it says the pipeline cannot yet do it alone:

- **One section took all three §7.3 iterations.** Guessed styling, a `calc()` width, and a theme `p`
  rule beating widget typography. A fourth failure would have discarded the pattern.
- **Two defects were caught by a human noticing, not by a gate.** The quote form's action button is
  `type="button"`, so it never raised a submit event — the form was **inert and screenshotted
  perfectly** (B15). And a leaked CSS selector silently restyled an already-verified section; that
  surfaced because a regression was recognised, not because anything failed.
- **B13 was undocumented.** The costliest discovery of the run existed only in commit messages until
  `32f4ffa`. An unattended run would have burned its whole verify budget on stale markup.
- **§3.c.vi needs a logged-in browser** (B14). The draft preview 404s without a session, so an
  unattended run's only route is minting an admin session automatically — a privileged act, unsupervised.

What is genuinely proven: the §0 backup gate ran and produced a set; identity-by-provenance behaved
correctly on both the create and the update paths; the enumeration manifest resolved; the validator
caught real defects the moment fragments changed; two §7 patterns were minted, verified and merged;
and a live form submission reached HubSpot with no PII in the dataLayer.

**Recommended gate before enabling:** one more supervised run on a sibling service page (Laser
Micromachining). It reuses both new patterns and needs only copy substitution, so it is the fairest
test of the pipeline rather than of the author. **If it completes with zero human interventions, that
is the evidence to enable the schedule.** This run took roughly a dozen.

---

## Dry run — CNC Micromachining, 2026-08-06 (no writes)

Everything up to SKILL.md §0 was executed for real against `CNC Micromachining.html`; nothing was
written to WordPress. What it established:

| Step | Result |
|---|---|
| Strip scaffolding (B6) | 6 removals — Tailwind Play CDN ×1, React dev ×2, Babel ×1, tweaks panel ×1, tweaks-root ×1. Zero off-site dependencies left |
| Segment | 12 sections |
| MATCH | **9 matched, 3 `UNMATCHED`** — `#services` "Explore our precision capabilities", `#quote` "Ready to move forward?", and `#why-us` (image coverage, B7). The first two were predicted; the third the dry run found |
| Arity | Every matched section equals its fragment: 5 hero stat pairs, 8 spec rows, 3 comparison cards, 5 steps, 4 ecosystem cards, 3 testimonials, 2 CTA buttons, 8 FAQ items (free repeater) |
| Assets | 10 inline base64 images, all unique: 4 eco logos → `{image_1..4}`; 5 service photos → belong to the unmatched `#services` grid; 1 team photo → **no slot (B7)** |
| Media reuse | None available — no attachment matches these filenames, and post 12133's own 4 image widgets carry **no** attachment id (they point at `novamira-drafts/` by URL). The run must create 10 new attachments, and SKILL.md §3's id gate is stricter than the source page |
| Interactive | `cnc-interactive.html` resolves; dependency gate **PASS** (0 external script/stylesheet) |
| Identity | No `_pl_auto_page` hit for this page; `pl-auto-cnc-micromachining` is free → the run would correctly build |
| Template literals | **36 found in section [11] (B8)** |
| Token extraction | Spec generated for the 9 matched sections — 164 tokens, validator clean — then **invalidated**: values had come from the legends, which are lossy (**B9**). 57 errors under the corrected rule |

### B7 — the team photo had nowhere to go (fixed `15ff654`)

`why-choose-inset-cta` has **no image slot** — of the ten fragments only `group-ecosystem-cards`
does — but the design's `#why-us` ships a 121 KB photo (`alt="Goodfellow Microfabrication team"`).
Matched as-is the photo was silently dropped, and invisibly: no token is missing, so neither
TRANSLATE nor the validator can see it, and the loss would surface only as a §3.c.vi screenshot
difference that burns three iterations and fails the page. The fragment's Notes even call that
empty first column "a layout spacer, not a missing image" — true of post 12133, wrong here.

**Image coverage is now part of matching.** §3.c.ii and TRANSLATE.md §4 count the design section's
content images against the candidate fragment's `{image_n}` tokens; if the design has more, the
match is a MISS and the section goes to §7 as a variant. Match-and-drop is forbidden explicitly,
with the reason, so it does not get re-derived as a shortcut later.

Two supporting rules make it stick:

- **§7.1 may not dedupe it back.** "Reduced strictness" covers copy and count, never dropping
  content the fragment cannot hold — collapsing `#why-us` back into `why-choose-inset-cta` would
  silently reintroduce the defect. Sibling pages reuse the *variant*, not the image-less original.
- **§7.7 names variants as siblings** — `why-choose-inset-cta-image` — and requires its
  `Recognise when` to state the discriminator (the copy column is paired with a photo), so a future
  run chooses between the two on structure instead of guessing.

Re-running the match with the rule applied: **9 matched, 3 `UNMATCHED`**, and `group-ecosystem-cards`
correctly still matches (4 images ≤ 4 slots). Nine of ten fragments lacking an image slot is a
property of post 12133, not of page design — which is what §7 exists to correct.

### B12 — the why-us photo was hardcoded (fixed `583270f`)

Fixed across five places, since the defect had been copied into the docs:

- **Fragment** — the 52% column's `background_image` is now `{image_1}` with `id: ""`, so each page
  supplies its own photo instead of inheriting post 12133's.
- **Legend** — gains `{image_1}` with the real URL, and a note that it is a container background
  rather than an image widget.
- **PATTERNS.md** — token count 10 → 11, and the Notes now describe a photo column (`cover`,
  `min_height:440`, radius 16) instead of asserting an empty spacer.
- **SKILL.md §5** — the same wrong claim, repeated there, corrected.
- **SKILL.md §3 gate** — widened: it checked `image` **widgets** for a missing `id`, which is
  structurally unable to see a container background. It now checks both shapes.

`SPEC-FORMAT.md`'s per-pattern table and `spec.example.yaml` gained the token. The validator proved
the change end to end: immediately after tokenising it errored with *"fragment tokens with no spec
key → would ship literal {token}: ['image_1']"* against the example, and passes at 175 tokens once
the example was filled in. A library-wide rescan finds no other hardcoded asset URL.

### B11 — the target forms exist; the wiring approach is the open decision

The two forms named are real, active, and already integrated — **through the Gravity Forms HubSpot
add-on**, not a bespoke API POST:

| HubSpot form | GUID | Route |
|---|---|---|
| `[Potomac] Start a Project` | `9dba7d36-e36b-4a10-9411-9dc073dab7a0` | GF form **#2** "Start a Project" → feed #19, active |
| `[Potomac] Contact Form` | `54d0ec75-106d-43eb-a420-0ff22e448e6d` | GF form **#1** "Contact Form" → feed #18, active |
| `[Potomac] Subscribe - Newsletter` | `986597b1-ebce-4c39-98ac-ccfe1a21398d` | GF form **#5** "Subscribe" → feed #20, active — a **third** form, and the Contact design has a newsletter section |

`gravityformsaddon_gravityformshubspot_settings` holds an OAuth `auth_token` + `portal_id`, so the
add-on performs the HubSpot call after a Gravity Forms submission. The fields already on those forms:

- **#2 Start a Project** — Name\*, Email\*, Phone, Company, Project Name, "Tell Me More About Your
  Project", **3 × file upload**, CAPTCHA.
- **#1 Contact Form** — Name, Email\*, Phone\*, Company\*, Website, Messages, CAPTCHA.

Since those forms may not be edited, every new section must map onto exactly these fields. #2 already
covers what the service-page `#quote` wizard collects, file uploads included.

**Decided 2026-08-06:** the quote section submits **direct to the Forms API**, not through Gravity
Forms, targeting `[Potomac] Start a Project` (`9dba7d36-e36b-4a10-9411-9dc073dab7a0`) on portal
143181153, with a **single** file upload. The full contract — property names, the step-2 folding, the
upload endpoint, UTM/hutk handling — is in `reference/HUBSPOT-FORMS.md`. The sandbox portal the owner
named, **145800879**, is referenced nowhere on this site (12,969 files plus the whole database swept),
so nothing here currently points at it.

**Two findings that remain open:**

1. **The existing funnels do not use either form.** All five interactive files
   (`cnc-`, `lm-`, `mhd-`, `rp-`, `3dp-interactive.html`) POST directly to
   `9eb36566-4364-4467-8592-15c743bdc901` on portal 143181153 — a third, bespoke form outside the
   two named. They already carry UTM capture, `hubspotutk`, GA4 `G-MQSBBH2M4J` and the
   `/wp-json/cnc-quote/v1/upload` endpoint. Re-pointing them at `9dba7d36` would consolidate
   submissions, but those five files are embedded by **38 posts** — 12133, 12223–12226, ~25
   `elementor_library` templates, and 12239 — so it is a wide, live-content change, not a local one.
2. **Two different portals are referenced.** Forms and funnels use portal **143181153**; the HubSpot
   WordPress plugin's `leadin_portalId` is **677962**. If the on-page tracking code belongs to 677962,
   the `hubspotutk` cookie the funnels forward will not resolve against 143181153, and first-touch
   attribution is silently lost. Worth verifying independently of this pipeline.

### B10 — CCIT is not the safe §7 shakedown I recommended (OPEN)

Authoring the three CNC patterns surfaced two more things, both of which invalidate claims I made
earlier in this session.

**B11 is not CCIT-specific.** I described CNC's three unmatched sections as "all static, copy-only" —
that was read off their headings, not their contents. CNC's `#quote` holds **9 `input`, 1 `select`, 2
`textarea`, 2 file inputs and 2 buttons** across a two-step wizard, and `hsforms.com` appears nowhere
in it. It is the same unwired-form problem as CCIT's, and since all five service pages share the
section, it affects all five. §7 authors Elementor JSON; it does not create HubSpot forms, map
properties or run a test submission. Note this is a *second* quote path on the page — the explorer's
basket funnel inside `cnc-interactive.html` is already wired to form `9eb36566…`, so a page built
without this section still has a working conversion route plus the final CTA band.

So of CNC's three unmatched sections, **two are mintable** (`#why-us` variant, `#services` grid) and
`#quote` should be recorded `deferred-form` on the same principle as C6's `deferred-interactive`.

**B12 — `why-choose-inset-cta` hides a hardcoded asset.** Its 52% first column is not empty. It carries
the team photo as a container `background_image` pointing at
`novamira-drafts/whyus-team.jpg`, with `id: ""`, and **no token**. Consequences:

- PATTERNS.md's Notes for the pattern — "the empty first column is a layout spacer, not a missing
  image. Keep it." — are wrong, and SKILL.md §5 repeats the claim. Both were written from the
  tokenised fragment, where the URL is invisible among the settings.
- Because the URL is untokenised, **every page built from this fragment renders post 12133's team
  photo**. For CNC that is accidentally correct. For the other four service pages it silently
  substitutes the wrong image — a wrong-content bug, not a missing-content one.
- SKILL.md §3's image gate checks `image` **widgets** for a missing `id`. A container
  `background_image` is not an image widget, so the gate cannot see this at all.
- It also means my B7 diagnosis was right by luck: the image-coverage rule counted `{image_n}` tokens,
  found none, and flagged the MISS for the wrong reason. The rule still gives the right answer here,
  and the variant §7 mints must carry a **tokenised** background image.

A library-wide scan found this is the only instance: 1 hardcoded asset URL across the ten fragments,
and only `group-ecosystem-cards` has real `{image_n}` slots (4). Fixing the existing fragment and its
PATTERNS.md Notes is a human job — §6 bars this automation from editing either — but it should be
fixed before the four sibling service pages are built, or they will each ship CNC's team photo.

### B10 / B11 — CCIT is not the safe §7 shakedown I recommended (OPEN)

I twice recommended minting the three new patterns on CCIT rather than CNC, "since four pages clone
CNC". Both halves of that were wrong, and checking CCIT before acting is what surfaced it.

**The three patterns cannot come from CCIT.** Patterns are minted from sections, and CCIT contains
none of the three: no services card grid, no why-us-with-photo, and its `#quote` is a different shape
entirely. CCIT's own unmatched sections are its own — a spec-sheet hero, a science explainer, a method
selector, a packaging showcase, a validation-documentation block and a related-applications strip.

**And minting on CCIT would not have de-risked anything.** All five service pages share those three
sections, so whichever service page mints them the pattern is identical and is reused five times. The
blast radius is a property of the pattern, not of the page that happens to mint it. Minting elsewhere
delays the risk, it does not reduce it.

**CCIT is also harder, not safer**, in two ways that block it outright:

- **B10 — the FAQ content is JS-rendered.** CCIT's `#faq` section is 981 characters with zero
  `<details>`, zero `aria-expanded` and zero `<h3>`: the Q&A pairs are injected by a 9 KB script.
  `faq-toggle` needs static repeater pairs, so translate would have to lift them out of JavaScript —
  and CCIT carries 7 template literals of its own (B8), so its closing section has the same
  contamination CNC's had.
- **B11 — the quote section is a real form with no wiring.** `#quote` holds 7 `input`/`select`/
  `textarea` fields and a submit, and `hsforms.com` appears nowhere in the file. §7 authors Elementor
  JSON; it does not create HubSpot forms, map properties or run a test submission — that is HANDOFF
  Stage H, and it is outside SKILL.md §1's write allowlist. So CCIT cannot be completed by this
  automation as specified, regardless of pattern budget. It needs a human form-integration pass first.

Corrected recommendation: **CNC's three unmatched sections are the cheapest and lowest-risk §7 work in
this zip** — a services card grid, a quote CTA block, and an image-bearing why-us variant, all static,
all copy-only. Mint them there, review the three patterns before the four sibling pages reuse them
(they live on the build branch until a human merges, which is exactly that review point), and leave
CCIT until someone decides the form question.

### B9 — the legends are lossy, and the docs pointed at them as the source of copy (fixed `35e3e36`)

`TRANSLATE.md` §6 said "never fill a token without reading its legend entry", which is right about
a slot's **role** and wrong if taken as its **value** — as the write phase did, generating a spec
straight from legend values. Checked against the live post 12133, the legends were written with
HTML stripped, and the loss is not cosmetic:

| Token | Real widget value on 12133 | Legend entry |
|---|---|---|
| `hero-dark-stat-strip.body_1` | `<p>…microscopic scale — with <strong>tolerances held to ±10 µm</strong> and features as small as 100 µm. Goodfellow Microfabrication delivers…</p>` | `…microscopic scale — with ` |
| `process-comparison-cards.body_3` | `<ul><li>Tight tolerances and structural geometry</li><li>Threads, undercuts, or deep features</li><li>Consistent precision across parts</li></ul>` | `Tight tolerances and structural geometryThreads, undercuts, or deep featuresConsistent precision across parts` |

So a body containing inline markup is **truncated at the first inline tag**, a `<ul>` has its items
**flattened together**, and even a clean paragraph loses its `<p>` wrapper. 31 of the 174 string
tokens across the ten legends show the signature. Filling tokens from legends ships truncated prose
to the page — and, worse, into any §7 pattern minted from the result.

Fixed three ways. TRANSLATE.md §6 now states that a legend gives a slot's role and never its value,
with this evidence inline; values come from the design markup with inline elements preserved, and
where a section is unchanged from 12133 the authoritative value is that post's stored widget value.
`validate_spec.py` promotes its old "renders as HTML but contains no markup" **warning** to an
**error** — that warning had fired 57 times against the legend-sourced spec and was correct;
treating it as advisory is what let the spec look clean. The spec generated this way is kept as
`specs/pl-auto-cnc-micromachining/spec.yaml.INVALID-legend-sourced` as a worked example of the trap.

The existing legends are not repaired here: §6 forbids editing them, and regenerating them is the
human-supervised process in PATTERNS.md §Regenerating. Until they are, they are role references.

### B8 — client-side templates inside a section (fixed `5aad50a`)

Section [11] holds the closing CTA band **and** 36 of the explorer's template literals
(`${a.label}`, `${a.summary}`, `${a.chips.map(...)}`). Extracted as copy they would ship to the
page as visible `${…}` text. TRANSLATE.md §3 now requires a `${` scan after segmenting, and
`validate_spec.py` rejects any token value containing one. Verified: a spec carrying
`${a.label}` now fails; the template still passes.

---

## What a run would do today

Worth stating plainly, because the fixes changed it substantially. Pre-flight now passes on its own (§0
takes a database backup if none is fresh). With `manifests/potomac-laser.txt` resolving, all 11 pages
enumerate, and the provenance check returns "not built" for every one — correctly, since nothing has been
built yet — so all 11 proceed. The five service pages resolve their explorers from the server. Then:

**The manifest is phased, and run 1 is the five service pages** — `pl-auto-cnc-micromachining`,
`-laser-micromachining`, `-micro-hole-drilling`, `-rapid-prototyping`, `-3d-printing`, all as
`post_services` drafts, each resolving its explorer from the server. They need **3** new patterns
between them — a services card grid, a quote block, and an image-bearing why-us variant (B7): §7
dedupes, so the first page mints all three and the other four reuse them. That leaves 5 of the cap
of 8 unused.

The run will also report **18 files as unlisted-not-built**: the 12 genuine non-pages plus the 6 pages
held back for runs 2 and 3. That is the phasing working as intended, not an error.

Had all 11 run at once, the remaining 6 pages would have needed ~11–12 further patterns against a
budget of 6, tripping the cap and failing several pages on iteration order. The remaining caveat is
copy, not machinery: the reused explorers may carry stale `APPS` content (see C6).

---

## Resolved

### B6 — the export ships design-time scaffolding (fixed `2032075`)

Every service page in the zip loads four things that must never reach a live page:
`cdn.tailwindcss.com` (Tailwind's Play CDN — on WP, WindPress compiles instead), React and
ReactDOM **dev** builds from unpkg, `@babel/standalone`, and a `tweaks-panel.jsx` design widget
with its `tweaks-root` mount. Nothing in the docs said to strip it, so it would have shipped —
putting third-party dev bundles on production pages.

Three layers now stop it: TRANSLATE.md §2 strips it as an explicit clean step; SKILL.md §2 greps
the assembled JSON for those hosts and for any external `<script src>` / `rel="stylesheet"` before
the first WordPress call; and `validate_spec.py` rejects either in a token value. No fragment needs
an off-site asset, so anything external is scaffolding by definition. Verified: Tailwind CDN, React
dev, `tweaks-root` and a bare external stylesheet each fail; a clean spec and the template pass.

### C3 — blocking human review vs autonomy (fixed `2032075`)

TRANSLATE.md §10 required human sign-off before §0 while AUTOMATION.md's preamble forbids asking for
input. §10 is now split by caller: an automation run puts the match table in the run report and
continues — the report is the review, and its output is unpublished drafts either way — while a
human-run translate still stops for sign-off.

### C5 — arity guidance (fixed `2032075`)

AUTOMATION.md said counts were "typical, not required"; TRANSLATE.md said a mismatch needs a
decision. TRANSLATE.md §131–150 now states the mechanical truth: the spec must supply exactly the
fragment's count because the validator compares the token set both ways, `faq-toggle` is the sole
free repeater, and a genuine mismatch is structural — drop the surplus deliberately and report it,
or take the section through §7, which is the only path allowed to change a fragment's shape. Never
juggle tokens to absorb it.

### D1–D5 — deployment gaps (fixed `2032075`)

- **D1/D2.** The audit's suggestion — point the automation at a `main` checkout — turned out to be
  wrong: `/Users/admin/orca/potomac-laser` is on `main` but has **no `.mcp.json`** (it is gitignored
  and exists only in the coordinator's workspace), so a run there would have no Novamira access at
  all. Worse than the branch mismatch it fixed. Instead §1 now names the concept: the coordinator
  runs from its own workspace, that workspace must have `.mcp.json` and a branch not behind
  `origin/main`, and whatever it runs from is **the coordinator branch**. §2 reads and §4 commits
  `build-state.json` there, then pushes to `origin/main` so the ledger is shared, not local.
- **D3.** §6 now states it outright: translate, mocks and screenshot comparison may be delegated;
  **every** WordPress read or write is made by the coordinator itself, because MCP is auto-denied to
  subagents and build worktrees have no `.mcp.json`. A worker claiming to have called Novamira is a
  bug — verify state directly.
- **D4.** SKILL.md §0 gate 2 now tests **reachability**, not configuration: a configured-but-dead
  `novamira-localhost` entry must not block a run, while a dev server that actually answers aborts
  it. No edit to anyone's `.mcp.json` required.
- **D5.** §4's report is now a committed file, `built/run-<timestamp>.report.md`, with an itemised
  contents list — enumeration, unlisted files, exclusions with rules, manifest hash status, the §0
  recovery floor, resolved interactive assets and deferrals, minted and discarded patterns, the §8
  counterparts, and the TRANSLATE match table. The worktree comment becomes a one-line pointer at
  it, which is all a single metadata string can honestly carry.

### C6 — the interactive asset was sought in the export, but it lives on the server (fixed `36c65bb`)

§3.c.iv required the design export to contain a self-contained interactive HTML file for any page using
`interactive-iframe-embed`, and failed the page otherwise. This export contains none — the "Select your
application" explorer ships **inline**, its 4,141-byte section carrying no script or style of its own
while the behaviour sits in a 24.7 KB page-level script shared with the FAQ and the quote basket. Read
literally, all five service pages were `failed: missing-interactive-asset`.

The premise was wrong, not just the remedy. **The interactive clusters already exist on the server**,
one per service page, from the earlier human-supervised work:

| File | Bytes | Modified | Dependency gate |
|---|---|---|---|
| `cnc-interactive.html` | 106,891 | 2026-07-31 | PASS |
| `lm-interactive.html` | 107,732 | 2026-07-31 | PASS |
| `mhd-interactive.html` | 107,762 | 2026-07-31 | PASS |
| `rp-interactive.html` | 107,796 | 2026-07-30 | PASS |
| `3dp-interactive.html` | 107,479 | 2026-07-30 | PASS |

All five carry `APPS` + `MATERIALS`, the basket, the HubSpot wiring (portal 143181153, form
`9eb36566…`), and read `window.parent` for page identity, so they are page-agnostic. Zero external
script or stylesheet dependencies.

§3.c.iv is now a resolution order: (1) a server file named by the manifest's `interactive=` field —
**referenced, never modified**, since these files belong to earlier work and to the pages already using
them (SKILL.md §1); (2) a self-contained file shipped in the export, uploaded as before; (3) neither →
build the page **without** that section, record `deferred-interactive`, and strip the section from
`mock.html` so 3.c.vi does not fail verify on a section that was never going to be there. Deferral is
now the rare fallback rather than the expected path. The interactive step also moved **ahead of image
upload**, so a page that cannot resolve its asset no longer leaves orphan attachments. The frame id
derives from the resolved filename (`cnc-interactive.html` → `cnc-interactive-frame`), not the
`pl-auto-` slug, because the id is part of the file's contract with its embed bridge.

The dependency gate was also corrected: it first tested for *any* external `<link>`, which failed all
five on the `rel="canonical"` each carries — inert inside an iframe. It now tests only real
dependencies: external `<script src>` and external `rel="stylesheet"`. Re-verified: all five PASS.

**Open, for a human, not a blocker:** these files date from 2026-07-30/31 and were built for the
*previous* iteration of these pages, while this design rewrites per-page explorer content — the zip's own
`CLAUDE.md` insists the `APPS` summaries, chips and materials must be topic-specific. So the explorer
will **work** but may carry **stale copy** until someone diffs the `APPS` data in those five files
against the export. The run reports this rather than assuming it is fine. Editing them is a human's job:
the automation may not touch them.

### B1 — the backup gate could never pass (fixed by self-serving a backup)

SKILL.md §0 demanded a backup **verified less than 24 hours old**, and AUTOMATION.md §6 made that the
one failure that stops the whole run. UpdraftPlus is on a **weekly** db schedule with file backups
`none`: at audit time the newest set was 2026-08-02 04:00 UTC (103.5 h old, db/plugins/themes, no
uploads), the last set including uploads was 2026-07-09, and the next was not due until 2026-08-09. The
gate was satisfiable for a few hours a week at best and failed outright on the day. The agent could not
fix it either — §1 permitted no PHP beyond insert / meta / media / CSS and read-only queries.

Rather than remove the gate, §0 now **takes its own backup** when none is fresh:
`do_action('updraft_backupnow_backup_database')` (verified registered on this install), then poll
`updraft_backup_history` and `updraft_last_backup` until a newer set reports success — every 30s, capped
at 10 minutes. The set's timestamp and nonce go into the run manifest as the run's recovery floor, and
the report must state it. A backup that runs but fails to upload is **not** a pass; no successful set
inside the cap still aborts the whole run with `failed: no-verified-backup`.

SKILL.md §1 was widened by exactly one entry to permit this — a **database-only** backup, in §0 only.
UpdraftPlus writes its own options and schedules its own resumption events as a consequence; those are
the plugin's writes, not the skill writing `wp_options` or changing cron. Files/uploads backups,
restores, deleting old sets, and any change to UpdraftPlus settings or schedule all remain forbidden.
Only the db matters here anyway: the run's file writes are additive, and the manifest already covers
them.

**Two properties of this install the human should know** (both recorded in §0):

- `updraft_delete_local=1` with `updraft_service=['dropbox']` — the set is uploaded and the local copy
  deleted, so there are **zero local backup files on the server** (confirmed) and recovery depends on
  the Dropbox connection still being valid. A stale token becomes a failed gate rather than a silent
  pass, which is the right failure direction, but it does mean the gate can start blocking runs for a
  reason that has nothing to do with this pipeline.
- `updraft_retain_db=5` — every backup this gate takes rotates one older set out. Today's five weekly
  sets span about five weeks; if the automation adds a set per run, weekday runs would compress that
  history to about five days. **Consider raising `updraft_retain_db`** if runs become frequent.

Still worth doing independently of this pipeline: a **daily** db schedule and any uploads coverage at
all. The gate now guarantees a backup at run time; it does not improve the site's baseline.

### B5 — identity was inferred from the slug (fixed `eddf406`)

The check asked "does anything with this slug exist?" when the question is "has this pipeline already
created this page?". Slug is neither necessary nor sufficient, and nothing on the site could answer the
real question: no postmeta key matching `%novamira%` / `%pl_auto%`, and zero `pl-auto-` attachments.

It failed both ways. **False positives:** `laser-micromachining`, `3d-printing`, `micro-hole-drilling`,
`about-our-group`, `contact`, `project-gallery`, `services-applications` and `kapton` all matched live,
published, *pre-process* pages and skipped — the pipeline never built them, so they should build.
**False negative:** CNC Micromachining exists four times — 11893 `cnc-micro-machining-services`, 12127
`cnc-micromachining-services-draft`, **12133** `cnc-micromachining-services-draft-blocks` (the fragment
library's own provenance page) and 12102 `cnc-new-temp` — and the derived `cnc-micromachining` matches
none of them, so a fifth copy would be built. It would not even have reached the drift report, which
only covered pages recorded `skipped-exists`.

Now: SKILL.md §4 stamps `_pl_auto_page` (the design file's path inside the zip — the identity that
survives a human editing slug or title), `_pl_auto_zip` and `_pl_auto_run`. §3.c.i queries
`_pl_auto_page` at `post_status`/`post_type=any`: hit → `skipped-already-built`, miss → build. Drafts
are created at `pl-auto-<slug>` so live pages keep the clean slugs; `validate_spec.py --automation`
enforces that namespace; §4 re-reads `post_name` after insert to catch WP's silent `-2` suffixing. §8
became informational — per design page, list live counterparts by slug family (`<slug>`, `-services`,
`-services-draft*`, `<slug>-*`) and by title, noting which carry `_pl_auto_page`.

### B3 — post type (fixed `eddf406`, `3751dab`)

`page` was the only permitted type, which forced service and application pages into the wrong permalink
and template. Type now follows what the page *is*: `post_services` for services (`/services/<slug>/`),
`post_application` for application and sector pages, `page` for everything else. Threaded through
SKILL.md §1, `ALLOWED_POST_TYPES`, SPEC-FORMAT.md, spec.example.yaml and AUTOMATION.md §3a/§3.c.i/§4;
§4 gates the chosen type against `elementor_cpt_support` before creating. All three are present in that
option.

### B2 — enumeration (fixed `16417be`; allow-list drafted `e11ae43`)

§3a identified interactive assets by iframe reference, and the export has no iframes, so every
standalone, canvas and working copy enumerated as a page — ~8 junk builds out of ~13, including two
byte-identical CNC copies (2,548,462 b each) and a 206-byte empty canvas. Kebab slugs don't collide
(`3d-printing-standalone` ≠ `3d-printing`), so nothing downstream caught it.

Now: the allow-list is a **repo-side manifest** under `manifests/`, resolved by a `# zip:` filename
directive (authoritative) or `# zip_sha256:` (advisory — a filename match with a stale hash is used and
reported, since a re-export legitimately changes the hash). It lives in the repo rather than the zip
because a re-export replaces the zip wholesale and would discard curation stored inside it. Entries are
parsed by trailing token, since filenames contain spaces. A manifest path missing from the zip fails the
zip; every zip HTML file the manifest omits is reported as *unlisted, not built* with its section count,
so a re-export that adds pages cannot be silently dropped. With no manifest: root-only `*.html`, minus
`*.dc.html`, `* (standalone).html`, structural duplicates, zero-`<section>` files and every
subdirectory, and the report says loudly that no manifest was found.

`manifests/potomac-laser.txt` carries this zip's curation — 11 pages of 23 HTML files (5
`post_services`, 4 `page`, 2 `post_application`), the 12 exclusions with their reasons, and a commented
phasing note for B4. **No action needed inside the zip.**

### C1, C2, C4, C7 — doc defects (fixed `16417be`)

- **C1/C2.** §7 requires authoring Elementor JSON and appending fragments, legends and `PATTERNS.md`
  entries, which SKILL.md §8 and TRANSLATE.md §5 both forbade outright. SKILL.md §8 now carries a
  daggered carve-out naming §7 as the sole exception and restating its gates; TRANSLATE.md §5 has the
  matching exception and still stops-and-reports for a human run.
- **C4.** "Delta = zips whose hash is not present with status 'built', 'partial', or 'failed'" excluded
  every recorded zip, making the partial-retry path and §5's retry rule unreachable. Now: absent from
  `processed_zips`, or present with status `partial`.
- **C7.** Two `reference/[PATTERNS.md](http://PATTERNS.md)` links pointed at a nonexistent URL, and
  `&lt;slug&gt;`-style entities appeared throughout §3 — 16 lines of paste artefacts that an agent reads
  literally.

---

## Verification baseline

Everything below was checked and holds at `08c4e58`.

| Check | Result |
|---|---|
| Referenced docs exist | `PATTERNS.md` (10 entries + Entry template + Regenerating), `SPEC-FORMAT.md`, `TRANSLATE.md`, `spec.example.yaml`, `manifests/potomac-laser.txt` ✅ |
| Fragment library | 10 `.json` + 10 sibling `.legend.json` ✅ |
| Skill sections cited by AUTOMATION.md | §0 gates, §1 scope, §2 assemble, §3 image, §4 write all exist and say what is claimed ✅ |
| Skill is version-controlled | `.claude/skills/potomac-elementor/SKILL.md` tracked → present in new worktrees ✅ |
| Validator | Python 3.9.6 + PyYAML 6.0.3. `spec.example.yaml --template` → 10 sections, 174 tokens, 0 errors ✅ |
| Validator, post types | `post_services` and `post_application` pass; `post_landing` rejected, naming the three allowed ✅ |
| Validator, slug namespace | bare slug rejected under `--automation`, accepted for a hand run ✅ |
| Validator resolves new patterns | `SNIPPETS` derives from the script's own location, so §7 fragments in a build worktree validate ✅ |
| Manifest | `manifests/potomac-laser.txt` binds to `Potomac Laser.zip` / sha `2f5215b4…`; all 11 entries parse by the documented rule and resolve inside the zip; the 12 unlisted files are exactly the documented exclusions ✅ |
| Elementor build path | v3 legacy still correct: `container` ACTIVE, `e_atomic_elements` off, `e_opt_in_v4` off, `e_classes` off (Elementor **4.2.1** / Pro **4.1.3** — the version string moved, the semantics didn't) ✅ |
| Kit + provenance | active kit 11259; posts 12133 (10 sections) and 12223–12226 (9 each) present, matching PATTERNS.md ✅ |
| `elementor_cpt_support` | `page`, `post_services`, `post_application` ✅ |
| Orca primitives | `orca worktree create --name … --base-branch …`, `worktree set --comment` ✅ |
| Artifacts committable | `.gitignore` covers neither `specs/`, `built/`, nor `reference/snippets/` ✅ |
| Backup trigger | `updraft_backupnow_backup_database` registered; WP-cron enabled; backup dir writable. `delete_local=1`, service `dropbox`, `retain_db=5`, 0 local sets on disk — see B1 ✅ |
| Production untouched | 0 posts with `_pl_auto_page`, 0 `pl-auto-` attachments, `processed_zips: []` ✅ |

---

## Before the first run

1. ~~**B4** — phase run 1 to the five service pages.~~ **Done** — the manifest's run-2 and run-3
   blocks are commented out with instructions for advancing a phase. Note that re-entering an already
   processed zip needs its `build-state.json` entry deleted by a human (§5) unless its status is still
   `partial`. Decide separately whether arity becomes a spec feature.
2. **Explorer copy** — optionally diff the `APPS` data in the five server-side interactive files
   against this design before running, or accept run 1 with the report flagging it (C6).
3. **Optional hygiene** — raise `updraft_retain_db` above 5 if runs will be frequent, and put
   UpdraftPlus on a daily db+files schedule; §0 guarantees a backup at run time but does not improve
   the site's baseline (B1).
4. **Dry-run one page** with the schedule still disabled — **CNC Micromachining**, done: its no-write
   phase is clean and its spec validates. Not CCIT: B10/B11 show it needs a human form pass first.
5. **Then enable the schedule** — and only then. Everything above is reversible; a scheduled
   autonomous run against production is the first thing that isn't.
