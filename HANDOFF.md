# HANDOFF — Claude Design → Claude Code → WordPress (Elementor Pro + WindPress/Tailwind)

**Objective:** take *any* project from Claude Design and reliably ship it to **potomac-laser.com** as new **pages / posts / Elementor Pro blocks** via the **Novamira WordPress MCP** — now using **WindPress (Tailwind for WordPress)** to carry the design's Tailwind classes straight through, making the Design→WP transition faster and more pixel-accurate than the CNC build.

This doc is a **repeatable, staged plan with paste-ready prompts**. Run the **Master Prompt** (§5) for a full build, or run stages individually (§6). Everything Claude Code needs is here + in the two memory files `potomac-elementor-rebuild.md` and `potomac-hubspot-forms.md`.

---

## 1. Environment & key facts

| Thing | Value |
|---|---|
| Site | potomac-laser.com — theme "Potomac 2023", **Elementor Pro (legacy v3 containers; atomic experiment OFF)** |
| MCP | `mcp__novamira-potomac-laser-co__mcp-adapter-execute-ability` (+ `-discover-abilities`, `-get-ability-info`). **Subagents can't use it — run from the main session.** |
| Key abilities | `novamira/execute-php`, `novamira/elementor-{add,edit,delete,get,set}-content-element`, `novamira/create-upload-link`, `novamira/code-snippets-{create,edit,enable,validate,get-types-schema}-snippet`, `novamira/aioseo-edit-post-seo`, `novamira/skill-get` |
| Tailwind | **WindPress 3.2.85** (Tailwind **v4**, CSS-first). **Configured ✅** — brand tokens live in the `brand.css` volume entry, imported by `main.css`; compiles via a DOM **observer** (`windpress:observer-js`) + cached inline CSS. See Stage C. |
| Other plugins | Gravity Forms + **GF HubSpot add-on**, **GTM4WP** (`GTM-KVRK6DFF`), Rank Math (SEO + GA), WP Rocket (cache), Code Snippets Pro |
| HubSpot | portal **143181153** (shared Goodfellow/Salesforce portal); `[Potomac]` / `potomac_*` property convention |
| GA4 | **`G-MQSBBH2M4J`** (property 359178110) — configured inside GTM `GTM-KVRK6DFF` |
| QA | Claude-in-Chrome (**blocked from google.com / tagmanager domains** — can't configure GTM or GA UI; can read network on the site) |
| Deploy note | Cloudflare + WP Rocket in front → **purge cache** (`rocket_clean_domain()`) + `delete_post_meta($id,'_elementor_css')` after edits |

### Reference build (the CNC page — copy patterns from it)
- Page: **post 12133**, slug `services/cnc-micromachining-services-draft-blocks` (published but hidden from nav + noindex).
- Reusable Elementor templates: **12135–12145** (Hero / Why-us / Capabilities / Process comparison / Process timeline / Ecosystem / Testimonials / FAQ / Final CTA / Interactive funnel / Full page).
- Code Snippets: **#9** hide drafts from nav, **#10** full-bleed page treatment, **#12** file-upload REST endpoint.
- Funnel file: `wp-content/uploads/novamira-drafts/cnc-interactive.html` (interactive cluster embedded via iframe+bridge).
- HubSpot quote form GUID: `9eb36566-4364-4467-8592-15c743bdc901`.

---

## 2. Architecture decisions (and why)

1. **Legacy Elementor v3 containers**, not the atomic/e-* widgets (experiment is OFF). Build with `elType:container` + widgets `heading / text-editor / button / image / icon / toggle / html / shortcode`.
2. **WindPress Tailwind is now the primary styling path.** Claude Design outputs Tailwind utility markup; WindPress compiles it on the site, so we keep the design's classes instead of re-deriving Elementor styles or hand-inlining CSS. This is the big speed/fidelity win over the CNC build (which pre-dated WindPress and used per-element `custom_css`).
3. **Editability is preserved by structure, not by avoiding HTML.** One Elementor **HTML widget per section** = sections stay reorderable/toggleable in Elementor while the *inside* is pixel-perfect Tailwind. Text-only sections that need frequent copy edits use native `heading`/`text-editor` widgets with Tailwind classes in the **CSS Classes** field.
4. **Full-bleed page treatment via a body-class snippet** (not per-page CSS): outer containers go full width, inner content boxed to the theme's 1224px, theme's duplicate `<h1>` hidden. One snippet covers all built pages.
5. **Interactive/JS clusters (baskets, multi-step, drawers) = a standalone HTML file embedded as an iframe + a "bridge"** — because a `position:fixed` drawer inside a mid-page iframe gets clipped; the bridge promotes the iframe to a full-viewport overlay while open and auto-heights it otherwise. Only use this for genuinely interactive clusters; static sections are native blocks.
6. **Forms submit *directly* to HubSpot via the Forms API** (`api.hsforms.com/submissions/v3/integration/submit/{portal}/{guid}`) from the (same-origin) iframe JS — no auth, CORS-ok. Chosen over the GF add-on because the funnel forms are bespoke. Standard/simple forms can still use Gravity Forms + the GF HubSpot feed.
7. **Analytics = direct gtag from the iframe** (not GTM), because Claude can't reach the GTM UI and GTM keeps `gtag` internal. `send_page_view:false` + Consent Mode (`ad_storage:denied`) avoids duplicate pageviews/Ads. Events also push to the parent `dataLayer` so it can be re-routed through GTM later.
8. **Page-agnostic components.** Forms/tracking read `window.parent` for page URL/title so the same component reports the correct page on any page it's embedded on. Identify the *form* by `form_id`, the *page* by `page_path`/`page_location`.
9. **PII stays out of GA4** (email/name/phone report `filled`-only); full values go to HubSpot only.

---

## 3. What's been built (status)

- ✅ CNC page (post 12133): 10 native Elementor sections + interactive funnel iframe + FAQ + process timeline, styled to the design.
- ✅ Reusable Elementor templates (12135–12145).
- ✅ Two funnel forms (Rapid Response Quote + Material/Machining Basket) → **direct-to-HubSpot** (form `9eb36566…`), with file upload (WP endpoint → HubSpot re-hosts), UTM + `hubspotutk` attribution, and **in-situ confirmations** (no `alert()`s).
- ✅ Analytics: `lead_form_{start,field,submit,submit_success,submit_error}` → GA4 `G-MQSBBH2M4J` (direct gtag, Consent Mode) + parent `dataLayer`; page captured per-submission.
- ✅ Snippets #9/#10/#12.
- ✅ **WindPress configured** — Goodfellow brand tokens in `brand.css`, compiling site-wide (Tailwind v4, DOM observer). Ready for the Tailwind-first build path.

---

## 4. Build-path decision (per section)

For each design section, pick:
- **HTML-widget + Tailwind (default, fastest):** paste the design's section markup into an Elementor HTML widget; WindPress compiles the classes. Use for visual/complex sections (heroes, cards, timelines, gradients).
- **Native Elementor widgets + Tailwind CSS classes:** for copy-heavy sections the client edits often (put Tailwind classes in each widget's *CSS Classes* field).
- **iframe + bridge:** only for interactive JS clusters (basket, multi-step quote, drawers, tabs with state).

> Rule of thumb: **static → HTML-widget/Tailwind; editable copy → native widgets; interactive/stateful → iframe.**

---

## 5. MASTER PROMPT (one-shot full build)

Paste this into Claude Code (main session) to run the whole pipeline. Fill the **INPUTS** block.

```
You are building a WordPress page on potomac-laser.com from a Claude Design export, via the Novamira MCP. Follow HANDOFF.md and the memory files potomac-elementor-rebuild and potomac-hubspot-forms exactly. Work from the MAIN session (subagents can't use the MCP). After any Elementor/data change: clear _elementor_css meta for the post and purge WP Rocket (rocket_clean_domain). Use execute-php with str_replace + match-count guards and write a .bak before overwriting any file.

INPUTS
- Design source: <paste the Claude Design export HTML, or the file path>
- Target: <page | post | post_services | post_application>
- Title: <…>   Slug: <…>
- Visibility: <live | draft-hidden-noindex>
- Has interactive cluster (basket/multi-step/drawer)? <yes/no + which sections>
- Has forms that must reach HubSpot? <yes/no + fields>
- Needs UTM/GA4 tracking on forms? <yes/no>

DO, IN ORDER, PAUSING FOR MY OK AFTER STAGE C AND BEFORE GO-LIVE:
A. Prep/discovery — confirm Elementor v3, CPT support, WindPress config state, and list the design's Tailwind tokens/classes used.
B. Ingest & clean the export (decode with json.loads not unicode_escape; unwrap mimecast links; list sections + assets + interactive clusters + forms).
C. WindPress setup — port the design's Tailwind tokens (colors/fonts/radius/shadows) into wp-content/uploads/windpress/data/main.css (Tailwind v4 @theme), ensure content scanning covers Elementor HTML, and verify a test class compiles. STOP and show me a screenshot.
D. Create the post (correct CPT + slug; if hidden, add its ID to snippet #9 + noindex via Rank Math; ensure the CPT is in elementor_cpt_support).
E. Build blocks per §4 (HTML-widget+Tailwind default; native widgets for editable copy; apply the full-bleed treatment snippet #10 to the page). Delete any stale Elementor autosave.
F. Upload assets (create-upload-link → curl PUT to wp-content/uploads/novamira-drafts/…), rewrite src.
G. If interactive: build the standalone HTML file + iframe + bridge (overlay-on-open, auto-height).
H. If forms: wire direct-to-HubSpot (clone/create the HubSpot form via the recipe; map fields to properties; hs_lead_status=NEW; pageName/pageUri from window.parent; file upload via the /wp-json endpoint). Test one submission with a DELIVERABLE email, verify the contact, then archive it.
I. If tracking: inject the analytics module (lead_form_* events, PII-safe, UTM+hutk, direct gtag to the GA4 id with Consent Mode, page from window.parent). Verify events fire to GA4 in the browser network tab.
J. SEO — set title/description/OG via aioseo-edit-post-seo (or Rank Math).
K. QA in Claude-in-Chrome — screenshot each section vs the design; verify widths, colours, fonts, interactive states, and (if forms) a live submission.
L. On my go-live OK: remove from snippet #9, clear noindex, purge cache.

Report after each stage with what changed + IDs + a screenshot.
```

---

## 6. Stages (run individually if you prefer granular control)

Each stage below has a **paste-ready prompt**. They assume the Master Prompt's INPUTS are known.

### Stage A — Prep & discovery
> **Prompt:** `Via Novamira execute-php: confirm Elementor is legacy v3 (atomic OFF), list elementor_cpt_support post types, confirm WindPress active + read wp-content/uploads/windpress/data/main.css (report if empty), and confirm GF+HubSpot, GTM4WP, Rank Math, WP Rocket are active. Then parse my Claude Design export and list: every top-level section, all image/SVG assets, any interactive JS clusters, any forms, and the full set of custom Tailwind classes/tokens the design uses (colors, fonts, radius, shadows, spacing). Don't build yet.`

### Stage B — Ingest & clean the export
> **Prompt:** `Clean the Claude Design export: if it's wrapped in a <script type="__bundler/template"> JSON string, decode with json.loads (NOT unicode_escape — that mojibakes µm/±). Unwrap any mimecastprotect.com/...?domain=X links back to https://X. Save the cleaned HTML to /tmp and give me: section list, asset list, and the <style>/Tailwind config block. Flag any fonts that differ from the site (we standardise on the site font unless I say otherwise).`

### Stage C — WindPress / Tailwind setup ✅ DONE (base config live; only extend per design)
**Base is configured** (2026-06-29). The Goodfellow tokens live in a `brand.css` volume entry (`@theme`), imported by `main.css` (preflight stays commented out so it doesn't reset the theme). Verified: `bg-orange`→#F5821F, `text-navy-mid`→#243854, `rounded-pill`→9999px, `shadow-orange`, `max-w-page`→1224px, `bg-navy-deep`→#152C4A, `font-display`→Inter all compile. WindPress uses a **DOM observer**, so it scans rendered content (Elementor HTML widgets included).

Current `brand.css` `@theme` tokens: `--color-orange #F5821F`, `--color-orange-dark #D96E10`, `--color-navy #1D3557`, `--color-navy-mid #243854`, `--color-navy-deep #152C4A`, `--color-ink #15253D`, `--font-display`/`--font-sans` = Inter, `--radius-pill 9999px`, `--shadow-orange`, `--container-page 1224px`.

> **Per-design extend prompt (run only if a design uses tokens not in `brand.css`):** `Read the WindPress brand.css volume entry via \WindPress\WindPress\Core\Volume::get_entries(). Diff the custom Tailwind classes this design uses against the existing @theme tokens; for any missing ones (new colours, radii, fonts, shadows, container widths, custom utilities) append matching v4 tokens to brand.css and save via Volume::save_entries([...]). Then load a test element in Claude-in-Chrome and confirm the new classes compile (getComputedStyle + check the windpress-cached-inline-css style tag). Do NOT edit wizard.css (Wizard-managed).`

*Caveats:* Tailwind **v4** = CSS-first (`@theme`, no `tailwind.config.js`). The observer scans the **rendered DOM** (Elementor HTML widgets ✅) but **not `<iframe>` documents** — so interactive iframe files (e.g. `cnc-interactive.html`) must keep their own inline/compiled CSS. Save tokens to `brand.css`, never `wizard.css` (the Wizard may overwrite it).

### Stage D — Create the page/post
> **Prompt:** `Create a <page|post|post_services|post_application> titled "<T>" at slug "<S>". Ensure its post type is in elementor_cpt_support (so "Edit with Elementor" works). Set _elementor_edit_mode=builder and an empty _elementor_data to start. If visibility=draft-hidden: add the new post ID to Code Snippet #9's exclusion list and set Rank Math noindex. Return the post ID + permalink.`

### Stage E — Build the blocks
> **Prompt:** `Build the page from the cleaned design, section by section, per HANDOFF §4: default to one Elementor HTML widget per section containing the design's Tailwind markup (WindPress compiles it); use native heading/text-editor/button widgets with Tailwind CSS classes for copy-heavy sections I'll edit often. Wrap each section as outer container content_width:full → inner content_width:boxed. Apply the full-bleed treatment (snippet #10 / body class cnc-elementor-fullbleed) to this post type. After building, delete any stale Elementor autosave (wp_get_post_autosave), clear _elementor_css, purge WP Rocket. Screenshot each section vs the design and list any diffs.`

*Gotchas baked in:* container width control is `width`/`boxed_width` (force with `custom_css selector{width:…!important;flex:0 0 …}` if it doesn't apply); card grids need `flex_align_items:stretch`; if a section wraps everything in one inner container, target `elements[0].elements`.

### Stage F — Assets
> **Prompt:** `For each image/SVG in the design: create-upload-link → curl -X PUT --data-binary @file with the X-Novamira-Upload-Token header to wp-content/uploads/novamira-drafts/, then rewrite the markup src to the uploaded URL. Report the URL map.`

### Stage G — Interactive cluster (only if needed)
> **Prompt:** `Build the interactive cluster as a standalone HTML file in wp-content/uploads/novamira-drafts/<name>.html (self-contained: markup + its own CSS + JS). Embed it in the page as an iframe HTML widget. Add the embed "bridge": auto-height the iframe to content, and while any drawer/overlay/basket is open promote the iframe to a full-viewport fixed overlay (clearing ancestor transforms), reverting on close. Keep this file's Tailwind/CSS compiled or inline (WindPress's page scanner does not see inside iframes). QA that the drawer spans full height and the close control is visible.`

### Stage H — Forms → HubSpot (only if design has forms)
> **Prompt:** `Wire the form(s) direct to HubSpot (portal 143181153) per memory potomac-hubspot-forms. Steps: (1) ensure a HubSpot form exists with all needed fields — clone an existing [Potomac] form via the create_form recipe (unset id; ≤3 fields per fieldGroup; keep configuration/displayOptions/legalConsentOptions), mapping each field name to a contact property ([Potomac]/potomac_* convention); include hidden utm_source/medium/campaign/term/content + hs_lead_status. (2) In the form JS, POST to https://api.hsforms.com/submissions/v3/integration/submit/143181153/<GUID> with fields[] + context{pageName,pageUri FROM window.parent, hutk from hubspotutk cookie}. Send hs_lead_status:'NEW'. (3) File uploads: POST the file to /wp-json/cnc-quote/v1/upload (snippet #12 pattern), take the returned URL, pass it as the file property — HubSpot re-hosts it. (4) In-situ confirmation via a showFormResult(formId, ok, msg) helper (success replaces the form with a thank-you; error/validation = inline banner) — NO alert(). Then submit ONE test with a DELIVERABLE email (NeverBounce blocks @example.com at GF validation but NOT the direct API — still, use a real inbox), verify the contact + properties, and archive it. DO NOT delete any Gravity Form that has a HubSpot feed — it cascades and deletes the linked HubSpot form.`

### Stage I — Analytics / UTM / GA4 (only if forms/tracking)
> **Prompt:** `Add the analytics module to the form JS (per memory potomac-hubspot-forms). Events: lead_form_start, lead_form_field (per field on change/blur), lead_form_submit, lead_form_submit_success, lead_form_submit_error. PII-safe: email/name/phone/free-text send field_filled only (no value); non-PII send field_value. Every event carries utm_source/medium/campaign/term/content (+gclid) read from window.parent URL (persist first/last touch in localStorage) and a page_path param. Push to window.parent.dataLayer AND send via a self-loaded gtag for G-MQSBBH2M4J with send_page_view:false, page_location+page_title from window.parent, and Consent Mode gtag('consent','default',{analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'}). Verify in Claude-in-Chrome network tab that region1.google-analytics.com/g/collect?tid=G-MQSBBH2M4J&en=lead_form_* fires with the parent page in dl/dp/dt. Note the 503s in the automated browser are Google throttling; real users get 204.`

### Stage J — SEO
> **Prompt:** `Set SEO for the post via novamira/aioseo-edit-post-seo (or Rank Math meta): title, meta description, canonical, OG title/description/image. If the page is a hidden draft, keep noindex until go-live.`

### Stage K — QA
> **Prompt:** `QA in Claude-in-Chrome: navigate to the page, and for each section screenshot + compare to the design (widths, colours, fonts, spacing, hover/active states). Verify Tailwind classes actually compiled (getComputedStyle spot-checks, not just screenshots — WP Rocket lazy-load shifts scroll). If forms: run a live submission end-to-end. Report diffs with fixes.`

### Stage L — Go live
> **Prompt:** `Go live: remove this post ID from Code Snippet #9, clear Rank Math noindex, purge WP Rocket + clear _elementor_css. Confirm the page is in nav/listings and indexable, and re-screenshot.`

---

## 7. Open issues / known limitations

1. **WindPress configured ✅** (brand tokens compile). Remaining watch-outs: the observer doesn't scan inside `<iframe>` documents (keep iframe CSS inline/compiled), and add per-design tokens to `brand.css` when a new design introduces classes not yet defined.
2. **Claude can't configure GTM or GA UI** (Google domains blocked). GA4 is fed by **direct gtag**; the parent `dataLayer` events are unused until someone wires GTM triggers/GA4 tags — if they do, **disable the gtag path to avoid double-counting**.
3. **GA4 receipt unverified in-tool** — automated browser gets 503 (Google throttling). Confirm in GA4 **Realtime** (instant) / DebugView (needs the GA Debugger extension or a `?gadebug=1` toggle we haven't added).
4. **Register GA4 custom dimensions** (event-scoped): `form_id`, `field_name`, `field_value`, `fields_completed`, `page_path`, `utm_*`; metric `materials_count`. Reuse an existing event-scoped `form_id` if present. Optionally mark `lead_form_submit_success` a **Key event**.
5. **File-upload staging copies** accumulate in `uploads/cnc-quote-uploads/` (HubSpot re-hosts, so a cron cleanup of files >24h old would be good hygiene — not built yet).
6. **Funnel filename** `cnc-interactive.html` is CNC-specific though its logic is page-agnostic; rename to e.g. `quote-funnel.html` if reusing widely.
7. **CNC page is a hidden draft** (`…-draft-blocks`) — decide go-live / final slug.
8. Minor: reopening the basket after a successful submit shows the thank-you (not a fresh basket); benign `ep.gtm=[object Object]` param from gtag+GTM coexistence.

---

## 8. Next steps

1. **Run Stage C once** to stand up WindPress with the brand tokens → unlocks the faster Tailwind build path for all future pages.
2. Do a **second page end-to-end with the Tailwind-first path** to validate the pipeline (a Services or Applications page) and time it vs the CNC build.
3. Build the **GA4 "submissions by page × form" view** (Exploration or Looker Studio; mark `lead_form_submit_success` as a Key event first).
4. Decide **CNC go-live** (Stage L) + final slug.
5. If routing analytics through GTM long-term, add the GTM triggers/GA4 tags and disable the iframe gtag.
6. Add the **upload-cleanup cron** and (optional) `?gadebug=1` DebugView toggle.

---

## 9. Appendix — conventions & gotchas (carry-over from the CNC build)

**Elementor build recipe:** outer container `content_width:full` (+bg) → inner `content_width:boxed` (snippet caps to 1224). Eyebrow = 28×2px orange bar + uppercase orange heading (11px/700/ls1.5). Colours: navy `#1D3557` (headings), `#243854` (theme text), orange `#F5821F`, body grey `#5F6878` (light)/`#AEB9C7` (dark), borders `#E1E6EE`/`#33445C`. Card grids: `flex_align_items:stretch`. Widget custom CSS: `selector{…}` (Elementor Pro).

**execute-php discipline:** heredoc/nowdoc closing marker at **column 0**; prefer NOWDOC `<<<'X'` for JS/HTML to avoid escaping; every file overwrite writes a `.bak` first; every `str_replace` checks the match count and ABORTS if not exactly as expected.

**Known gotchas:** decode design export with `json.loads` not `unicode_escape` (mojibake); delete stale Elementor autosave (hides sections); add CPT to `elementor_cpt_support` (enables "Edit with Elementor"); Elementor width field may not render → force via `custom_css !important`; the Toggle/FAQ title link defaults to Elementor accent `#6EC1E4` (override to navy); `position:fixed` inside a mid-page iframe is clipped → use the overlay bridge; purge WP Rocket + delete `_elementor_css` after edits (Cloudflare too); GF-form deletion cascades to its linked HubSpot form; HubSpot file property accepts a public URL and re-hosts it; keep PII out of GA4.

**Font:** standardise on the **site font (Inter)** unless the client asks for the design font — set the WindPress `--font-*` tokens accordingly so Tailwind `font-*` classes resolve to it.
