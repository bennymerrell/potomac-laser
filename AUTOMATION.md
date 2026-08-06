# Potomac Page Sync — autonomous create-and-improve run (project-zip trigger)

Every page in the zip gets built, whether or not the pattern library already
covers it. Sections that match a documented pattern are assembled from it;
sections that match nothing are authored, verified, and then tokenised back
into the library as new patterns (§7), so each run leaves the library able to
recognise more of the next design.

You are the build coordinator. Complete ALL steps without asking for input. Follow the potomac-elementor skill for all Elementor work. TEMPORARY: the target is the LIVE site (potomac-laser.com) until staging exists, so every write runs in the skill's PRODUCTION MODE under its §0 pre-flight gates. Never publish. Never edit existing pages.

## 1. FETCH

git fetch origin. Read the project-zip branch in read-only fashion — never commit to it. The coordinator itself runs from main, where this file, build-state.json, reference/, and the skill live.

## 2. DETECT NEW WORK

List all *.zip files on origin/project-zip. Compute each file's SHA-256. Compare against processed_zips in build-state.json (on main).

Delta = zips whose hash is either absent from `processed_zips` entirely, or present with status "partial". A hash recorded "built" or "failed" is never reprocessed. Zips marked "partial" are re-entered ONLY to retry pages whose individual status is "failed" or missing — never rebuild pages already marked "built" or "skipped-already-built".

If the delta is empty, exit silently. Do nothing else.

## 3. FOR EACH new zip (sequentially)

a. UNPACK into a temp dir. Enumerate page-level HTML files — entry documents only.

**If the zip root contains `pages.txt`, it is the allow-list: one entry per line and the complete set of pages. Enumerate exactly those and nothing else.** A human curating the zip is cheaper than the automation guessing. Each line is a path relative to the zip root, optionally followed by the post type to build it as (`page`, `post_services` or `post_application`; default `page`). Blank lines and lines starting with `#` are ignored.

**Parse rule — design filenames contain spaces, so do not split on the first whitespace.** Trim the line; if its LAST whitespace-separated token is exactly `page`, `post_services` or `post_application`, that token is the post type and everything before it, trimmed, is the path. Otherwise the whole trimmed line is the path and the type is `page`. The three are a closed set, and no design filename ends in one of them, so this never misreads a path.

```
CNC Micromachining.html                 post_services
Services & Applications.html            page
uploads/sector-medical-potomac.html
# entries not listed here are not built — see reference/pages.example.txt
```

A path in `pages.txt` that does not exist in the zip is a zip-level error: report it and mark the zip `"failed"` rather than silently building a subset — a typo in the allow-list would otherwise look like a deliberate omission.

With no `pages.txt`, enumerate `*.html` in the zip ROOT ONLY and exclude, by path and filename:

- any file not in the zip root — `_src/`, `uploads/`, `assets/`, `screenshots/`, `_ds/`, and any other subdirectory. Nested HTML in a design export is source material, working copies, or handoff variants, never a page to build.
- `*.dc.html` — design-canvas documents (`<x-dc>` wrappers), not pages.
- `* (standalone).html` and any file whose section structure is byte-identical to another enumerated page — self-contained duplicates of a page already in the list.
- any file with zero `<section>` elements — empty canvases and partials such as a site footer.

Do NOT use "referenced from an iframe" as the test for interactive app files: an export may embed its interactive markup inline, in which case no iframe exists and the test silently passes everything (see 3.c.iv).

List the enumerated pages in the final report, **and every file excluded with the rule that excluded it**, so a human can confirm nothing was missed and correct the next zip with a `pages.txt`.

b. WORKTREE: using the orca CLI, create ONE worktree/branch per zip, named build/<zip-name>, from main. All pages from this zip are built in this worktree.

c. FOR EACH page in the zip:

i. IDENTITY: the question here is **"has this pipeline already created this page?"** — never "does anything with this slug exist?". Live pages and pre-process duplicates are irrelevant to it: they were made before this process existed, and a fresh draft is meant to be built alongside them, not skipped because of them.

**Check by provenance, via Novamira:** query for a post with postmeta `_pl_auto_page` = this design page's path inside the zip, at `post_status=any` and `post_type=any`.

- **Hit** → this pipeline built it. Record `"skipped-already-built"` with the existing post_id and continue. The one exception: if this zip's status is `partial` and this page's recorded status is `"failed"` or missing, re-enter and rebuild it.
- **Miss** → build it, regardless of what else lives at that slug. `build-state.json` is the ledger of record, but it lives on a build branch that may never merge — so if WP meta says this pipeline built a page and the ledger disagrees, trust WP and reconcile the ledger.

