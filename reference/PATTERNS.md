# Elementor Section Patterns — Potomac Laser / Goodfellow

Reusable section patterns extracted from the built `post_services` pages.
The **TRANSLATE** step matches a design's sections against the *Recognise when*
field below, then loads the matching fragment from `reference/snippets/<id>.json`
and swaps the `{placeholder}` tokens for the new page's copy.

> **Format note:** no canonical template was available when this file was written,
> so the entry format below was designed to fit the pipeline. If you have the real
> template, replace the block below and the entries will need reformatting to match.

## Entry template

```
### <id>
| | |
|---|---|
| **Snippet** | `reference/snippets/<id>.json` |
| **Source** | post `<post_id>` (`<slug>`) section index `<n>` |
| **Used by** | <which pages carry this pattern, and at which section index> |
| **Signature** | `<structural hash>` · `<n>` widgets · `<bytes>` bytes |
| **Recognise when** | <what a design section must look like for TRANSLATE to pick this> |
| **Structure** | <container nesting + widget order> |
| **Tokens** | <count> placeholders: <list> |
| **Globals** | <n> native `__globals__` refs · <n> `var(--e-global-color-*)` rewrites |
| **Unmapped colours** | <hexes with no Kit token, left hardcoded> |
| **Notes** | <gotchas, variants, dependencies> |
```

## Provenance

All fragments were extracted from post **12133** (`services/cnc-micromachining-services-draft-blocks`),
which is the origin page of the clone chain and the only page containing all 10 patterns.

Structural fingerprinting of every `draft-blocks` page proved the rest add nothing:

| Post | Slug | Sections | Distinct patterns contributed |
|---|---|---|---|
| 12133 | `cnc-micromachining-services-draft-blocks` | 10 | **all 10** |
| 12223 | `3d-printing-contract-services-draft-blocks` | 9 | 0 (subset of 12133) |
| 12224 | `rapid-prototyping-services-draft-blocks` | 9 | 0 (identical to 12223) |
| 12225 | `laser-micro-hole-drilling-services-draft-blocks` | 9 | 0 (identical to 12223) |
| 12226 | `laser-micromachining-services-draft-blocks` | 9 | 0 (identical to 12223) |

12223–12226 share the same 9 section hashes in the same order *and* the same
distinct-colour set — they are copy-swaps, not structural variants. `spec-table-dark`
is the only pattern unique to 12133.

Fingerprinting all **46** sections across the five pages resolved every one to a
pattern below — there are no unclassified sections, so these 10 patterns are complete
coverage of the `draft-blocks` set.

## Page coverage

Cell = the section index that pattern occupies on that page. The clone chain simply
omits `spec-table-dark`, which shifts every later section up by one.

| Pattern | 12133 CNC | 12223 3DP | 12224 RP | 12225 MHD | 12226 LM |
|---|---|---|---|---|---|
| `hero-dark-stat-strip` | 0 | 0 | 0 | 0 | 0 |
| `why-choose-inset-cta` | 1 | 1 | 1 | 1 | 1 |
| `interactive-iframe-embed` | 2 | 2 | 2 | 2 | 2 |
| `spec-table-dark` | 3 | — | — | — | — |
| `process-comparison-cards` | 4 | 3 | 3 | 3 | 3 |
| `process-steps-numbered` | 5 | 4 | 4 | 4 | 4 |
| `group-ecosystem-cards` | 6 | 5 | 5 | 5 | 5 |
| `testimonials-avatar-cards` | 7 | 6 | 6 | 6 | 6 |
| `faq-toggle` | 8 | 7 | 7 | 7 | 7 |
| `cta-band-dark` | 9 | 8 | 8 | 8 | 8 |

## Per-page variants

What actually differs between the five pages is copy, the iframe target and the
comparison triad. All five share the same button targets (`#quote`, `/contact/`) and
the same `group-ecosystem-cards` / `testimonials-avatar-cards` / `faq-toggle` framing
copy. ` / ` marks a `<br>` line break in the H1.

