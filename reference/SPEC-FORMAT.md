# spec.yaml — format reference

The build input consumed by the **potomac-elementor** skill (§2 assemble, §3 images,
§4 write). One spec describes one page. The assembler loads each section's fragment from
`reference/snippets/<pattern>.json`, substitutes the tokens, concatenates in spec order,
and writes the result as `_elementor_data`.

Design rule: **the spec is a flat token map, not a layout language.** Every key corresponds
1:1 to a `{token}` that physically exists in a fragment, so assembly is plain string
substitution with no mapping layer to get wrong. Layout lives in the fragments; the spec
only supplies content.

- Working example with every token of all ten patterns: **`reference/spec.example.yaml`**
- Pattern semantics, `Recognise when`, and colour gaps: **`reference/PATTERNS.md`**
- Token → original copy for any slot: **`reference/snippets/<pattern>.legend.json`**

## Top level

```yaml
spec_version: 1          # int, required. Bump on breaking format changes.
page:      { ... }       # required, one page per spec
assets:    { ... }       # required only if a section uses image tokens
sections:  [ ... ]       # required, ordered — render order is spec order
```

### `page`

| Key | Type | Required | Notes |
|---|---|---|---|
| `title` | string | yes | Post title |
| `slug` | string | yes | `post_name`; also the `built/<slug>.json` filename. Automation runs namespace it `pl-auto-<slug>` (AUDIT.md B5) and `--automation` enforces that |
| `post_type` | string | yes | **`page` or `post_services` only** — SKILL.md §1. A service page is `post_services` (that is what its live counterparts are, and what puts it under `/services/`); everything else is `page` |
| `post_status` | string | yes | **`draft` only** — the agent never publishes (§1, §8) |

### `assets`

Media referenced by `image_*` tokens. Keys are arbitrary but must be unique.

```yaml
assets:
  eco_logo_1:
    attachment_id: 41822                     # int, required, non-zero
    url: "https://…/pl-auto-eco-logo-1.png"  # string, required, production URL
```

Both fields are mandatory: §3 sets `image.url` **and** `image.id`, and its gate rejects any
image widget with a missing id. Uploads carry the `pl-auto-` filename prefix so automation
uploads stay identifiable in the media library.

### `sections[]`

```yaml
sections:
  - pattern: hero-dark-stat-strip   # string, required, must match a fragment filename
    tokens:  { ... }                # map, required
    options: { ... }                # map, only for the two patterns listed below
```

`pattern` must be one of the ten in `PATTERNS.md`. A pattern may repeat within a page, and
a page may use any subset — only `hero-dark-stat-strip` first and `cta-band-dark` last are
conventions rather than rules.

## Token values

Key = token name without braces (`heading_1`, not `{heading_1}`). Value type depends on the
prefix:

| Prefix | Value | Notes |
|---|---|---|
| `heading_n` | string | Plain text. Elementor `heading` widget `title`. |
| `body_n` | string | **HTML** — `<p>`, `<ul>`, `<strong>` all render. Fills `text-editor`. |
| `button_n` | string | Button label |
| `url_n` | string | Href — path (`/contact/`), anchor (`#quote`), or absolute URL |
| `image_n` | `{ asset: <key> }` | Reference into `assets`, never an inline URL |
| `embed_n` | string | Raw markup (the `<iframe>` for `interactive-iframe-embed`) |
| `faq_q_n` | string | Accordion question (plain text) |
| `faq_a_n` | string | Accordion answer (**HTML**) |

Numbering is per-section, in document order — `heading_4` of section 2 is unrelated to
`heading_4` of section 5. Never guess what a slot is for: read the matching
`legend.json`, which records the copy each token replaced (SKILL.md §8).

## Token counts per pattern

Exact, generated from the fragments. A spec section must supply **every** token its
pattern declares — a missing key leaves a literal `{token}` on the page, which §2's gate
rejects.

| Pattern | Total | heading | body | button | url | image | embed | faq_q/faq_a |
|---|---|---|---|---|---|---|---|---|
| `hero-dark-stat-strip` | 19 | 12 | 3 | 2 | 2 | – | – | – |
| `why-choose-inset-cta` | 10 | 3 | 3 | 2 | 2 | – | – | – |
| `interactive-iframe-embed` | 1 | – | – | – | – | – | 1 | – |
| `spec-table-dark` | 23 | 12 | 11 | – | – | – | – | – |
| `process-comparison-cards` | 29 | 12 | 13 | 2 | 2 | – | – | – |
| `process-steps-numbered` | 24 | 17 | 7 | – | – | – | – | – |
| `group-ecosystem-cards` | 23 | 7 | 10 | 1 | 1 | 4 | – | – |
| `testimonials-avatar-cards` | 17 | 14 | 3 | – | – | – | – | – |
| `faq-toggle` | 21 | 2 | 1 | 1 | 1 | – | – | 8 / 8 |
| `cta-band-dark` | 7 | 2 | 1 | 2 | 2 | – | – | – |

Total across all ten: **174**.

## `options` — the two non-copy obligations

Most of SKILL.md §5 is satisfied by filling tokens correctly. Two obligations are
**structural** — they move or restyle a widget, so they cannot be expressed as a token value
and the assembler must act on them:

```yaml
  - pattern: group-ecosystem-cards
    options:
      you_are_here_unit: 2    # 1-based unit index; badge widget moves to that card,
                              # and only that card keeps the button (others use text links)

  - pattern: process-steps-numbered
    options:
      highlight_step: 3       # 1-based step index; that card gets #FFF7EF bg / #C2691A text
```