**POST TYPE:** type follows what the page IS, because it sets the permalink and the theme template — a service page is `post_services` (`/services/<slug>/`), an application or sector page is `post_application`, everything else is `page`. Nothing else is permitted — SKILL.md §1. If `pages.txt` gives a type for the page, use it; otherwise infer from the design and state the inference in the report. SKILL.md §4 gates every type against `elementor_cpt_support` before creating.

**SLUG:** kebab-case from the filename or `<title>`, then namespace it: `pl-auto-<slug>`, mirroring the `pl-auto-` media prefix. Live pages keep the clean slugs, this run's drafts cannot collide with them, and WordPress cannot silently suffix them into something the report would misstate. Renaming at go-live is a human step.

Record the design page's path, the resolved post type, and the final slug in the report — the path is the identity that survives a human editing the title or slug later.

ii. MATCH: segment the design page into sections and match each section against the "Recognise when" field of every pattern in reference/PATTERNS.md. Element counts in "Recognise when" are typical, not required, wherever the pattern's Notes mark the count as adjustable (stat pairs, step cards, spec rows, FAQ items) — match on structure, not count. Record the match result per section: a pattern id, or `UNMATCHED`.

If every section matches, the page is a STANDARD BUILD — continue to iii.

If any section is `UNMATCHED`, the page is an EXTEND BUILD: it is still built, and each unmatched section becomes a candidate new pattern via §7. Do NOT fail the page for being unmatched. A page only fails here if §7 itself cannot produce a verified pattern for it. A page failure never sinks its sibling pages.

iii. TRANSLATE into the standard handoff: - copy the page's source to specs/<slug>/design-export/ (source of truth) - write specs/<slug>/mock.html (the page HTML with assets rewired to relative paths) - write specs/<slug>/spec.yaml as an ordered list of sections. Each section = the pattern id plus a token map filling that fragment's placeholders:

```
          sections:
            - pattern: hero-dark-stat-strip
              tokens:
                heading_1: "LASER MICROMACHINING SERVICES"
                heading_2: "Precision Laser Micromachining<br>at the Micro Scale."
                body_1: "<p>…intro copy…</p>"
                button_1: "Request a Quote"
                url_1: "#quote"
                # …every token the fragment defines

      Before filling any fragment, read its sibling
      reference/snippets/<id>.legend.json — the legend maps every
      token to the original copy it replaced; use it to understand
      each slot's intent. Fill EVERY token the fragment defines.
      For repeater/adjustable patterns, add or remove items per
      the pattern's Notes and number the tokens accordingly.

```

iv. ASSETS: - Images: upload this page's images to the WP media library on potomac-laser.com via Novamira, with the `pl-auto-` filename prefix required by SKILL.md §3; record {token → attachment_id, url} in the spec. Dedupe within the zip — if an identical image was already uploaded for a sibling page in this run, reuse the existing attachment ID. - Interactive apps: if the page uses interactive-iframe-embed, the design export MUST contain the self-contained interactive HTML file (it ships its own CSS/JS — nothing compiles inside the iframe). Upload it to wp-content/uploads/novamira-drafts/ named <slug-prefix>-interactive.html and point the iframe's src at it, with frame id <slug-prefix>-interactive-frame. If the page has an interactive section but the export contains no such file, mark the page "failed: missing-interactive-asset" and move on.

v. BUILD: follow the potomac-elementor skill build checklist exactly, including image ID re-attachment and per-pattern obligations. Matched sections are assembled from their fragments as usual; `UNMATCHED` sections use the Elementor JSON authored in §7 step 2. Create the page as a DRAFT on potomac-laser.com via Novamira. Regenerate the Elementor CSS for THIS POST ONLY after writing (`\Elementor\Core\Files\CSS\Post::create($post_id)->update();`) — NEVER the global `files_manager->clear_cache()`, which SKILL.md §4 forbids on production.

vi. VERIFY: open the draft preview in the Orca browser, screenshot, compare against specs/<slug>/mock.html. Fix discrepancies and re-check. Max 3 iterations; if still not matching, mark the page "failed: verify" with a note on what differs, and move on.

d. LINK PASS: after all pages in the zip are built, if pages link to each other in the design export, rewrite those internal links in the built pages to the draft preview URLs. Skip this step if there are no cross-links.

e. COMMIT the worktree branch — specs/, generated built/<slug>.json for every page, any new fragments/legends and PATTERNS.md entries from §7, and the run manifest, all from this zip in one branch — and push it. Do NOT merge to main.

