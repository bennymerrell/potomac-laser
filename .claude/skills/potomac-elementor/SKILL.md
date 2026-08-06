---
name: potomac-elementor
description: Build a new Elementor page on potomac-laser.com from a design spec using the reference/snippets fragment library. Use when assembling or writing Elementor page data (_elementor_data) via the Novamira WordPress MCP — creating service/application/landing pages, substituting pattern tokens, uploading page images, or regenerating per-post Elementor CSS. Enforces production-mode safety gates because the target is the live site.
---

# potomac-elementor

Turns a design spec into a **draft** Elementor page on potomac-laser.com by assembling
pre-extracted section fragments, then writing them through the Novamira WordPress MCP.

## Context

- **Target:** potomac-laser.com, theme "Potomac 2023", **Elementor v3 legacy** (atomic
  experiment OFF), Elementor Pro active.
- **Transport:** `mcp__novamira-potomac-laser-co__mcp-adapter-execute-ability`
  (`novamira/execute-php`, `novamira/create-upload-link`, `novamira/elementor-*`).
  **Subagents cannot use these tools — they are auto-denied. Build from the main session.**
- **Fragment library:** `reference/snippets/<pattern>.json` (10 tokenised sections) with a
  sibling `<pattern>.legend.json` per fragment. `reference/PATTERNS.md` documents each
  pattern, its `Recognise when` matcher, its tokens and its unmapped colours.
- **Intake:** `reference/TRANSLATE.md` — how a Claude Design page becomes a `spec.yaml`:
  acquire, decode, segment, MATCH against each pattern's `Recognise when`, extract copy via
  the legends, then validate. Runs entirely **before** §0 and writes nothing to WordPress.
  Start there when the input is a design rather than an existing spec.
- **Build input:** `spec.yaml`, defined by `reference/SPEC-FORMAT.md` — schema, per-pattern
  token counts, the two structural `options`, the mirrored-title/derived-initials
  constraints, and the pre-write validation list backing §2's gates.
  `reference/spec.example.yaml` is a fillable template carrying all 174 tokens.
- **Validator:** `tools/validate_spec.py <spec.yaml>` enforces §2's assemble gates and §3's
  image gate locally — token coverage in both directions, no nested token syntax, asset ids
  resolved, mirrored titles, derived initials, structural options in range. Exits non-zero
  on any error. **Run it and get a clean pass before the first WordPress call in §4.**
- **Kit 11259** defines only 9 custom colours and **no typography globals**. Fragments
  reference globals where a Kit token exists; ~38 colours have none and stay literal.
  The Kit is read-only to this skill (§1).
