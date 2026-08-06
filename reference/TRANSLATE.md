# TRANSLATE — design → spec.yaml

The intake step for the **potomac-elementor** skill. TRANSLATE turns a Claude Design page
into a validated `spec.yaml`. It runs **entirely before** SKILL.md §0 and touches nothing on
production: its only output is a local file.

```
design export ──▶ decode ──▶ segment ──▶ MATCH ──▶ extract ──▶ spec.yaml ──▶ validate ──▶ §0
                                          │
                                    PATTERNS.md
                                   "Recognise when"
```

Hard rule: **TRANSLATE never invents layout.** Every section of the output maps to one of the
ten fragments in `reference/snippets/`. A design section that matches nothing stops the
translate — see [§5 No match](#5-no-match). Hand-building section JSON is forbidden
(SKILL.md §8).

---

## 1. Acquire the design source

In preference order:

1. **Pasted export or file path.** The original HANDOFF intake, with no size ceiling. Ask for
   `<page>.html` from the Claude Design project, or for the specific sections needed.
2. **Chrome RPC route.** Reliable for the full file. Chrome must be signed into the **work**
   account (`ben.merrell@goodfellow.com`) — a personal login returns
   `404 project not found`. Verify with `fetch('/api/organizations')`; you want org
   `bb2e2ffa-2867-4856-8025-23d4b16022ff` "Goodfellow Group". Then on any
   `claude.ai/design/...` tab:

   ```
   POST https://claude.ai/design/anthropic.omelette.api.v1alpha.OmeletteService/GetFile
   headers: content-type: application/json, connect-protocol-version: 1
   body:    {"projectId":"1948b4a2-8c1d-43a1-9d9d-de121879a668","path":"<Page>.html"}
   ```

   Returns `{content: <base64>}`. Decode with `atob` + `TextDecoder`, stash on
   `window.__SRC`, then render the slice you want into a `<pre>` and read it with
   `get_page_text` — `javascript_tool` truncates results at ~1 KB, so never return the text
   directly.
3. **DesignSync `get_file` — expect it to fail.** It truncates at 256 KiB and the page files
   are ~1 MB (inline base64 images). The readable head covers hero, why-us and the start of
   services; **applications, capabilities, process, FAQ, quote and final CTA are past the
   cut** — which is most of what TRANSLATE needs. Never *write* through DesignSync from a
   truncated read: it sends the whole file and would delete the tail from the design.

## 2. Decode and clean

- **Standalone export** wraps the page in `<script type="__bundler/template">` holding a
  quoted JSON string. Decode with `json.loads(raw)`. **Not** `unicode_escape` — that
  double-encodes and turns `µm`/`±` into `Âµ`/`Â±` mojibake, which then ships to the page.
- **Unwrap mail-scanner links:** `mimecastprotect.com/...?domain=X` → `https://X`.
- **Note inline base64 images** and set them aside as assets (§7). Don't carry them into the
  spec; the spec references uploaded media by attachment id.
- **STRIP DESIGN-TIME SCAFFOLDING.** A Claude Design export carries tooling that must never
  reach a live page. In this corpus every service page loads all four:
  `cdn.tailwindcss.com` (the Tailwind Play CDN — on WP, WindPress compiles instead),
  `unpkg.com/react@…/react.development.js` and `react-dom.development.js` (**dev** builds),
  `@babel/standalone`, and a `tweaks-panel.jsx` design widget with its `tweaks-root` mount.
  Remove all of it, plus any other `<script src>`/`<link rel=stylesheet>` pointing off-site.
  Nothing in the fragment library needs an external asset, so anything left is scaffolding.
  SKILL.md §2 gates this and `tools/validate_spec.py` rejects it in a token value.
- Sanity-check a few `µ`/`±`/`→` characters survived before going further.

## 3. Segment

Split the cleaned markup into top-level sections in document order. Record for each: its
position, its heading text, its background tone (light/dark), and whether it contains a card
grid, an accordion, an image set, or a bespoke interactive cluster. This list is the input to
matching — one design section becomes at most one spec section.

## 4. MATCH — the core step

For each design section, read the **`Recognise when`** field of every entry in
`reference/PATTERNS.md` and pick the one it satisfies. That field is the matcher; it is
written to be discriminating, so match against it rather than against a pattern's name.

Quick signal table (the full text in `PATTERNS.md` is authoritative):

| Signal in the design | Pattern |
|---|---|
| Opening section, dark navy, H1 + 2 CTAs + rule + big-number stat row | `hero-dark-stat-strip` |
| White 2-col value proposition, copy column ends in a tinted inset CTA card | `why-choose-inset-cta` |
| One self-contained interactive app (configurator/calculator/basket) | `interactive-iframe-embed` |
| Dark block, label/value spec rows stacked on lighter cards | `spec-table-dark` |
| "X vs Y vs Z" cards, each with "Best when you need:" + a "See … →" link | `process-comparison-cards` |
| Numbered workflow cards (`01`…`05`), one tinted orange | `process-steps-numbered` |
| Mid-navy, sibling business units with logos + a "You are here" badge | `group-ecosystem-cards` |
| Light grey, quote cards with stars + initials avatar | `testimonials-avatar-cards` |
| Accordion of questions | `faq-toggle` |
| Closing dark band: heading + one paragraph + exactly two buttons | `cta-band-dark` |

**Tie-breakers** for the three-card patterns, which are the easiest to confuse:

- `testimonials-avatar-cards` has an eyebrow + H2 and **no intro paragraph** — that absence
  is the discriminator.
- `process-comparison-cards` has the literal sub-heading "Best when you need:" in every card
  and a closing "Have a part in mind?" line *below* the cards.
- `process-steps-numbered` leads each card with a two-digit number.
- `group-ecosystem-cards` is the only three-plus-card pattern with an image per card.

Record the match decisions as comments at the top of the emitted `spec.yaml` — design section
index, chosen pattern, and the signal that decided it. That makes the translate auditable
when a page later looks wrong.

## 5. No match

If a design section satisfies no `Recognise when`:

1. Re-read the candidates — check it isn't a known pattern with different copy.
2. Check whether it belongs in an iframe instead (bespoke JS/interactivity →
   `interactive-iframe-embed` plus a separate uploaded file).
3. Otherwise **stop and report**. Do not approximate with a near-miss pattern, and do not
   hand-build JSON (SKILL.md §8). A genuinely new section type means extending the fragment
   library first — a separate job with its own extraction and `PATTERNS.md` entry.

   **Exception:** when translate is running inside the page-sync automation, that "separate job"
   is `AUTOMATION.md` §7 (EXTEND), which does it in-run under its own gates — see the carve-out at
   the foot of SKILL.md §8. A human-run translate still stops and reports.

Note `spec-table-dark` exists only on post 12133; the clone chain dropped it. Take it from
the library, never from the page being cloned.

## 6. Extract copy into tokens

For each matched section, open `reference/snippets/<pattern>.legend.json` and fill each token
from the design's corresponding slot. **Never fill a token without reading its legend entry**
(SKILL.md §8) — the legend records what that slot held on the source page, which is the only
way to know a slot's role. `heading_4` means nothing on its own.

Then apply:

- **Brand normalisation (standing policy).** Designs say "Potomac" / "Potomac Photonics";
  the built pages say **"Goodfellow Microfabrication"**. Swap throughout, questions as well
  as answers. **Never** touch "**Goodfellow's** ISO 17025-accredited materials testing
  division" — that names the materials arm, not the microfabrication brand.
- **HTML vs plain text.** `body_*` and `faq_a_*` render as HTML; `heading_*`, `button_*` and
  `faq_q_*` render literally. Markup in a plain slot shows up as visible angle brackets.
- **Line breaks in headings.** Hero H1s use `<br>`. Keep them — they are deliberate.

### Fixed arity — where translate most often breaks

Each fragment carries a fixed number of repeating units, and **the spec must supply exactly
that many** — `tools/validate_spec.py` compares the token set both ways, so omitting a pair
ships a literal `{token}` and adding one silently drops the copy. Either way the gate fails.

`faq-toggle` is the sole exception: its `tabs[]` is a real repeater, so the count is free.

Everywhere else a count mismatch is a **structural** difference, not a token difference. Do not
juggle tokens to absorb it. Flag it, and take one of two routes: drop the surplus copy
deliberately and say so in the report, or treat the section as a new pattern via
`AUTOMATION.md` §7, which is the only path that may change a fragment's shape. Never silently
discard design copy.

| Pattern | Repeating unit | Count in fragment |
|---|---|---|
| `hero-dark-stat-strip` | stat value/caption pairs | 5 (add/remove **in pairs**) |
| `spec-table-dark` | label/value rows | 8 |
| `process-comparison-cards` | cards | 3 |
| `process-steps-numbered` | steps | 5 |
| `group-ecosystem-cards` | units | 4 |
| `testimonials-avatar-cards` | quotes | 3 |
| `cta-band-dark` | buttons | 2 |
| `faq-toggle` | q/a items | 8 shipped, but a **repeater — count is free** |

`faq-toggle` is the only pattern where the count varies freely; everywhere else a mismatch
needs a decision.

## 7. Assets

- Collect every image the matched sections need. Each becomes an `assets` entry with a real
  `attachment_id` **and** production `url` (SKILL.md §3 gate rejects a missing id).
- Uploads take the `pl-auto-` filename prefix.
- `group-ecosystem-cards` needs four logos (`eco-logo-1..4`).
- If the design has a bespoke interactive cluster, it ships as
  `<slug-prefix>-interactive.html` under `novamira-drafts/`, referenced by `embed_1` with
  frame id `<slug-prefix>-interactive-frame`. That file carries its own CSS/JS — **nothing
  compiles inside an iframe**, so Tailwind classes will not resolve there and styles must
  never be injected into it.

## 8. Structural options

Two obligations are not copy and must be decided from the design (see `SPEC-FORMAT.md`):

- `group-ecosystem-cards.options.you_are_here_unit` — the unit **this** page represents.
  Inheriting the source page's badge is a visible error.
- `process-steps-numbered.options.highlight_step` — the step the design tints orange
  (default 3, engineering review).

## 9. Emit and validate

Write `spec.yaml` per `reference/SPEC-FORMAT.md` — starting from
`reference/spec.example.yaml`, which already carries every token of all ten patterns with the
source copy in comments, so deleting the sections this page doesn't use is safer than typing
token names by hand. Then:

```bash
tools/validate_spec.py path/to/spec.yaml
```

**A clean pass is the exit condition for TRANSLATE.** The validator catches the two silent
failures that otherwise reach the page: a fragment token with no spec key ships a literal
`{token}`, and a spec key with no fragment slot throws away copy you just extracted. It also
enforces mirrored card titles, initials derived from the adjacent name, and the structural
options.

## 10. Surface the proposal

TRANSLATE output is a proposal, and it must always be surfaced — what differs is *to whom*.

- **Automation run** (`AUTOMATION.md`): there is no human in the loop, so the match table goes
  into the run report and the build continues. The report is the review, after the fact, and
  the drafts it produces are unpublished until a human says otherwise.
- **Human run:** stop here and get sign-off before starting §0.

Either way, surface:

- the match table (design section → pattern → deciding signal)
- any arity mismatches and what was decided
- any copy that was normalised or dropped
- the asset list, with ids not yet uploaded marked as such

Then start SKILL.md §0. TRANSLATE writes nothing to WordPress, so it is always safe to re-run.