## 4. STATE + REPORT

On main, update build-state.json with per-page status under each zip:

```
{
  "processed_zips": [
    {
      "zip_hash": "…",
      "filename": "…",
      "branch": "build/<zip-name>",
      "status": "built" | "partial" | "failed",
      "pages": [
        {
          "slug": "…",
          "post_id": 123,
          "preview_url": "…",
          "build_type": "standard" | "extend",
          "design_page": "CNC Micromachining.html",
          "post_type": "page" | "post_services" | "post_application",
          "status": "built" | "failed: <reason>" | "skipped-already-built"
        }
      ],
      "new_patterns": [
        {
          "id": "contact-form-split",
          "source_post_id": 12401,
          "section_index": 1,
          "minted_by": "contact",
          "reused_by": ["ccit"]
        }
      ]
    }
  ]
}

```

Zip status is "built" if every page is built or skipped-already-built, "partial" if any page failed, "failed" if the zip could not be unpacked or enumerated at all.

Commit and push build-state.json. Write a worktree comment on the coordinator run summarising: pages built / failed / skipped per zip, with preview URLs, branch names, the page enumeration from 3a, every new pattern minted by §7 (with which page minted it and which reused it), every candidate pattern DISCARDED and why, and the §8 drift report.

## 5. FAILURE RULES

- Any unresolvable error after 2 attempts → mark the page (or zip, if the failure is at zip level) "failed" with the reason, and MOVE ON. Never loop.
- A discarded §7 candidate pattern fails only its page, never the zip, and never removes a pattern already verified earlier in the run.
- Never reprocess a zip hash marked "built" or "failed". "partial" zips: retry failed pages only.
- A human resets a "failed" entry by deleting it from build-state.json; do not do this yourself.

## 6. HARD BOUNDARIES

- Production Novamira server (`novamira-potomac-laser-co`) only, in the skill's PRODUCTION MODE. Staging does not exist yet; when it does, switch here and in SKILL.md §0/§4 together. Localhost/dev servers must NOT be connected during a run (SKILL.md §0 gate).
- Honour SKILL.md §0 before any write: a backup verified less than 24h old — verified, not assumed — or abort the entire run, marking pending pages "failed: no-verified-backup". This is the one condition that stops the whole run rather than one page.
- Record every post_id, attachment_id, and uploaded file path in `built/run-<timestamp>.manifest.json` AS IT IS CREATED. It is the rollback map, and SKILL.md §1 requires checking it before any update call.
- Never global cache clear. Never touch Kit 11259, `wp_options`, users, roles, plugins, themes, widgets, menus, or any Elementor global.
- Drafts only. Publishing is human-only.
- Never modify a published page in place.
- Never commit to the project-zip branch.
- Documented patterns are filled via their fragment tokens — never improvised. Authoring NEW Elementor JSON is permitted ONLY inside §7, only for a section that matched nothing, and only when it survives §7's verify gate. Anywhere else, hand-built JSON is still forbidden.
- Never edit an EXISTING entry in reference/PATTERNS.md, an existing fragment, or an existing legend. §7 may only APPEND new ones. The existing 10 patterns and their provenance from post 12133 are regenerated by a separate human-supervised process, not by this automation.
- New patterns from §7 live on the zip's build branch only. They are usable within the run that created them, but they do not enter the shared library on main without a human merge. Never commit a §7 pattern directly to main.
- Never modify or update a post this run did not create, even when its content has drifted from the design, even when it sits at the slug this page "should" have. Record it in §8 and leave it alone. The only posts this run may write to are the ones it created and recorded in the manifest.
- Drafts are created at `pl-auto-<slug>` and stamped `_pl_auto_page` / `_pl_auto_zip` / `_pl_auto_run` (SKILL.md §4). That stamp is the only thing that makes a later run's §3.c.i correct — never skip it, and never write it onto a post this run did not create.

## 7. EXTEND — adding a pattern autonomously

Triggered per `UNMATCHED` section from 3.c.ii. The library's existing fragments were tokenised **server-side from an already-built Elementor post** (PATTERNS.md §Regenerating) — there is no way to tokenise a design HTML file directly. So the pipeline inverts: author the section, build it, verify it, and only then tokenise the verified result into a fragment.

**1. DEDUPE FIRST.** Compare the section against (a) every documented pattern once more at reduced strictness, and (b) every pattern already minted by §7 earlier in this run. If it matches one, use that — do not mint a near-duplicate. Sibling pages in a zip usually share sections: the first page to hit a given section mints the pattern, the rest reuse it. Log every dedupe hit in the report.

