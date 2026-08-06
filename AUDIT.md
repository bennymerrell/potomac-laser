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
| B2 | Page enumeration had no working exclusion rule | Fixed `16417be`; allow-list drafted, **not yet in the zip** |
| B3 | 7 of 11 pages skipped for the wrong reason; wrong post type | Fixed `eddf406`, `3751dab` |
| B4 | §7 pattern budget exhausted; arity changes fail the validator | **OPEN** — human decision |
| B5 | No provenance marker, so identity was inferred from the slug | Fixed `eddf406` |
| C1 | §7 vs SKILL.md §8 (authoring / appending forbidden) | Fixed `16417be` |
| C2 | §7 vs TRANSLATE.md §5 ("stop and report") | Fixed `16417be` |
| C3 | TRANSLATE.md §10's blocking human review vs full autonomy | **OPEN** — follows from scope |
| C4 | §2 delta rule excluded every status it defines | Fixed `16417be` |
| C5 | Arity guidance differs between AUTOMATION.md and TRANSLATE.md | **OPEN** — same decision as B4 |
| C6 | §3.c.iv unsatisfiable: the interactive cluster ships inline | **OPEN** — blocks all 5 service pages |
| C7 | Broken `PATTERNS.md` links and HTML entities in AUTOMATION.md | Fixed `16417be` |
| D1–D5 | Deployment gaps (branch, MCP config, agent type, localhost entry, report field) | **OPEN** |

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

## Open: C6 — §3.c.iv is unsatisfiable for this export, and it blocks all five service pages

§3.c.iv requires the export to contain a self-contained interactive HTML file for any page using
`interactive-iframe-embed`. Here the "Select your application" explorer ships **inline** in each
service page — the `APPS` JS object that the zip's own `CLAUDE.md` flags as easy to miss — and **the
export contains zero `<iframe>` elements at all**. Read literally, every service page is
`failed: missing-interactive-asset`.

Worse, §3.c.iv uploads images *before* checking for the interactive file, so a run would push ~10
`pl-auto-` attachments per page to the live media library and then abandon the page. They land in the
manifest, but nothing deletes them.

Two further wrinkles in the same step: the design's images are base64 `data:` URIs embedded in the
HTML (10 per service page), and extracting them to files before upload is a step the spec never
describes; and `assets/` also holds file copies of some of them, so a rule is needed for which source
wins.

**Fix (human decision, then a spec change):** either extract the explorer into
`<slug-prefix>-interactive.html` during translate — which is authoring, and needs the same treatment
§7 got — or declare inline-interactive an accepted input and define how it is handled (most likely:
lift the markup into an `html` widget, accepting that WindPress does not compile inside an iframe and
so the file must carry its own CSS either way). Also move the interactive check *before* image upload,
so a doomed page costs nothing.

## Open: C3 and C5 — two doc conflicts that follow from the decisions above

- **C3.** TRANSLATE.md §10 requires human review of the match table before §0; AUTOMATION.md's
  preamble says "Complete ALL steps without asking for input." If the automation keeps full autonomy,
  §10 should become "emit the match table into the run report" rather than a gate. Left deliberately
  until scope is settled.