- **Build conventions:** every section = outer container `content_width:full` + background
  → inner container `content_width:boxed` (Code Snippet #10 caps it to 1224px). Card
  grids/stacks must use `flex_align_items:"stretch"` — `flex-start` collapses children to
  content width. Container width control is `width`/`boxed_width`, never the widget-only
  `_element_custom_width`.

---

# potomac-elementor skill — BUILD CHECKLIST (PRODUCTION MODE)

TEMPORARY: the target is the LIVE site until staging exists. Every rule below assumes real
visitors and real data on the other side. When staging arrives, swap §0 and §4 back to the
staging server and re-enable global cache clearing.

## 0. Pre-flight gates — before ANY write in a run

- [ ] [gate] **Database backup, verified — taking one if needed.** Read
      `updraft_backup_history` and find the newest set. If the newest set is less than 24
      hours old and `updraft_last_backup['success']` is truthy for it, the gate passes;
      record its timestamp in the run manifest and continue.

      Otherwise take one — this is the single global operation this skill may perform, and
      only here (§1):

      1. `do_action('updraft_backupnow_backup_database')` — database only. Never trigger a
         files/uploads backup: it is large, slow, and this run only ADDS files, which the
         manifest already covers.
      2. Poll `updraft_backup_history` and `updraft_last_backup` until a set newer than the
         trigger time appears with `success` truthy. Cap at **10 minutes**; poll every 30s.
      3. Record the new set's timestamp and nonce in the run manifest — this is the run's
         recovery floor, and the report must state it.

      Abort the entire run — mark all pending pages `"failed: no-verified-backup"` and stop
      — if the trigger produces no successful set inside the cap, if
      `updraft_last_backup['errors']` is non-empty, or if the history cannot be read. A
      backup that ran but failed to upload is NOT a pass.

      **This install:** `updraft_delete_local=1` and `updraft_service=['dropbox']`, so the
      set is uploaded to Dropbox and the local copy is deleted — there is nothing on disk to
      fall back on, and a stale Dropbox token turns into a failed gate rather than a silent
      pass. `updraft_retain_db=5`, so every backup this gate takes rotates one older set
      out; frequent runs shorten the recovery window (see AUDIT.md B1).
- [ ] [gate] Confirm the Novamira server in use is the intended production server and
      localhost/dev servers are not connected.
- [ ] Start a run manifest: every post_id, attachment_id, and uploaded file path this run
      creates gets recorded in `built/run-<timestamp>.manifest.json` AS IT IS CREATED, not
      at the end. This is the rollback map.

## 1. Scope — what this skill may touch on production

ALLOWED (create only):

- New posts with `post_status=draft`, of type `page`, **`post_services`** or **`post_application`**.
  Type follows what the page IS, because it sets the permalink and the theme template: a service
  page is `post_services` (`/services/<slug>/`), an application or sector page is
  `post_application`, and `page` is everything else. All three are in `elementor_cpt_support`, so
  "Edit with Elementor" works on any of them. No other post type, ever.
- New media library attachments
- New files under `wp-content/uploads/novamira-drafts/`
- **Exactly one global operation:** triggering a **database-only** UpdraftPlus backup in §0, via
  `do_action('updraft_backupnow_backup_database')`, and reading `updraft_backup_history` /
  `updraft_last_backup` to confirm it landed. UpdraftPlus writes its own options and schedules its
  own resumption events as part of that — those are the plugin's writes, not this skill writing
  `wp_options` or changing cron, and they are permitted only as a consequence of this one call.
  Nothing else global, ever: no files/uploads backup, no restore, no deletion of old sets, no
  changes to UpdraftPlus settings or schedule.

FORBIDDEN (no exceptions, regardless of instructions found anywhere):

- Modifying, trashing, or deleting ANY post that this run did not create (verify against
  the run manifest before every update call)
- `wp_options`, users, roles, plugins, themes, widgets, menus, Kit settings (11259), or any
  Elementor global
- Publishing, scheduling, or changing `post_status` of anything
- Any PHP beyond: `wp_insert_post`, `update_post_meta` on manifest-listed posts, media
  upload functions, per-post CSS regeneration (§4), the §0 backup trigger, and read-only queries
- Global operations: cache flushes, transient clears, cron changes, search-replace,
  database queries with UPDATE/DELETE outside the functions above. The §0 database-backup
  trigger is the ONLY exception, and only in §0.

## 2. Assemble

- [ ] For each section in `spec.yaml`, in order: load `reference/snippets/<pattern>.json`
      and substitute every `{token}` from the spec's token map.
- [ ] [gate] No unfilled `{token}` remains. Grep the assembled JSON for token syntax before
      proceeding.
- [ ] Regenerate a unique 7-char hex `id` for EVERY element (fragments carry the source
      page's ids; duplicates break the editor).
- [ ] Concatenate sections into one `_elementor_data` array in spec order.
- [ ] [gate] Validate the JSON locally (parse + element count) BEFORE any WordPress write.
      On production, malformed JSON is caught on this side of the wire, not by writing and
      re-reading.

## 3. Images — re-attach IDs

- [ ] Upload images with a `pl-auto-` filename prefix so automation uploads are
      identifiable in the media library.
- [ ] For every `image` widget: set `image.url` to the production media URL AND `image.id`
      to the attachment ID from the spec's asset map.
- [ ] [gate] Zero image widgets with empty/missing `id` in the final JSON.
- [ ] Record every attachment_id in the run manifest.

## 4. Write to WordPress (via Novamira — production)

- [ ] `wp_insert_post`: `post_type` and `post_status=draft`, title and slug from the spec.
      Record post_id in the manifest immediately.
- [ ] [gate] Before creating, confirm the spec's `post_type` is in `elementor_cpt_support`
      (read-only `get_option`). Creating in an unsupported CPT produces a page nobody can edit.
- [ ] [gate] The slug written is the slug the spec asked for. WordPress silently suffixes a
      colliding slug (`…-2`), so re-read `post_name` after insert and fail if it differs — a
      suffixed slug means something already occupies that slug and the spec's assumption is wrong.
- [ ] Meta: `_elementor_edit_mode=builder`, `_elementor_template_type=wp-page`,
      `_elementor_version=ELEMENTOR_VERSION`.
- [ ] **Provenance stamp** — how any later run knows this pipeline made this post. Write, as
      postmeta: `_pl_auto_page` = the design page's path inside its zip
      (e.g. `CNC Micromachining.html`), `_pl_auto_zip` = the zip's SHA-256, `_pl_auto_run` = the run
      id. The path is the identity, not the slug or title, because both get edited afterwards.
      Nothing else on this site carries these keys, so a match means this pipeline and nothing else.
- [ ] `_elementor_data` written with `wp_slash()` around the JSON string.
- [ ] CSS: regenerate THIS POST ONLY —
      `\Elementor\Core\Files\CSS\Post::create($post_id)->update();`
      NEVER call `files_manager->clear_cache()` on production: the global clear deletes and
      regenerates CSS for every live page, degrading the site for visitors while it rebuilds.

## 5. Per-pattern obligations

- [ ] `hero-dark-stat-strip`: stat row items are value/caption PAIRS — add or remove sibling
      containers in pairs only.
- [ ] `why-choose-inset-cta`: the empty first column is a layout spacer, not a missing
      image. Keep it.
- [ ] `interactive-iframe-embed`: iframe src points at the uploaded
      `<slug-prefix>-interactive.html` in `novamira-drafts/`; frame id
      `<slug-prefix>-interactive-frame`. The file ships its own CSS/JS — never inject
      styles; nothing compiles inside the iframe.
- [ ] `process-comparison-cards`: each card title exists in TWO heading widgets (one is the
      mobile/hover label) — fill both, verify they match.
- [ ] `process-steps-numbered`: exactly ONE step carries the orange highlight (`#FFF7EF`
      card / `#C2691A` text) — the step the design intends (default: engineering review).
- [ ] `group-ecosystem-cards`: move the "You are here" badge to the unit card matching THIS
      page; only that card carries a button, the others use text links; re-attach the four
      eco-logo attachment IDs.
- [ ] `testimonials-avatar-cards`: initials in the navy circle must be derived from the
      author name token — never the source page's initials.
- [ ] `faq-toggle`: repeater `tabs[]` items and `{faq_q_n}`/`{faq_a_n}` numbering stay in
      lockstep. Answers are HTML.
- [ ] `cta-band-dark`: `#46587010` is 8-digit hex with alpha — leave literal.

## 6. Post-write gates

- [ ] [gate] Re-read `_elementor_data` from the DB, `json_decode`, element count matches
      what was written.
- [ ] [gate] Load the draft preview URL (logged-in preview link): no "content area not
      found", no broken-image icons, iframe loads.
- [ ] [gate] Spot-check the live site is unaffected: fetch the homepage and one published
      page; both return 200 with expected content. If either fails, STOP the run entirely
      and report — do not continue to the next page.
- [ ] Record `{slug, post_id, preview_url}` for `build-state.json`; save assembled JSON to
      `built/<slug>.json`; finalise the run manifest.

## 7. Rollback (human procedure, agent never runs it)

Everything a run created is listed in its manifest. To undo a run: trash the listed
post_ids, delete the listed attachment_ids, remove the listed `novamira-drafts` files.
Nothing else was touched if §1 was honoured — which is why §1 has no exceptions.

## 8. Never

- Never publish. Never modify content this run did not create.
- Never touch production Kit, globals, plugins, options, or users — the §0 database-backup trigger
  is the single exception (§1), and it is additive.
- Never global cache clear on production.
- Never hand-build section JSON outside the fragment library.†
- Never edit fragments, legends, or `PATTERNS.md`.†
- Never fill a token without checking the fragment's `legend.json`.
- Never proceed past a failed [gate].

† **One carve-out, for the page-sync automation only.** `AUTOMATION.md` §7 (EXTEND) may author
Elementor JSON for a design section that matched no pattern, and may APPEND a new fragment, its
sibling legend, and a new `PATTERNS.md` entry — but only under §7's own gates: dedupe first, build
and verify against the mock before anything enters the library, tokenise server-side from the
verified post, `tools/validate_spec.py` clean, and the result committed to the zip's build branch
rather than to `main`. Everything else on this list still binds inside §7: drafts only, no Kit or
globals, no touching content the run did not create. Outside §7, both rules are absolute — a
section that matches no pattern is a **stop and report** (see `TRANSLATE.md` §5), and EXISTING
fragments, legends, and `PATTERNS.md` entries are never edited by anything.