**2. AUTHOR the Elementor JSON** for the section, using `reference/snippets/*.json` as the structural reference for how this site builds Elementor v3 legacy data:

- Widget types from semantics: headings → `heading`, copy → `text-editor`, CTAs → `button`, imagery → `image`, FAQ/accordion → `toggle`, self-contained interactive markup → `html`.
- Container nesting and `_element_custom_width` conventions copied from the nearest existing fragment, not invented.
- Colours: map every value to a Kit 11259 global token (PATTERNS.md §Kit global tokens) via `__globals__` refs. A value with no token stays literal and is listed under the entry's **Unmapped colours** — do NOT add Kit tokens, do NOT touch the Kit.
- Typography/spacing: read `_ds/*/tokens/*.css` in the export for the design's intent, express it with the site's existing conventions.
- Unique 7-char hex `id` on every element, per SKILL.md §2.

**3. BUILD AND VERIFY BEFORE ADDING.** The authored section ships inside its page and goes through 3.c.v and 3.c.vi unchanged. A pattern is NEVER added to the library on the strength of authored JSON alone — it must render correctly against the mock. If the page fails verify after 3 iterations, mark it `"failed: verify"`, DISCARD the candidate, and move on. Nothing enters the library.

**4. TOKENISE the verified section** server-side from the page just built, reusing the §Regenerating process: `novamira/execute-php` to tokenise → apply the colour global map → write to `wp-content/uploads/novamira-drafts/patterns/` → download → verify by SHA-256. The newly built post becomes this pattern's `Source`, exactly as post 12133 is for the original 10. Placeholder vocabulary per PATTERNS.md (`{heading_n}`, `{body_n}`, `{button_n}`, `{url_n}`, `{image_n}`, `{embed_n}`, `{faq_q_n}`/`{faq_a_n}`), numbered per-fragment in document order.

**5. WRITE the sibling legend** `reference/snippets/<id>.legend.json`, mapping every token to the copy it replaced — the same contract the existing 10 legends honour.

**6. APPEND the PATTERNS.md entry** using the Entry template verbatim, filling every field: `Snippet`, `Source` (new post_id + section index), `Used by`, `Signature`, `Recognise when`, `Structure`, `Tokens`, `Globals`, `Unmapped colours`, `Notes`. **`Recognise when` is the field that makes the pattern reusable** — write it so a future run's 3.c.ii can match a similar section on structure, and mark element counts adjustable where they genuinely are. Append to the `# Patterns` section and add a row to `## Page coverage`. Do not restructure the file or touch existing entries.

**7. ID NAMING:** `<shape>-<qualifier>`, matching the existing vocabulary (`hero-dark-stat-strip`, `cta-band-dark`). Describe the section's structure, not the page that happened to need it — `contact-form-split`, not `contact-page-section-2`.

**8. VALIDATE:** run `python3 tools/validate_spec.py --automation` on every spec using a new pattern. A validator failure is a §7 failure: discard the pattern, fail the page, move on.

**9. CAP:** at most 8 new patterns per zip. On the 9th unmatched section, stop minting — mark remaining pages `"failed: pattern-budget-exhausted"` and report. A design needing more than 8 new patterns is a library-design problem for a human, not an automation problem.

**10. RECORD** each new pattern in build-state.json under `new_patterns`: id, source post_id, section index, the page that minted it, and which pages reused it.

## 8. DRIFT REPORT

Existing pages never affect what gets built (§3.c.i) — but a design shipping a page the site already has is signal, and this report is where it lands. It is **informational only, and never a skip trigger**.

For every page in the zip, whether built or skipped, search read-only for its likely live counterparts and record what you find:

- **slug family:** `<slug>`, `<slug>-services`, `<slug>-services-draft`, `<slug>-services-draft-blocks`, and any slug that starts with `<slug>-` — the site's naming convention appends suffixes, so an exact-slug search finds nothing useful. CNC Micromachining exists four times under four suffixed slugs; a bare `cnc-micromachining` lookup matches none of them.
- **title match:** posts whose title matches the design's `<title>` or `<h1>`, case- and punctuation-insensitive.

For each counterpart record: post_id, post_type, post_status, slug, permalink, Elementor section count (0 = not an Elementor page), and last-modified date. Flag any whose section count differs from the design's, and note which ones carry `_pl_auto_page` (this pipeline's work) versus which do not (live or pre-process).

Nothing is modified. This is a to-do list for a human deciding what to retire, redirect, or promote.

