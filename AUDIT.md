# Readiness audit — autonomous page-sync automation

Audited 2026-08-06 against `AUTOMATION.md` (a699e3b), `.claude/skills/potomac-elementor/SKILL.md`,
`reference/*`, `tools/validate_spec.py`, the Orca automation `Potomac - Claude to WP`, the queued
input `Potomac Laser.zip` on `origin/project-zip`, and the live site via read-only Novamira calls.

**Verdict: NOT READY — do not enable the schedule.** Five blockers found. **B2, B3 and B5 are now
fixed in-repo**; **B1 and B4 remain open** and both need a human decision, not a code change. B1
stops the run at its first gate, so it is the one that matters most.

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

### B3 — 7 of 11 real pages resolve to `skipped-exists`, all for the wrong reason. FIXED 2026-08-06.

**Corrected 2026-08-06 after clarification from the project owner:** the question §3.c.i needs to
answer is *"has this pipeline already created this page?"* — not *"does anything with this slug
exist?"*. Every live page and every pre-process duplicate on the site is irrelevant to that
decision: those pages were made before the process existed, and the automation is meant to build a
fresh draft alongside them, not stand down because they are there. So the table below is not a
safety feature working as intended — it is 7 pages skipped for a reason that has no bearing on the
question. See **B5** for the mechanism and the fix; this entry records the blast radius.

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

So the run's output is 3 real new pages, ~8 junk pages (B2), and 8 pages skipped that should have
been built. Once B5 is fixed, all 11 build.

Two secondary defects surface here:

- **Post-type mismatch — FIXED 2026-08-06.** The five service pages belong to `post_services`
  (that's what their live equivalents are, and it's in `elementor_cpt_support`), but SKILL.md §1
  permitted `post_type=page` only and the validator hard-errored on anything else. `post_services`
  is now allowed end to end: SKILL.md §1, §4's pre-create `elementor_cpt_support` gate,
  `ALLOWED_POST_TYPES` in the validator, SPEC-FORMAT.md, and §3.c.i's rule that type follows what
  the page IS: `post_services` for services (`/services/<slug>/`), `post_application` for
  application and sector pages, `page` for everything else. No other type is permitted, and §4
  gates the chosen type against `elementor_cpt_support` before creating.
- **§3.c.i's scoping ambiguity — MOOT as of the B5 fix.** The check no longer looks at slugs at
  all, so there is nothing left to scope. WP's silent slug suffixing is now caught two ways: the
  reserved `pl-auto-` namespace means nothing should collide, and SKILL.md §4 re-reads `post_name`
  after insert and fails if it differs from the spec.

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

### B5 — Nothing on the site records that a page was built by this pipeline, so §3.c.i infers it from the slug and gets it wrong in both directions. FIXED 2026-08-06.

The check in §3.c.i is meant to answer one question: **has this pipeline already created this
page?** A slug lookup cannot answer it, because the slug is neither necessary nor sufficient.

Verified on production — there is no provenance marker of any kind to check against:

- Zero postmeta keys matching `%novamira%`, `%pl_auto%`, `%pl-auto%`, or `%_auto_source%` anywhere
  in the database.
- Zero attachments with the `pl-auto-` prefix, so even SKILL.md §3's media convention has never run.
- Meta on the pipeline-adjacent pages (12133, 12226) is indistinguishable from any hand-built
  Elementor page: `_elementor_*`, `_wp_page_template`, `_edit_lock`. Nothing says who made it.

The slug proxy then fails both ways:

- **False positive (7 pages).** `laser-micromachining`, `3d-printing`, `micro-hole-drilling`,
  `about-our-group`, `contact`, `project-gallery`, `services-applications` all hit *live, published,
  pre-process* pages and skip. The pipeline never built them; they should build.
- **False negative (CNC).** CNC Micromachining exists four times — 11893
  `cnc-micro-machining-services`, 12127 `cnc-micromachining-services-draft`, **12133**
  `cnc-micromachining-services-draft-blocks` (the fragment library's own provenance page, 10
  sections), 12102 `cnc-new-temp` — and the derived slug `cnc-micromachining` matches none of them.
  The page builds as a fifth artifact. It also never reaches the §8 drift report, because drift only
  covers pages recorded `skipped-exists`, so an exact-slug miss is invisible to the run.
- **Silent collision.** Where a slug does collide and the check is scoped by post type, WordPress
  appends a suffix (`laser-micromachining-2`) without complaint, so the page the run reports is not
  at the slug the spec asked for.

#### The rule, as implemented 2026-08-06

**Identity is provenance, not slug.**

1. **Stamp on create.** In SKILL.md §4, alongside the `_elementor_*` meta, write:
   `_pl_auto_page` = the design page's path inside the zip (`CNC Micromachining.html`) — the stable
   identity, since slugs and titles get edited afterwards; `_pl_auto_zip` = zip SHA-256;
   `_pl_auto_run` = run id. `update_post_meta` on a manifest-listed post is already permitted by
   §1, so this needs no widening of scope.
2. **Check by meta.** §3.c.i becomes a `meta_key=_pl_auto_page` query at `post_status=any`,
   `post_type=any`. Hit → this pipeline built it: record `skipped-already-built` and move on (or, if
   the zip is `partial` and that page's status is `failed`, re-enter it). Miss → build, regardless
   of what else lives at that slug. Retire the `skipped-exists` status.
3. **Ledger primary, meta as backstop.** `build-state.json` `pages[].post_id` remains the record of
   record, but it lives on a build branch that may never merge — so when WP meta shows a page this
   pipeline built and the ledger doesn't, trust WP and reconcile the ledger.
4. **Reserve a slug namespace.** Create drafts at `pl-auto-<slug>`, mirroring the `pl-auto-` media
   prefix. Live pages keep the clean slugs, the automation's drafts never collide (so no silent
   `-2` suffixing), and they are obvious in the admin list. A human renames at go-live.
5. **Repoint the drift report.** §8 becomes read-only "possible counterparts": for each design page,
   list live posts whose slug is in the same family (`<slug>`, `<slug>-services`,
   `<slug>-services-draft*`, `<slug>-*`) or whose title matches, with post_id, type, status, section
   count, last-modified, and whether the post carries `_pl_auto_page`. Informational for a human,
   never a skip trigger — which is the only way 12133 would have shown up in this run's report.

Where each piece landed: AUTOMATION.md §3.c.i (identity/post type/slug), §3a `pages.txt` optional
per-page post type, §4 ledger fields `design_page` + `post_type` and the `skipped-already-built`
status, §6 boundaries, §7.8 `--automation`, §8 drift report; SKILL.md §1 (allowed types) and §4
(pre-create CPT gate, post-insert slug check, provenance stamp); `validate_spec.py`
(`ALLOWED_POST_TYPES`, `--automation` slug-namespace enforcement); SPEC-FORMAT.md and
spec.example.yaml.

Verified after the change: `post_services` + `pl-auto-` slug passes under `--automation`;
`post_application` is rejected; a bare slug is rejected under `--automation` but still passes for a
hand-run spec; `spec.example.yaml --template` unchanged at 174 tokens / 0 errors.

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
2. ~~Implement B5 — the `_pl_auto_page` stamp, the meta-based check, the `pl-auto-` slug namespace,
   and the repointed drift report; settle the post-type question (B3).~~ **Done** — services build
   as `post_services`, applications and sector pages as `post_application`, everything else as
   `page`; all three verified present in `elementor_cpt_support`.
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
