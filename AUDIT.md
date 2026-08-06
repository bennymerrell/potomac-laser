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
| B7 | The design's why-us team photo has no slot in its matched fragment | **OPEN** — decision, found by dry run |
| B8 | A section carries the explorer's JS template literals as if they were copy | Fixed `5aad50a` — found by dry run |
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

## Dry run — CNC Micromachining, 2026-08-06 (no writes)

Everything up to SKILL.md §0 was executed for real against `CNC Micromachining.html`; nothing was
written to WordPress. What it established:

| Step | Result |
|---|---|
| Strip scaffolding (B6) | 6 removals — Tailwind Play CDN ×1, React dev ×2, Babel ×1, tweaks panel ×1, tweaks-root ×1. Zero off-site dependencies left |
| Segment | 12 sections |
| MATCH | **10 matched, 2 `UNMATCHED`** — `#services` "Explore our precision capabilities" and `#quote` "Ready to move forward?", exactly as predicted |
| Arity | Every matched section equals its fragment: 5 hero stat pairs, 8 spec rows, 3 comparison cards, 5 steps, 4 ecosystem cards, 3 testimonials, 2 CTA buttons, 8 FAQ items (free repeater) |
| Assets | 10 inline base64 images, all unique: 4 eco logos → `{image_1..4}`; 5 service photos → belong to the unmatched `#services` grid; 1 team photo → **no slot (B7)** |
| Media reuse | None available — no attachment matches these filenames, and post 12133's own 4 image widgets carry **no** attachment id (they point at `novamira-drafts/` by URL). The run must create 10 new attachments, and SKILL.md §3's id gate is stricter than the source page |
| Interactive | `cnc-interactive.html` resolves; dependency gate **PASS** (0 external script/stylesheet) |
| Identity | No `_pl_auto_page` hit for this page; `pl-auto-cnc-micromachining` is free → the run would correctly build |
| Template literals | **36 found in section [11] (B8)** |

### B7 — the team photo has nowhere to go (OPEN, needs a decision)

`why-choose-inset-cta` has **no image slot** — of the ten fragments only `group-ecosystem-cards`
does. But the design's `#why-us` ships a 121 KB photo (`alt="Goodfellow Microfabrication team"`).
Matched as-is, the photo is silently dropped: the validator cannot catch it (there is no token to
be missing), so the first sign would be §3.c.vi's screenshot comparison failing, burning its 3
iterations and marking the page `failed: verify`. The fragment's Notes even say the empty first
column is "a layout spacer, not a missing image" — true of the source page, wrong for this design.

Three ways out, all a human's call: accept the difference and give §3.c.vi a known-difference
allowance for it; treat `#why-us` as `UNMATCHED` so §7 mints an image-bearing variant (a third new
pattern, still inside the cap); or confirm the photo isn't wanted on the built page.

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
`post_services` drafts, each resolving its explorer from the server. They need **2** new patterns
between them (a services card grid and a quote block): §7 dedupes, so the first page mints and the
other four reuse — comfortably inside the cap of 8.

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
4. **Dry-run one page** with the schedule still disabled. CCIT is the best single-page candidate — no
   interactive cluster, no live counterpart at its slug, and it exercises §7 minting end to end. Or
   dry-run CNC Micromachining to exercise the interactive-asset resolution instead.
5. **Then enable the schedule** — and only then. Everything above is reversible; a scheduled
   autonomous run against production is the first thing that isn't.
