# Readiness audit — autonomous page-sync automation

Audited 2026-08-06 against `AUTOMATION.md` (a699e3b), `.claude/skills/potomac-elementor/SKILL.md`,
`reference/*`, `tools/validate_spec.py`, the Orca automation `Potomac - Claude to WP`, the queued
input `Potomac Laser.zip` on `origin/project-zip`, and the live site via read-only Novamira calls.

**Verdict: NOT READY — do not enable the schedule.** Four blockers. One (B1) stops the run at its
first gate; the other three mean that if the gate were passed, the run would build the wrong pages
and stall partway.

---

## What passed

| Check | Result |
|---|---|
| Referenced docs all exist | `PATTERNS.md` (10 entries + Entry template + Regenerating), `SPEC-FORMAT.md`, `TRANSLATE.md`, `spec.example.yaml` ✅ |
| Fragment library complete | 10 `.json` + 10 sibling `.legend.json` ✅ |
| Skill sections cited by AUTOMATION.md | SKILL §0 gates, §1 scope, §2 assemble, §3 image, §4 write all exist and say what AUTOMATION.md claims ✅ |
| Skill is version-controlled | `.claude/skills/potomac-elementor/SKILL.md` is tracked → present in new worktrees ✅ |
| Validator runs | Python 3.9.6 + PyYAML 6.0.3; `validate_spec.py reference/spec.example.yaml --template` → 174 tokens, 0 errors, "gates passed" ✅ |
| Validator resolves new patterns | `SNIPPETS` is derived from the script's own location, so §7 fragments written into the build worktree validate correctly ✅ |
| Elementor build path | v3 legacy containers still correct: `container` ACTIVE, `e_atomic_elements` off, `e_opt_in_v4` off, `e_classes` off (installed Elementor **4.2.1** / Pro **4.1.3** — version string moved, semantics didn't) ✅ |
| Kit + provenance intact | active kit = 11259; posts 12133 (10 sections) and 12223–12226 (9 each) all present, matching PATTERNS.md ✅ |
| `elementor_cpt_support` | `page`, `post_services`, `post_application` ✅ |
| Orca primitives exist | `orca worktree create --name … --base-branch …` and `worktree set --comment` (§3b, §4) ✅ |
| Artifacts are committable | `.gitignore` does not cover `specs/`, `built/`, or `reference/snippets/` ✅ |
| Backup plugin present | UpdraftPlus active — a verification path exists (see B1 for the schedule) ✅ |

---

## Blockers

### B1 — The §0 backup gate cannot pass. The run aborts before its first write.

SKILL.md §0 requires a backup **verified less than 24 hours old**, and AUTOMATION.md §6 makes this
the one failure that stops the whole run.

UpdraftPlus on production, read live:

| Latest sets (UTC) | Age at audit | Contents |
|---|---|---|
| 2026-08-02 04:00 | **91.9 h** | db, plugins, themes |
| 2026-07-26 04:00 | 259.9 h | db, plugins, themes |
| 2026-07-09 14:33 | 657.3 h | db, plugins, themes, **uploads** |

- `updraft_interval` = **weekly**; next run 2026-08-09. File backups: `none`.
- So the gate is satisfiable for at most a few hours a week, and today it fails outright — a
  weekday-09:00 schedule would abort ~every run with "failed: no-verified-backup".
- Uploads have not been backed up since 2026-07-09, and the run creates media attachments.
- The agent cannot fix this itself: SKILL.md §1 permits no PHP beyond insert/meta/media/CSS and
  read-only queries, so triggering a backup is out of scope by design.

**Fix (human, pick one):** set UpdraftPlus to daily (db **and** files) so the gate can pass; or
implement the "backup-status file the human updates" that SKILL.md §0 offers as the alternative —
it is named there but nothing in the repo defines its path, format, or who writes it.

### B2 — Page enumeration has no working exclusion rule for this zip. ~8 of ~13 built pages would be junk or duplicates.

§3a excludes interactive app files by "being referenced from an iframe in a page document".
**The export contains zero `<iframe>` elements** (grep across all 23 HTML files). The rule cannot
fire, so every standalone/partial/canvas file is enumerated as a page:

| File | Sections | What it actually is |
|---|---|---|
| `CNC Micromachining.html`, `Laser Micromachining.html`, `Micro-Hole Drilling.html`, `Rapid Prototyping.html`, `3D Printing.html` | 12 each | the real service pages |
| `3D Printing (standalone).html` | 12 | duplicate of the above |
| `uploads/CNC Micromachining (standalone).html`, `uploads/cnc-standalone-upload.html` | 12 | duplicates — **byte-identical to each other** (2,548,462 b) |
| `uploads/cnc-unpacked.html` | 12 | working copy |
| `uploads/Project Gallery (standalone).html` | 3 | duplicate |
| `design_handoff_about_page/About Our Group -no hero-.html` | 3 | variant |
| `Site Footer.dc.html` | 0 | a footer partial |
| `Canvas-4.dc.html` | 0 | **empty** `<x-dc>` canvas, 206 bytes |
| `Blog Index.dc.html`, `Blog Article.dc.html`, `Kapton.dc.html` | 5/2/2 | design canvases, not pages |
| `_src/original.html` | 0 | source artefact |
| `uploads/sector-medical-potomac.html` | 6 | sector page |

Kebab-cased slugs don't collide (`3d-printing-standalone` ≠ `3d-printing`), so the §3.c.i
skip-if-exists check gives no protection against the duplicates.

**Fix — APPLIED 2026-08-06.** §3a now enumerates from an optional `pages.txt` allow-list in the zip
root, falling back to root-only `*.html` with explicit exclusions (`*.dc.html`,
`* (standalone).html`, structural duplicates, zero-`<section>` files, everything outside the root),
and the report must list every exclusion with the rule that caused it. The iframe test is
explicitly retired. **Still open:** the fallback heuristics are a safety net, not a substitute for a
curated `pages.txt` — this zip should get one before any real run.

### B3 — The zip's real intent is redesigning pages that already exist, which the automation is forbidden to do. 7 of 11 real pages resolve to `skipped-exists`.

Slug checks run live against production:

| Design page | Derived slug | Live WP | Outcome |
|---|---|---|---|
| Laser Micromachining | `laser-micromachining` | 1421 `post_services` publish | skipped |
| Micro-Hole Drilling | `micro-hole-drilling` | 2692 `post_services` publish | skipped |
| 3D Printing | `3d-printing` | 4958 `post_services` publish | skipped |
| About Our Group | `about-our-group` | 12178 `page` publish | skipped |
| Contact | `contact` | 15 `page` publish | skipped |
| Project Gallery | `project-gallery` | 12183 `page` publish | skipped |
| Services & Applications | `services-applications` | 9970 `page` publish | skipped |
| Kapton | `kapton` | 4690 `post_application` draft | skipped |
| CNC Micromachining | `cnc-micromachining` | — | build |
| Rapid Prototyping | `rapid-prototyping` | — | build |
| CCIT | `ccit` | — | build |

So the run's output is 3 real new pages, ~8 junk pages (B2), and a drift report covering the 8
pages the design was actually redrawing. That is a coherent safety posture but the wrong
deliverable — worth deciding before enabling, not after.

Two secondary defects surface here:

- **Post-type mismatch.** The five service pages belong to `post_services` (that's what their live
  equivalents are, and it's in `elementor_cpt_support`), but SKILL.md §1 permits creating
  `post_type=page` only, and `validate_spec.py:85` hard-errors on anything else. The pipeline
  structurally cannot produce a service page.
- **§3.c.i doesn't say whether the existence check is scoped by post type.** Slug-only gives the
  table above; scoped-to-`page` instead makes the three `post_services` hits *build*, and WordPress
  silently suffixes the colliding slug (`laser-micromachining-2`), producing orphan near-duplicates
  of live pages. Both readings are defensible from the current text.

### B4 — §7's pattern budget is exhausted by this zip, and arity adjustment fails the validator.

**Budget.** §7.9 caps new patterns at 8 per zip, then fails all remaining pages with
"pattern-budget-exhausted". Sectioning the pages that would actually build:

- CNC/Rapid Prototyping (12 sections): 10 map to the library; **2 are new** — `#services`
  "Explore our precision capabilities" and `#quote` "Ready to move forward?" (on post 12133 the
  quote form lived inside the interactive iframe, so no fragment covers it).
- CCIT (9 sections): ~5 new — leak-test science explainer, method selector, packaging showcase,
  validation-documentation block, related-applications strip.
- `sector-medical-potomac` (6): ~2–3 new.
- Blog Index / Blog Article canvases: ~3–4 new.

That is 12–14 candidates against a cap of 8 — the cap trips mid-run, and which pages die depends on
file iteration order.

**Arity.** §3.c.ii says to match "on structure, not count" where PATTERNS.md Notes mark a count
adjustable (they do, e.g. hero stat pairs). But `validate_spec.py` checks token coverage **exactly,
both directions** (`:140-145`): a 4-pair hero omits `heading_11/12` → `ERROR fragment tokens with no
spec key`; supplying extras → `ERROR spec keys with no fragment slot`. Any count change fails the
gate it must pass, and §7.8 turns a validator failure into a discarded pattern plus a failed page.
Verified good news on the real input: the CNC page's capability table has exactly 8 rows, comparison
3 cards, process 5 steps, hero 2 buttons + 1 text link — all matching fragment arity. The trap is
latent, not immediately fatal.

---

## Contradictions to resolve in the docs

1. **§7 vs SKILL.md §8 — FIXED 2026-08-06.** AUTOMATION.md §7 requires authoring Elementor JSON and
   appending fragments, legends and `PATTERNS.md` entries; SKILL.md §8 forbade both outright, with
   no carve-out, while AUTOMATION.md §9 tells the agent to follow the skill "for all Elementor
   work". SKILL.md §8 now carries a daggered carve-out naming §7 as the sole exception, restating
   §7's gates (dedupe → build → verify → tokenise → validate → build branch only) and confirming
   every other prohibition still binds inside §7.
2. **§7 vs TRANSLATE.md §5 — FIXED 2026-08-06.** TRANSLATE.md §5.3's "stop and report" now carries
   an exception pointing at §7 for automation runs, and reaffirms stop-and-report for human-run
   translate.
3. **Autonomy vs TRANSLATE.md §10 — STILL OPEN.** §10 requires human review of the match table
   before §0; AUTOMATION.md's preamble says "Complete ALL steps without asking for input." Left
   deliberately: which one wins depends on the B3 decision about what this pipeline is for. If the
   automation keeps full autonomy, §10 should be rewritten as "emit the match table into the run
   report" rather than a blocking review.
4. **§2 delta logic was self-cancelling — FIXED 2026-08-06.** "Delta = zips whose hash is not
   present with status 'built', 'partial', or 'failed'" excluded *every* recorded zip, since those
   are the only three statuses §4 defines, making the partial-retry path and §5's "'partial' zips:
   retry failed pages only" both unreachable. Delta now reads: absent from `processed_zips`, or
   present with status "partial".
5. **Arity guidance** differs between AUTOMATION.md §3.c.ii ("counts are typical, not required") and
   TRANSLATE.md §131-150 ("a mismatch needs a decision"; only `faq-toggle` is free). See B4.
6. **§3.c.iv is unsatisfiable as written** for this export: it requires the self-contained
   interactive HTML file, but the "Select your application" explorer ships **inline** in each
   service page (the `APPS` JS object the zip's own `CLAUDE.md` calls out as easy to miss). Read
   literally, every service page is "failed: missing-interactive-asset". Someone must either extract
   the explorer into `<slug>-interactive.html` during translate — which is authoring, not
   assembling — or state that inline-interactive is an accepted input and how it's handled.
7. **Markdown corruption in AUTOMATION.md — FIXED 2026-08-06.** Two occurrences of
   `reference/[PATTERNS.md](http://PATTERNS.md)` (§3.c.ii and §6) pointed an agent at a nonexistent
   URL, and `&lt;zip-name&gt;` / `&lt;slug&gt;` / `&lt;slug-prefix&gt;` HTML entities appeared in
   §3a/b/iii/iv/vi and §3e — 16 lines changed in total. Paste artefacts, but they were instructions
   an agent reads literally.

---

## Deployment gaps

- **Branch mismatch.** The automation's workspace is
  `…/workspaces/potomac-laser/main-2` (currently on branch `main-2`, **2 commits ahead of
  `origin/main`** and unpushed), while AUTOMATION.md §1 says "The coordinator itself runs from main"
  and §2/§4 read and commit `build-state.json` "on main". As configured it would read and write the
  ledger on `main-2`.
- **`.mcp.json` is gitignored and exists only in `main-2`.** Per-zip worktrees created by §3b
  therefore have no Novamira config: any agent session started *inside* a build worktree cannot
  reach WordPress. All WP calls must stay in the coordinator's own session — which AUTOMATION.md
  never states, though SKILL.md's Context does ("Subagents cannot use these tools").
- **Agent type is `claude-agent-teams`.** Combined with the line above, delegating page builds to
  team workers means every Novamira call is auto-denied. If teams are intended, AUTOMATION.md needs
  an explicit rule that translate/verify may be delegated but all MCP writes happen in the lead.
- **`novamira-localhost` is still configured** in `.mcp.json` (currently ECONNREFUSED). SKILL.md §0
  gate 2 says confirm "localhost/dev servers are not connected" — configured-but-unreachable is
  ambiguous, and a strict reading aborts the run. Remove the entry before enabling, or reword the
  gate as "no localhost server reachable".
- **§4's "worktree comment"** maps to `orca worktree set --comment <text>` — a single metadata
  string. The §4 report (per-page status, preview URLs, enumeration, new patterns, discards, drift)
  is long for that field; consider committing `built/run-<ts>.report.md` and putting a pointer in
  the comment.
- The schedule is **disabled** (weekdays 09:00 Europe/London, 720-min missed-run grace). Nothing
  fires until someone enables it — which is the correct state today.

---

## Recommended order of fixes

1. UpdraftPlus → daily db+files, or define the backup-status file (B1). Nothing else matters until
   the gate can pass.
2. Decide the answer to B3: is this pipeline for *new* pages only (then curate the zip down to CCIT
   and friends), or does redesigning live pages need a separate human-reviewed flow? Settle the
   post-type question at the same time.
3. ~~Replace the iframe-based enumeration rule with an allow-list or explicit exclusions (B2).~~
   **Done** — add a curated `pages.txt` to this zip before the first real run.
4. ~~Reconcile §7 against SKILL.md §8 and TRANSLATE.md §5; fix the §2 delta logic; fix the
   `[PATTERNS.md](http://PATTERNS.md)` links and HTML entities.~~ **Done.** TRANSLATE.md §10's
   blocking human review is still unreconciled — see contradiction 3, which turns on the B3
   decision.
5. Either raise/remove the 8-pattern cap for a first real run or curate the zip so it fits, and
   decide how arity changes pass the validator (B4).
6. Point the automation at `main`, remove `novamira-localhost`, and state the MCP-in-lead-session
   rule in AUTOMATION.md.
7. Then dry-run one page (CCIT) with the schedule still disabled, before enabling it.