| | 12133 | 12223 | 12224 | 12225 | 12226 |
|---|---|---|---|---|---|
| **Slug** | `cnc-micromachining-services-draft-blocks` | `3d-printing-contract-services-draft-blocks` | `rapid-prototyping-services-draft-blocks` | `laser-micro-hole-drilling-services-draft-blocks` | `laser-micromachining-services-draft-blocks` |
| **Sections** | 10 | 9 | 9 | 9 | 9 |
| **Hero eyebrow** | CNC MICROMACHINING SERVICES | 3D PRINTING CONTRACT SERVICES | RAPID PROTOTYPING SERVICES | LASER MICRO-HOLE DRILLING SERVICES | LASER MICROMACHINING SERVICES |
| **Hero H1** | CNC Micromachining at ±10 µm Tolerances. | Micro 3D Printing, / from Concept to / Production. | High-Precision / Rapid Prototyping / in Days. | Laser Micro-Hole / Drilling from 2 µm / Diameters. | Precision / Laser Micromachining / at the Micro Scale. |
| **Iframe file** | `cnc-interactive.html` | `3dp-interactive.html` | `rp-interactive.html` | `mhd-interactive.html` | `lm-interactive.html` |
| **Comparison triad** | CNC vs. Laser vs. Conventional Machining | 3D Printing vs. Micro-CNC vs. Laser | Micro 3D Printing vs. Micro-CNC vs. Laser | UV Laser vs. IR Laser vs. Micro-CNC Drilling | Laser vs. Micro-CNC vs. Micro 3D Printing |
| **Process heading** | Our Micro-CNC Process | Our Micro 3D Printing Process | Our Rapid Prototyping Process | Our Micro-Hole Drilling Process | Our Laser Micromachining Process |
| **Closing CTA** | Ready to machine at the micron scale? | Ready to build at the micron scale? | Ready to prototype at the micron scale? | Ready to drill at the micron scale? | Ready to laser micromachine your next part? |

Notes when adding the next page in the chain:

- **`spec-table-dark` is missing from every clone.** If a new services page needs a
  technical-spec block, take it from this library rather than the page you clone.
- **The duplicate comparison triad on 12224/12226 was resolved on 12224** (2026-08-05).
  Both pages had read "Laser vs. Micro-CNC vs. Micro 3D Printing". 12226 keeps it —
  leading with its own service is the convention every other page follows. On 12224
  the three cards were reordered to Micro 3D Printing → Micro-CNC → Laser and the H2
  rebuilt from the existing card titles, so no copy was invented. Each card's bullets
  and "See … →" link travelled with its own card; the section has no `nth-child`-style
  CSS, so the reorder is presentation-safe. Backup:
  `uploads/novamira-drafts/backups/elementor-12224.bak-pretriad-20260805-210650.json`
  (86,937 bytes, sha256 `0378e81c…`). Only section 3 changed.
- **Still open on 12226:** its intro reads "Choose the right **prototyping** process for
  your part", inherited from 12224 — wrong framing for a laser micromachining page.
  Left as-is pending the design file; fixing it needs the intended copy, not a guess.
- Iframes follow `<prefix>-interactive.html` in `uploads/novamira-drafts/`, with frame
  ids `<prefix>-interactive-frame`. The file is **not** part of the fragment.
- The closing CTA verb is the only copy that tracks the service; everything else in
  `cta-band-dark` is boilerplate.

## Placeholder vocabulary

| Token | Replaces |
|---|---|
| `{heading_n}` | `heading` widget `title` |
| `{body_n}` | `text-editor` widget `editor` (HTML copy) |
| `{button_n}` | `button` widget `text` |
| `{url_n}` | any widget's `link.url` |
| `{image_n}` | `image` widget `image.url` (`image.id` blanked — re-attach on build) |
| `{embed_n}` | `html` widget raw markup |
| `{faq_q_n}` / `{faq_a_n}` | `toggle` repeater `tab_title` / `tab_content` |

Numbering is per-fragment, in document order. Each fragment has a sibling
`<id>.legend.json` mapping every token to the original copy it replaced, so you can
see the intent of a slot without opening the source page.

## Kit global tokens (Kit 11259, "Default Kit")

| Token id | Hex | Title |
|---|---|---|
| `gforange` | `#F5821F` | GF Orange |
| `gforangedk` | `#D96E10` | GF Orange Dark |
| `gfnavy` | `#15253D` | GF Navy (headings) |
| `gfnavymid` | `#1D3557` | GF Navy Mid |
| `gfnavydp` | `#0D1B2A` | GF Navy Deep |
| `gfbody` | `#6B7280` | GF Body Gray |
| `gfink` | `#3C4858` | GF Ink |
| `gfwhite` | `#FFFFFF` | GF On-Dark White |
| `gfblue` | `#1A71AB` | GF Accent Blue |