- **C5.** AUTOMATION.md §3.c.ii ("counts are typical, not required") and TRANSLATE.md §131–150 ("a
  mismatch needs a decision"; only `faq-toggle` is free) still disagree. Whichever way B4's arity
  question goes, both docs should end up saying the same thing.

## Open: D1–D5 — deployment gaps

1. **Branch mismatch.** The automation's workspace is `…/workspaces/potomac-laser/main-2`, on branch
   `main-2`, while AUTOMATION.md §1 says "the coordinator runs from main" and §2/§4 read and commit
   `build-state.json` "on main". `main-2` and `origin/main` are currently identical (`08c4e58`), but
   local `main` is stale at `a994e53`, so a run would read and write the ledger on `main-2`. Either
   point the automation at a `main` checkout, or reword §1/§2/§4 to name the coordinator branch.
2. **`.mcp.json` is gitignored and exists only in `main-2`.** Per-zip worktrees created by §3b get no
   Novamira config, so an agent session started *inside* a build worktree cannot reach WordPress. All
   MCP calls must stay in the coordinator's own session — true today, but AUTOMATION.md never says so,
   though SKILL.md's Context does ("Subagents cannot use these tools").
3. **Agent type is `claude-agent-teams`.** With (2), delegating page builds to team workers means
   every Novamira call is auto-denied. If teams are intended, AUTOMATION.md needs an explicit rule:
   translate and verify may be delegated, all MCP writes happen in the lead.
4. **`novamira-localhost` is still configured** in `.mcp.json` (currently ECONNREFUSED). SKILL.md §0
   gate 2 says confirm "localhost/dev servers are not connected" — configured-but-unreachable is
   ambiguous, and a strict reading aborts the run. Remove the entry before enabling, or reword the
   gate as "no localhost server reachable".
5. **§4's "worktree comment"** maps to `orca worktree set --comment <text>`, a single metadata string.
   The §4 report (per-page status, preview URLs, enumeration, exclusions, new patterns, discards,
   drift) is long for that field; commit `built/run-<ts>.report.md` and put a pointer in the comment.

The schedule is **disabled** (weekdays 09:00 Europe/London, 720-minute missed-run grace), which is the
correct state today.

---

## What a run would do today

Worth stating plainly, because the fixes changed it. Pre-flight now passes on its own — §0 takes a
database backup if none is fresh. With `pages.txt` in the zip, all 11 pages enumerate; the provenance check returns "not built" for every one (correctly — nothing has been built
yet), so all 11 proceed. Then:

- The **5 service pages** fail at §3.c.iv on the inline explorer (C6), after uploading their images.
- The **6 remaining pages** are mostly `UNMATCHED` against a service-page library, so §7 mints until
  the cap of 8 trips (B4) and the rest fail `pattern-budget-exhausted`.

Net expected output: **0–2 built pages, ~50 orphan attachments, and a long report.** C6 and B4 are now
the only things between a passing pre-flight and a useful run.

---

## Resolved

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

Now: an optional `pages.txt` in the zip root is the complete allow-list, parsed by trailing token
(filenames contain spaces, so the post type is read as the last token); a listed path missing from the
zip fails the zip. Without it: root-only `*.html`, minus `*.dc.html`, `* (standalone).html`, structural
duplicates, zero-`<section>` files and every subdirectory. Exclusions must be reported with the rule
that caused them.

**Remaining action:** `reference/pages.example.txt` holds the drafted allow-list for this zip — 11 pages
of 23 HTML files (5 `post_services`, 4 `page`, 2 `post_application`), with all 12 exclusions and their
reasons. **It still has to be copied into the zip root as `pages.txt`.** Until then the fallback
heuristics run, and they are a safety net rather than curation.

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
| Referenced docs exist | `PATTERNS.md` (10 entries + Entry template + Regenerating), `SPEC-FORMAT.md`, `TRANSLATE.md`, `spec.example.yaml`, `pages.example.txt` ✅ |
| Fragment library | 10 `.json` + 10 sibling `.legend.json` ✅ |
| Skill sections cited by AUTOMATION.md | §0 gates, §1 scope, §2 assemble, §3 image, §4 write all exist and say what is claimed ✅ |
| Skill is version-controlled | `.claude/skills/potomac-elementor/SKILL.md` tracked → present in new worktrees ✅ |
| Validator | Python 3.9.6 + PyYAML 6.0.3. `spec.example.yaml --template` → 10 sections, 174 tokens, 0 errors ✅ |
| Validator, post types | `post_services` and `post_application` pass; `post_landing` rejected, naming the three allowed ✅ |
| Validator, slug namespace | bare slug rejected under `--automation`, accepted for a hand run ✅ |
| Validator resolves new patterns | `SNIPPETS` derives from the script's own location, so §7 fragments in a build worktree validate ✅ |
| Allow-list | all 11 entries parse by the documented rule and resolve inside the zip; the 12 unlisted files are exactly the documented exclusions ✅ |
| Elementor build path | v3 legacy still correct: `container` ACTIVE, `e_atomic_elements` off, `e_opt_in_v4` off, `e_classes` off (Elementor **4.2.1** / Pro **4.1.3** — the version string moved, the semantics didn't) ✅ |
| Kit + provenance | active kit 11259; posts 12133 (10 sections) and 12223–12226 (9 each) present, matching PATTERNS.md ✅ |
| `elementor_cpt_support` | `page`, `post_services`, `post_application` ✅ |
| Orca primitives | `orca worktree create --name … --base-branch …`, `worktree set --comment` ✅ |
| Artifacts committable | `.gitignore` covers neither `specs/`, `built/`, nor `reference/snippets/` ✅ |
| Backup trigger | `updraft_backupnow_backup_database` registered; WP-cron enabled; backup dir writable. `delete_local=1`, service `dropbox`, `retain_db=5`, 0 local sets on disk — see B1 ✅ |
| Production untouched | 0 posts with `_pl_auto_page`, 0 `pl-auto-` attachments, `processed_zips: []` ✅ |

---

## Before the first run

1. **C6** — decide how the inline interactive explorer is handled, and move the check ahead of image
   upload so a failing page costs no orphan attachments.
2. **B4** — raise the pattern cap for the first run or curate the zip to fit; decide whether arity
   becomes a spec feature. Then align C5's wording across both docs.
3. **B2 residue** — copy `reference/pages.example.txt` into the zip root as `pages.txt`.
4. **D1–D4** — point the automation at a `main` checkout, state the MCP-in-lead-session rule, remove the
   `novamira-localhost` entry.
5. **C3** — resolve TRANSLATE.md §10 once scope is settled.
6. **Dry-run one page** with the schedule still disabled. CCIT is the best candidate: no interactive
   cluster, no live counterpart at its slug, and it exercises §7 minting end to end.