Omitting `options` leaves the fragment's source-page arrangement in place — which is wrong
for any page that isn't the CNC original. Treat both as required for those two patterns.

## Constraints a spec must satisfy

These are the §5 obligations expressed against the real token names, so they can be checked
mechanically before any write.

**`process-comparison-cards` — mirrored card titles.** Each card title exists in two heading
widgets (one is the mobile/hover label). Both must be filled *identically*:

| Card | Tokens that must match |
|---|---|
| 1 | `heading_3` == `heading_4` |
| 2 | `heading_6` == `heading_7` |
| 3 | `heading_9` == `heading_10` |

`heading_12` is not card content — it is the closing "Have a part in mind?" line below the
three cards.

**`testimonials-avatar-cards` — derived initials.** The navy circle must carry initials
derived from the adjacent author name, never the source page's:

| Initials token | Derived from |
|---|---|
| `heading_4` | `heading_5` |
| `heading_8` | `heading_9` |
| `heading_12` | `heading_13` |

**`hero-dark-stat-strip` — stat pairs.** `heading_3..12` are five value/caption pairs
(`heading_3`+`heading_4`, `heading_5`+`heading_6`, …). Changing the stat count is a
structural edit — add or remove sibling containers **in pairs only**.

**`process-steps-numbered` — step triples.** `heading_3..17` are five number/stage/title
triples (`03`/`ENGINEERING`/`Engineering Review`). Keep the two-digit numbering sequential.

**`spec-table-dark` — label/value rows.** `body_1` is the disclaimer caption under the H2.
`heading_3..10` are eight spec labels, each paired with `body_2..9` as its value
(`heading_3`↔`body_2`, `heading_4`↔`body_3`, … `heading_10`↔`body_9`) — keep label and value
in step when adding or removing a row. The trailing highlighted sub-block is
`body_10` + `heading_11` + `heading_12` + `body_11`.

**`faq-toggle` — lockstep repeater.** `faq_q_n` and `faq_a_n` must be added and removed
together. The `tabs[]` count is free, unlike the fixed-arity patterns.

**`cta-band-dark` — leave `#46587010` literal.** 8-digit hex with alpha; Elementor globals
cannot express it.

**`why-choose-inset-cta`** has no extra constraints, but its empty first column is a layout
spacer — the assembler must not prune it as an empty container.

**`interactive-iframe-embed`** — `embed_1`'s iframe `src` points at the uploaded
`<slug-prefix>-interactive.html` under `novamira-drafts/`, with frame id
`<slug-prefix>-interactive-frame`. The file ships its own CSS/JS; nothing compiles inside an
iframe, so never inject styles into it.

## Validation before writing

Run the checker — it implements every check below and exits non-zero on any error:

```bash
tools/validate_spec.py path/to/spec.yaml              # strict: use before a build
tools/validate_spec.py path/to/spec.yaml --automation  # + require the pl-auto- slug namespace
tools/validate_spec.py reference/spec.example.yaml --template
```

`--template` downgrades empty token values and placeholder `attachment_id: 0` to warnings,
for checking a skeleton rather than a buildable spec. Requires PyYAML. Warnings never fail
the run; errors mean **do not write to WordPress** (SKILL.md §2, §8).

Checks that must pass locally, before any WordPress call (SKILL.md §2, §3):

1. YAML parses; `spec_version` is 1.
2. `page.post_type` is `page` or `post_services`, and `page.post_status == draft`. Under
   `--automation`, `page.slug` also starts with `pl-auto-`.
3. Every `sections[].pattern` resolves to an existing `reference/snippets/<pattern>.json`.
4. **Token coverage both ways** — for each section, the set of `{token}`s in the fragment
   equals the set of keys in `tokens`. A fragment token with no spec key ships a literal
   `{token}`; a spec key with no fragment token is silently dropped, meaning copy the author
   wrote never appears.
5. No token value itself contains `{…}` token syntax.
6. Every `image_*` value resolves to an `assets` entry with a non-zero `attachment_id` and a
   non-empty `url`.
7. The mirrored-title and derived-initials constraints above hold.
8. `options` present for `group-ecosystem-cards` and `process-steps-numbered`, with indices
   in range.

`reference/spec.example.yaml` passes 1–6 and 8 by construction; its token values are empty
placeholders, so it is a template, not a buildable spec.

## Worked minimal example

A two-section page:

```yaml
spec_version: 1

page:
  title: "Laser Welding Services"
  slug: "laser-welding-services"
  post_type: page
  post_status: draft

sections:
  - pattern: faq-toggle
    tokens:
      heading_1: "FAQ"
      heading_2: "Common questions"
      body_1: "<p>Direct answers to the engineering questions buyers ask.</p>"
      button_1: "Ask a Technical Question"
      url_1: "/contact/"
      faq_q_1: "What tolerances can you hold?"
      faq_a_1: "<p>Typically ±10 µm in plastics.</p>"
      # … faq_q_2..8 / faq_a_2..8

  - pattern: cta-band-dark
    tokens:
      heading_1: "GET STARTED TODAY"
      heading_2: "Ready to weld at the micron scale?"
      body_1: "<p>Share your CAD files and tolerance requirements.</p>"
      button_1: "Request a Quote"
      button_2: "Upload CAD"
      url_1: "#quote"
      url_2: "#quote"
```