The Kit defines **no** `system_colors` and **no** typography globals
(`system_typography` and `custom_typography` are both empty), so no snippet can
reference a global font — all typography in these fragments is per-widget.

**Audit result:** the live pages reference **zero** globals (`__globals__` is absent
throughout) and carry 263 hardcoded hex values on 12133 / 216 on each clone.
In the saved fragments, every value matching one of the 6 usable Kit colours was
converted — **116** native `__globals__` refs plus **17** `var(--e-global-color-*)`
rewrites inside `custom_css`/`html`. `gforangedk`, `gfink` and `gfblue` are never
used by these sections. The remaining ~38 colours have no Kit equivalent and are
listed per entry, and consolidated under [Unmapped colours](#unmapped-colours).

---

# Patterns

### hero-dark-stat-strip
| | |
|---|---|
| **Snippet** | `reference/snippets/hero-dark-stat-strip.json` |
| **Source** | post `12133` section index `0` |
| **Used by** | all 5 pages (12133, 12223, 12224, 12225, 12226) at index 0 |
| **Signature** | `d76ec95c1d` · 18 widgets · 38,262 bytes |
| **Recognise when** | The page's opening section, on a dark navy background, with a small uppercase eyebrow label, one large H1, an intro paragraph, **two** CTA buttons plus a tertiary text link, and — below a horizontal rule — a row of 5 big-number statistics (value + uppercase caption). |
| **Structure** | `container:full bg=gfnavydp` → boxed → eyebrow (orange 28×2 bar + uppercase heading) → H1 → intro `text-editor` → button pair → text link → supporting note → `divider` → 5-up stat row (`heading` value + `heading` caption each) |
| **Tokens** | 19: `{heading_1..12}`, `{body_1..3}`, `{button_1..2}`, `{url_1..2}` |
| **Globals** | 14 native · 1 CSS-var rewrite |
| **Unmapped colours** | `#1A2F4A` (gradient stop b), `#B6C0CC`, `#3A4A60`, `#8A97A6`, `#2A3A52` |
| **Notes** | Background is a gradient: `background_color` → `gfnavydp` global, but `background_color_b` `#1A2F4A` has no token. `{heading_1}` is the eyebrow, `{heading_2}` the H1; `{heading_3..12}` are the 5 stat value/caption pairs (`±10µm`/`TOLERANCE`, `100µm`/`MIN FEATURE`, `4-Axis`/`CNC CAPABILITY`, `24h`/`RAPID RESPONSE`, `1982`/`EST.`) — add/remove sibling containers in pairs to change the count. |

### why-choose-inset-cta
| | |
|---|---|
| **Snippet** | `reference/snippets/why-choose-inset-cta.json` |
| **Source** | post `12133` section index `1` |
| **Used by** | all 5 pages at index 1 |
| **Signature** | `739b2ea6f0` · 8 widgets · 25,476 bytes |
| **Recognise when** | A white two-column "why choose us" / value-proposition section where one column holds the copy (eyebrow + H2 + two paragraphs) and the copy column ends in a **tinted inset card** containing a short heading and a duplicate of the hero's two CTA buttons. |
| **Structure** | `container:full bg=gfwhite` → boxed → row → \[empty media column] + copy column (eyebrow → H2 → 2× `text-editor` → inset `container bg=#F9FAFB` with `heading` + button pair + note) |
| **Tokens** | 10: `{heading_1..3}`, `{body_1..3}`, `{button_1..2}`, `{url_1..2}` |
| **Globals** | 9 native · 1 CSS-var rewrite |
| **Unmapped colours** | `#ECEEF2`, `#5F6878`, `#F9FAFB` (inset card bg), `#E5E7EB`, `#737C8D` |
| **Notes** | The first column is an empty container in the source — it is a layout spacer, not a dropped image. Keep it or the copy column loses its offset. |

### interactive-iframe-embed
| | |
|---|---|
| **Snippet** | `reference/snippets/interactive-iframe-embed.json` |
| **Source** | post `12133` section index `2` |
| **Used by** | all 5 pages at index 2 — different embed file per page |
| **Signature** | `31273e25fe` · 1 widget · 602 bytes |
| **Recognise when** | A section whose entire content is one self-contained interactive app (configurator, calculator, quote basket) that ships its own CSS/JS — i.e. the design has a block you cannot express as native widgets. |
| **Structure** | `container:full` → single `html` widget holding one `<iframe>` |
| **Tokens** | 1: `{embed_1}` |
| **Globals** | 0 · 0 |
| **Unmapped colours** | none |
| **Notes** | WindPress's DOM observer **does not scan inside iframe documents**, so the embedded file must carry its own compiled/inline CSS — Tailwind classes will not compile for it. Iframe ids follow `<prefix>-interactive-frame`. The iframe target is a separate uploaded HTML file, not part of this fragment. |

### spec-table-dark
| | |
|---|---|
| **Snippet** | `reference/snippets/spec-table-dark.json` |
| **Source** | post `12133` section index `3` |
| **Used by** | **12133 only** — absent from 12223–12226 |
| **Signature** | `e547f8eed4` · 23 widgets · 57,907 bytes |
| **Recognise when** | A dark technical-specification block: eyebrow + H2 + a short disclaimer caption, followed by a vertical stack of **label / value rows** on slightly lighter cards — one row per spec (tolerance, min feature, axis capability, materials…) — optionally closing with a highlighted sub-block. |
| **Structure** | `container:full bg=#182336` → boxed row → eyebrow → H2 → caption → 8 × `container bg=#1E2D45` rows, each `heading` (label) + `text-editor` (value) → trailing `MATERIAL SUPPORT` sub-block |
| **Tokens** | 23: `{heading_1..12}`, `{body_1..11}` |
| **Globals** | 5 native · 0 CSS-var rewrites |
| **Unmapped colours** | `#182336`, `#1D2C42`, `#22334B`, `#9FB0C0`, `#1E2D45`, `#33445C`, `#E8EDF3`, `#AEB9C7`, `#8FA0B2`, `#3A4A60` |
| **Notes** | **Unique to 12133** — the clone chain dropped it. Lowest global coverage of any pattern (5 refs vs 10 orphan colours): this section's dark palette (`#182336`, `#1E2D45`) is a near-miss for `gfnavy`/`gfnavydp` but matches neither, so it is the strongest candidate for Kit consolidation. Row count is data-driven — repeat the row container per spec. |

### process-comparison-cards
| | |
|---|---|
| **Snippet** | `reference/snippets/process-comparison-cards.json` |
| **Source** | post `12133` section index `4` |
| **Used by** | all 5 pages — index 4 on 12133, index 3 on 12223–12226 |
| **Signature** | `748b912a7c` · 27 widgets · 54,733 bytes |
| **Recognise when** | An "X vs Y vs Z" process/option comparison on white: eyebrow + H2 + intro, then a lead paragraph, then **3 peer cards** that each repeat their own title, a "Best when you need:" sub-heading, a bulleted capability paragraph, a tolerance/spec line, and a "See … →" text link. |
| **Structure** | `container:full bg=gfwhite` → boxed → eyebrow → H2 → intro → lead `text-editor` → row of 3 `container` cards (`heading` title ×2 → `heading` "Best when you need:" → `text-editor` bullets → `text-editor` spec → `text-editor` link) |
| **Tokens** | 29: `{heading_1..12}`, `{body_1..13}`, `{button_1..2}`, `{url_1..2}` — `{heading_12}` is a closing "Have a part in mind?" line below the 3 cards, not card content |
| **Globals** | 14 native · **9** CSS-var rewrites |
| **Unmapped colours** | `#5F6878`, `#1B2434`, `#223248`, `#1D2C42`, `#E0E4EA`, `#6BD0E3`, `#EAEDF1`, `#E8EAEE`, `#BFC8D2`, `#C2CCD8`, `#8FA0B2` |
| **Notes** | Heaviest `custom_css` user of any pattern — most of its styling lives in per-widget CSS, which is why it needed 9 `var()` rewrites. `#6BD0E3` (cyan) appears nowhere else in the design system and is likely an accent that should be promoted to a Kit token or removed. Each card's title is duplicated in two `heading` widgets (one is the mobile/hover label) — swap both. |

### process-steps-numbered
| | |
|---|---|
| **Snippet** | `reference/snippets/process-steps-numbered.json` |
| **Source** | post `12133` section index `5` |
| **Used by** | all 5 pages — index 5 on 12133, index 4 on 12223–12226 |
| **Signature** | `7ec08de400` · 24 widgets · 45,696 bytes |
| **Recognise when** | A "how it works" / numbered-workflow section on white: eyebrow + H2 + intro, then a row of **5** sequential step cards each led by a two-digit number (`01`…`05`), an uppercase stage label, a step title and a description — with **one** step (the engineering-review step) visually highlighted in an orange tint. |
| **Structure** | `container:full bg=gfwhite` → boxed → eyebrow → H2 → intro → row of 5 step `container`s (`heading` number → `heading` stage label → `heading` title → `text-editor` description); highlighted step uses `bg=#FFF7EF` |
| **Tokens** | 24: `{heading_1..17}`, `{body_1..7}` — 3 headings per step (`{heading_3..17}`) |
| **Globals** | 19 native · 1 CSS-var rewrite |
| **Unmapped colours** | `#5F6878`, `#E1E6EE`, `#8A94A3`, `#FFF7EF` (highlight tint), `#C2691A` (highlight text) |
| **Notes** | Highest global coverage relative to size. The highlight pair `#FFF7EF`/`#C2691A` is a tint/shade of `gforange` with no Kit token — promote as `gforange-tint`/`gforange-deep` if consolidating. |

### group-ecosystem-cards
| | |
|---|---|
| **Snippet** | `reference/snippets/group-ecosystem-cards.json` |
| **Source** | post `12133` section index `6` |
| **Used by** | all 5 pages — index 6 on 12133, index 5 on 12223–12226 |
| **Signature** | `c972a6df04` · 22 widgets · 44,517 bytes |
| **Recognise when** | A "our group / ecosystem" section on mid-navy introducing sibling business units: eyebrow + H2 + intro, then **4 white cards** each with a logo image, a unit name, a description, a condensed feature list and a "→" link — with a **"You are here"** badge marking the current unit. |
| **Structure** | `container:full bg=#152C4A` → boxed → eyebrow → H2 → intro → row of 4 white cards (`image` logo → `heading` name \[+ `heading` "You are here"] → `text-editor` description → `text-editor` feature list → `text-editor` link / `button`) |
| **Tokens** | 23: `{heading_1..7}`, `{body_1..10}`, `{image_1..4}`, `{button_1}`, `{url_1}` |
| **Globals** | 21 native · 4 CSS-var rewrites |
| **Unmapped colours** | `#152C4A` (section bg), `#E1E6EE`, `#AEB9C7`, `#5F6878` |
| **Notes** | The four units are Material Supply, Precision Fabrication (`{heading_5}` = "You are here"), Reference & Calibration, Testing & Validation. Logos are `eco-logo-1.png`…`eco-logo-4.png`; `image.id` is blanked in the fragment, so re-attach the media IDs after insert or Elementor renders broken images. **Move the "You are here" badge to the card matching the new page.** Only the current-unit card carries a `button`; the others use a text link. Section bg `#152C4A` is a third navy that matches no Kit token. |

### testimonials-avatar-cards
| | |
|---|---|
| **Snippet** | `reference/snippets/testimonials-avatar-cards.json` |
| **Source** | post `12133` section index `7` |
| **Used by** | all 5 pages — index 7 on 12133, index 6 on 12223–12226 |
| **Signature** | `724f2da328` · 17 widgets · 48,643 bytes |
| **Recognise when** | A social-proof section on a light grey background: eyebrow + H2 with **no** intro paragraph, then 3 white quote cards each with a 5-star row, the quote itself, and an author block built from a navy initials circle + name + company. |
| **Structure** | `container:full bg=#F9FAFB` → boxed → eyebrow → H2 → row of 3 white cards (`heading` ★★★★★ → `text-editor` quote → author row: `container bg=gfnavymid` with `heading` initials + `heading` name + `heading` company) |
| **Tokens** | 17: `{heading_1..14}`, `{body_1..3}` |
| **Globals** | 21 native · 0 CSS-var rewrites |
| **Unmapped colours** | `#F9FAFB` (section bg), `#E1E6EE`, `#737C8D` |
| **Notes** | Only section with an eyebrow + H2 and no intro copy — useful as a negative signal when disambiguating from other 3-card patterns. Stars are literal `★` characters in a `heading`, not an icon widget. Initials must be kept in sync with the author name by hand. |

### faq-toggle
| | |
|---|---|
| **Snippet** | `reference/snippets/faq-toggle.json` |
| **Source** | post `12133` section index `8` |
| **Used by** | all 5 pages — index 8 on 12133, index 7 on 12223–12226 |
| **Signature** | `de6df985c8` · 5 widgets · 15,988 bytes |
| **Recognise when** | An FAQ / accordion section on white: eyebrow + H2 + intro + a single "ask a question" CTA button in the left rail, with all Q&A collapsed into one accordion beside it. |
| **Structure** | `container:full bg=gfwhite` → row → copy column (eyebrow → H2 → intro → `button`) + `toggle` widget with 8 repeater items |
| **Tokens** | 21: `{heading_1..2}`, `{body_1}`, `{button_1}`, `{url_1}`, `{faq_q_1..8}`, `{faq_a_1..8}` |
| **Globals** | 7 native · 1 CSS-var rewrite |
| **Unmapped colours** | `#5F6878`, `#F3F4F6`, `#D1D5DB` |
| **Notes** | Q&A lives in the `toggle` repeater, so item count is free — add/remove `tabs[]` entries and the `{faq_q_n}`/`{faq_a_n}` tokens follow. Answers are HTML. |

### cta-band-dark
| | |
|---|---|
| **Snippet** | `reference/snippets/cta-band-dark.json` |
| **Source** | post `12133` section index `9` |
| **Used by** | all 5 pages — index 9 on 12133, index 8 on 12223–12226 |
| **Signature** | `5f75e0e0e5` · 5 widgets · 12,764 bytes |
| **Recognise when** | The page's closing conversion band on dark navy: eyebrow + H2 + one short paragraph + exactly two buttons, and nothing else. Always last. |
| **Structure** | `container:full bg=#16253D` → boxed → eyebrow → H2 → `text-editor` → button pair |
| **Tokens** | 7: `{heading_1..2}`, `{body_1}`, `{button_1..2}`, `{url_1..2}` |
| **Globals** | 6 native · 0 CSS-var rewrites |
| **Unmapped colours** | `#16253D`, `#213754`, `#1B2E4A`, `#B6C0CC`, `#46587010` |
| **Notes** | Shallowest nesting of the boxed patterns (no intermediate wrapper). `#46587010` is an **8-digit hex with alpha** — Elementor globals cannot express it, so it must stay literal. `#16253D` is a 1-channel near-miss for `gfnavy` `#15253D` and is almost certainly meant to be the same colour. |

---

## Unmapped colours

~38 distinct values have no Kit token. Grouped by apparent intent, with the
consolidation each group suggests:

| Group | Values | Suggested action |
|---|---|---|
| Dark navy surfaces | `#182336`, `#16253D`, `#152C4A`, `#1B2434`, `#1B2E4A`, `#1D2C42`, `#1E2D45`, `#213754`, `#223248`, `#22334B`, `#1A2F4A` | Collapse to 2–3 tokens (`gfnavy-surface`, `gfnavy-raised`, `gfnavy-grad-b`). `#16253D` should likely just become `gfnavy` `#15253D`. |
| Dark borders | `#33445C`, `#3A4A60`, `#2A3A52`, `#46587010` | One `gfnavy-border` token; the alpha value must stay literal. |
| On-dark text | `#B6C0CC`, `#9FB0C0`, `#AEB9C7`, `#8FA0B2`, `#8A97A6`, `#E8EDF3`, `#E0E4EA`, `#EAEDF1`, `#E8EAEE`, `#BFC8D2`, `#C2CCD8` | Collapse to `gfbody-ondark` + `gfheading-ondark`. This is the largest cluster of accidental variation. |
| Light greys / surfaces | `#F9FAFB`, `#F3F4F6`, `#ECEEF2`, `#E5E7EB`, `#E1E6EE`, `#D1D5DB` | 2 tokens (`gfsurface`, `gfborder`). |
| Body greys | `#5F6878`, `#737C8D`, `#8A94A3` | Map to `gfbody`/`gfink` or add `gfbody-muted`. |
| Orange tint/shade | `#FFF7EF`, `#C2691A` | `gforange-tint`, `gforange-deep`. |
| Orphan accent | `#6BD0E3` | Single-use cyan — promote or remove. |

Per your instruction these were **left hardcoded** and no production change was made.
The Kit (11259) and all five live pages are untouched; only the local fragments were
rewritten. Adding these tokens is a follow-up that needs a colour-consolidation
decision first, because several groups above are unintentional near-duplicates
rather than deliberate distinctions.

## Regenerating

Fragments are produced server-side from post 12133 via `novamira/execute-php`
(tokenise → apply the 6-colour global map → write to
`wp-content/uploads/novamira-drafts/patterns/`), then downloaded and verified by
SHA-256. Regenerate rather than hand-editing: these are 12–58 KB of generated JSON.

Totals across the 10 fragments: **174** placeholder tokens, **116** native
`__globals__` refs, **17** `var(--e-global-color-*)` rewrites.
