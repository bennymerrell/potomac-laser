# Potomac Page Sync — autonomous run (project-zip trigger)

You are the build coordinator. Complete ALL steps without asking for input. Follow the potomac-elementor skill for all Elementor work. TEMPORARY: the target is the LIVE site (potomac-laser.com) until staging exists, so every write runs in the skill's PRODUCTION MODE under its §0 pre-flight gates. Never publish. Never edit existing pages.

## 1. FETCH

git fetch origin. Read the project-zip branch in read-only fashion — never commit to it. The coordinator itself runs from main, where this file, build-state.json, reference/, and the skill live.

## 2. DETECT NEW WORK

List all *.zip files on origin/project-zip. Compute each file's SHA-256. Compare against processed_zips in build-state.json (on main).

Delta = zips whose hash is not present with status "built", "partial", or "failed". Zips marked "partial" are re-entered ONLY to retry pages whose individual status is "failed" or missing — never rebuild pages already marked "built" or "skipped-exists".

If the delta is empty, exit silently. Do nothing else.

## 3. FOR EACH new zip (sequentially)

a. UNPACK into a temp dir. Enumerate ALL page-level HTML files — entry documents only. Exclude fragments/partials that are only referenced by other pages, asset folders, and any self-contained interactive app files (see 3.c.iv — those are assets, not pages; identify them by being referenced from an iframe in a page document). List the enumerated pages in the final report so a human can confirm nothing was missed.

b. WORKTREE: using the orca CLI, create ONE worktree/branch per zip, named build/&lt;zip-name&gt;, from main. All pages from this zip are built in this worktree.

c. FOR EACH page in the zip:

i. SLUG: derive from the page filename or &lt;title&gt;, kebab-cased. If a page with this slug already exists in WP (check via Novamira, any post status), record "skipped-exists" for that page and continue to the next page.

ii. MATCH: segment the design page into sections and match each section against the "Recognise when" field of every pattern in reference/[PATTERNS.md](http://PATTERNS.md). Element counts in "Recognise when" are typical, not required, wherever the pattern's Notes mark the count as adjustable (stat pairs, step cards, spec rows, FAQ items) — match on structure, not count. HARD RULE: only documented patterns. If a section matches no pattern, mark THIS PAGE "failed: unknown-pattern &lt;short description of the section&gt;" and continue with the next page. A page failure never sinks its sibling pages.

iii. TRANSLATE into the standard handoff: - copy the page's source to specs/&lt;slug&gt;/design-export/ (source of truth) - write specs/&lt;slug&gt;/mock.html (the page HTML with assets rewired to relative paths) - write specs/&lt;slug&gt;/spec.yaml as an ordered list of sections. Each section = the pattern id plus a token map filling that fragment's placeholders:

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

iv. ASSETS: - Images: upload this page's images to the WP media library on potomac-laser.com via Novamira, with the `pl-auto-` filename prefix required by SKILL.md §3; record {token → attachment_id, url} in the spec. Dedupe within the zip — if an identical image was already uploaded for a sibling page in this run, reuse the existing attachment ID. - Interactive apps: if the page uses interactive-iframe-embed, the design export MUST contain the self-contained interactive HTML file (it ships its own CSS/JS — nothing compiles inside the iframe). Upload it to wp-content/uploads/novamira-drafts/ named &lt;slug-prefix&gt;-interactive.html and point the iframe's src at it, with frame id &lt;slug-prefix&gt;-interactive-frame. If the page has an interactive section but the export contains no such file, mark the page "failed: missing-interactive-asset" and move on.

v. BUILD: follow the potomac-elementor skill build checklist exactly, including image ID re-attachment and per-pattern obligations. Create the page as a DRAFT on potomac-laser.com via Novamira. Regenerate the Elementor CSS for THIS POST ONLY after writing (`\Elementor\Core\Files\CSS\Post::create($post_id)->update();`) — NEVER the global `files_manager->clear_cache()`, which SKILL.md §4 forbids on production.

vi. VERIFY: open the draft preview in the Orca browser, screenshot, compare against specs/&lt;slug&gt;/mock.html. Fix discrepancies and re-check. Max 3 iterations; if still not matching, mark the page "failed: verify" with a note on what differs, and move on.

d. LINK PASS: after all pages in the zip are built, if pages link to each other in the design export, rewrite those internal links in the built pages to the draft preview URLs. Skip this step if there are no cross-links.

e. COMMIT the worktree branch — specs/, generated built/&lt;slug&gt;.json for every page, all from this zip in one branch — and push it. Do NOT merge to main.

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
          "status": "built" | "failed: <reason>" | "skipped-exists"
        }
      ]
    }
  ]
}

```

Zip status is "built" if every page is built or skipped-exists, "partial" if any page failed, "failed" if the zip could not be unpacked or enumerated at all.

Commit and push build-state.json. Write a worktree comment on the coordinator run summarising: pages built / failed / skipped per zip, with preview URLs, branch names, and the page enumeration from 3a.

## 5. FAILURE RULES

- Any unresolvable error after 2 attempts → mark the page (or zip, if the failure is at zip level) "failed" with the reason, and MOVE ON. Never loop.
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
- Only patterns documented in reference/[PATTERNS.md](http://PATTERNS.md), filled via their fragment tokens. No improvised layouts, no hand-built JSON.
- Never edit reference/[PATTERNS.md](http://PATTERNS.md), the fragments, or the legends — they are regenerated by a separate human-supervised process, not by this automation.

