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
| `services-image-cards` | — | — | — | — | — |
| `quote-form-hubspot` | — | — | — | — | — |   <!-- minted from 12239 index 9; wired to [Potomac] Start a Project -->   <!-- minted from 12239 (pl-auto-cnc-micromachining) index 2; not present on the original five -->
| `legend-cards-dark` | — | — | — | — | — |   <!-- minted from 12268 (pl-auto-about-our-group, page) index 0 by run 20260924-100754 -->
| `split-rows-logo-alternating` | — | — | — | — | — |   <!-- minted from 12268 (pl-auto-about-our-group, page) index 1 by run 20260924-100754 -->
| `hero-dark-centered-meta` | — | — | — | — | — |   <!-- minted from 12277 (pl-auto-about-potomac, page) index 0 by run 20260924-100754 -->
| `split-media-prose` | — | — | — | — | — |   <!-- minted from 12277 (pl-auto-about-potomac, page) index 1 by run 20260924-100754 -->
| `icon-cards-3` | — | — | — | — | — |   <!-- minted from 12277 (pl-auto-about-potomac, page) index 2 by run 20260924-100754 -->
| `profile-cards-4` | — | — | — | — | — |   <!-- minted from 12277 (pl-auto-about-potomac, page) index 3 by run 20260924-100754 -->
| `stat-cards-6` | — | — | — | — | — |   <!-- minted from 12277 (pl-auto-about-potomac, page) index 4 by run 20260924-100754 -->
| `hero-dark-centered` | — | — | — | — | — |   <!-- minted from 12295 (pl-auto-case-studies, page) index 0 by run 20260924-125928 -->
| `image-link-cards-5` | — | — | — | — | — |   <!-- minted from 12295 (pl-auto-case-studies, page) index 1 by run 20260924-125928 -->
| `image-link-cards-12-button` | — | — | — | — | — |   <!-- minted from 12296 (pl-auto-news, page) index 1 by run 20260924-125928 -->
| `hero-dark-centered-cta` | — | — | — | — | — |   <!-- minted from 12298 (pl-auto-employment, page) index 0 by run 20260924-125928 -->
| `split-prose-list-media` | — | — | — | — | — |   <!-- minted from 12298 (pl-auto-employment, page) index 1 by run 20260924-125928 -->
| `text-link-cards-6-filter` | — | — | — | — | — |   <!-- minted from 12298 (pl-auto-employment, page) index 2 by run 20260924-125928 -->
| `faq-accordion-filter-10` | — | — | — | — | — |   <!-- minted from 12300 (pl-auto-faqs, page) index 1 by run 20260924-125928 -->
| `split-list-figure` | — | — | — | — | — |   <!-- minted from 12301 (pl-auto-quality-policy, page) index 1 by run 20260924-125928 -->
| `check-list-centered` | — | — | — | — | — |   <!-- minted from 12301 (pl-auto-quality-policy, page) index 2 by run 20260924-125928 -->
| `hero-split-contact-form` | — | — | — | — | — |   <!-- minted from 12302 (pl-auto-contact, page) index 0 by run 20260924-125928 -->
| `hq-panel-map` | — | — | — | — | — |   <!-- minted from 12302 (pl-auto-contact, page) index 1 by run 20260924-125928 -->
| `offices-grid-6-social` | — | — | — | — | — |   <!-- minted from 12302 (pl-auto-contact, page) index 2 by run 20260924-125928 -->
| `hero-dark-centered-meta-4` | — | — | — | — | — |   <!-- minted from 12357 (pl-auto-project-gallery, page) index 0 by run 20260924-125928 -->
| `gallery-grid-filter-lightbox` | — | — | — | — | — |   <!-- minted from 12357 (pl-auto-project-gallery, page) index 1 by run 20260924-125928 -->

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
| **Tokens** | 11: `{heading_1..3}`, `{body_1..3}`, `{button_1..2}`, `{url_1..2}`, `{image_1}` (the first column's **background** image, not an image widget) |
| **Globals** | 9 native · 1 CSS-var rewrite |
| **Unmapped colours** | `#ECEEF2`, `#5F6878`, `#F9FAFB` (inset card bg), `#E5E7EB`, `#737C8D` |
| **Notes** | The first column is a **photo column**: a 52%-wide container whose `background_image` carries the picture, at `background_size:cover`, `min_height:440`, radius 16. It is NOT a layout spacer — an earlier version of this entry said so, because the URL sits in container settings rather than an image widget and is easy to miss (AUDIT.md B12). Fill `{image_1}` per page; leaving it unfilled ships a literal `{image_1}` as the CSS url. Because it is a background rather than an image widget, SKILL.md §3's attachment-id gate had to be widened to see it. |

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

### services-image-cards
| | |
|---|---|
| **Snippet** | `reference/snippets/services-image-cards.json` |
| **Source** | post `12239` (`pl-auto-cnc-micromachining`) section index `2` |
| **Used by** | 12239 at index 2. Expected on all five service pages — the section is identical across them |
| **Signature** | `bb7f3d9fa0` · 24 widgets · 61,382 bytes |
| **Recognise when** | A light "our services / capabilities" section: eyebrow + centred H2 + one centred intro line + a single centred orange text link, then a row of **5 equal cards**, each card an image flush to its top edge above a padded block of title + one-paragraph description + a bordered "Learn more →" pill. The discriminators against `group-ecosystem-cards`: light background rather than mid-navy, five cards rather than four, no "You are here" badge, no per-card feature list, and every card carries the same pill-style link rather than one card having a button. |
| **Structure** | `container:full bg=gfwhite pad 68/0` → `container:boxed` gap 30 → head block (eyebrow row = 28×2px orange bar + uppercase heading; centred H2; centred intro; centred orange link) → card row `flex_direction:row flex_align_items:stretch flex_gap:22 flex_wrap:wrap` → 5 × card `container` (border 1px #E1E6EE, radius 8, `overflow:hidden`, padding 0, `flex:0 0 calc((100% - 88px)/5)`) → `image` + inner text `container` pad 14/14/16/14 → `heading h3` + `text-editor` + `text-editor` (pill) |
| **Tokens** | 24 placeholders: `{heading_1..7}`, `{body_1..12}`, `{image_1..5}`. Numbering is document order, so each card is a `{heading_n}` + two `{body_n}` triple: card 1 = `heading_3`/`body_3`/`body_4`, card 2 = `heading_4`/`body_5`/`body_6`, and so on |
| **Globals** | 9 native `__globals__` refs (`gforange` ×2, `gfwhite` ×6 incl. the 5 card backgrounds, section bg) · 0 CSS-var rewrites |
| **Unmapped colours** | `#0F1F3A` (H2 + card titles), `#111827` (body text), `#B9681F` (pill text), `#D5DCE7` (pill border), `#E1E6EE` (card border — already library-wide) |
| **Notes** | Five-up needs `flex:0 0 calc((100% - 88px)/5)` in `custom_css`: percentage widths plus 22px pixel gaps overflow the 1224px container and wrap the fifth card. The card descriptions need an explicit `selector p{font-size:14px}` — the theme styles `p` at 16px and beats the widget's inherited typography. `overflow:hidden` on the card is what makes the image sit flush inside the 8px radius. Image `id` is blanked in the fragment — re-attach on build (SKILL.md §3). **Verified against the design at 12 computed properties with zero diffs**; it took three §7.3 iterations (wrap, then font size). Its legend keeps full markup, unlike the original ten (AUDIT.md B9). |

### quote-form-hubspot
| | |
|---|---|
| **Snippet** | `reference/snippets/quote-form-hubspot.json` |
| **Source** | post `12239` (`pl-auto-cnc-micromachining`) section index `9` |
| **Used by** | 12239 at index 9. Expected on all five service pages — the section is identical across them |
| **Signature** | `html`-widget section · 3 containers + 1 widget · 16,575 bytes |
| **Recognise when** | A two-column "rapid response quote" section: left column is eyebrow + H2 + two short paragraphs + a confidentiality note + a 3-item "now / within hours / within 24 hours" timeline; right column is a white card with a two-step progress indicator and a form collecting first and last name (side by side), company, email, a part-description textarea and a single file upload, ending in one primary action. Distinguish from `cta-band-dark`, which is a closing band with two buttons and **no fields**. If the design shows a *second* variant with tolerance/quantity selects (`data-quote-variant="detailed"`), it is the same pattern — those two fields have no HubSpot property and fold into the description (see Notes). |
| **Structure** | `container:full bg=gfwhite pad 64/0` → `container:boxed` → ONE `html` widget carrying the section's markup, its scoped `<style>`, and its `<script>`. Not an iframe: WindPress compiles Tailwind in rendered DOM but not inside iframe documents, and a form needs no overlay bridge |
| **Tokens** | 21 placeholders: `{heading_1..11}`, `{body_1..9}`, `{button_1}`. **They substitute inside the single `html` string**, so `body_*` values are plain text, not block markup — the reverse of every other fragment. `tools/validate_spec.py` exempts this pattern from the HTML-slot check via `EMBED_TEXT_PATTERNS` |
| **Globals** | 1 native `__globals__` ref (section background `gfwhite`). The form's own colours live in its scoped `<style>` |
| **Unmapped colours** | inside the scoped `<style>` only — none reach Elementor settings |
| **Notes** | **Wired, not decorative.** Posts direct to the HubSpot Forms API v3 at portal `143181153`, form `[Potomac] Start a Project` (`9dba7d36-e36b-4a10-9411-9dc073dab7a0`) — no Gravity Forms. The full contract, including why Tolerance/Quantity fold into `potomac_project_description` and why only ONE file property is used, is `reference/HUBSPOT-FORMS.md`. **The wiring, CSS and JS are deliberately untokenised** — identical on every page, and must not be edited per page. Two gotchas that cost iterations: the design's action button is `type="button"` and therefore never raises a `submit` event, so the script binds it explicitly; and the section's CSS must be scoped to its own classes — one extracted rule carried `h1..h6, .hero-title, .section-title, .gf-services-title` alongside `.gf-rapid-left h2` and silently restyled every heading on the page. Verified 2026-08-06 by a live test submission: seven fields accepted, `lead_form_submit_success`, and no PII in the dataLayer. `potomac_file_submission` is still unproven — no test has carried a file. **Revised 2026-09-24** (supervised, from the re-export's design): "Your name" split on the first space became required First name + Last name fields sent straight to `firstname`/`lastname`, and optional Organisation became required Company; two visible em dashes in the form's own messages were removed per the content style rules. Needs a fresh test submission before it counts as verified; the pre-change fragment is pinned in `tools/fixtures/mhd-preorder/snippets/` for the assembler self-test. |

### legend-cards-dark
| | |
|---|---|
| **Snippet** | `reference/snippets/legend-cards-dark.json` |
| **Source** | post `12268` (`pl-auto-about-our-group`, type `page`) section index `0` — minted by run 20260924-100754 (§7) |
| **Used by** | 12268 at index 0 |
| **Signature** | `27c0eddfbf` (sha256 of the elType/widgetType tree, first 10 hex) · 16 containers + 11 widgets · 56,205 bytes |
| **Recognise when** | A dark navy section (flat `#0D1B2A` with a faint 32px grid and two soft radial glows) holding a **centred** head — small uppercase orange eyebrow, one H2, one lede paragraph capped ~760px — followed by a single row of **4 small white link cards**, each card only a coloured dot + a short name on one line and an uppercase role label under it, the whole card a jump link. No images, no buttons, no body copy inside the cards. Discriminators: against `group-ecosystem-cards`, no logos, no feature lists, no "You are here" badge and no per-card link text; against `hero-dark-stat-strip`, a centred H2 (not an H1) and cards rather than big-number stats; against `cta-band-dark`, cards and no buttons. Card count is **adjustable** (see Notes). |
| **Structure** | `container:full bg=gfnavydp pad 80/24` + `custom_css` grid/glow background → `container:boxed` (`boxed_width` 1152) column centred → head `container` width 760 (`heading` eyebrow, `heading h2` margin 12/0/16, `text-editor` lede) → card row `flex_direction:row flex_align_items:stretch flex_gap:14 flex_wrap:wrap` margin-top 48 → 4 × card `container` `html_tag:a` + `link` (bg `gfwhite`, border 1px `#DCE1EA`, radius 8, pad 18/20, `flex:0 0 calc((100% - 42px)/4)`, 2-up under 880px, hover lift) → name row `container` (11px dot `container` radius 50% + `heading` name) + `heading` role |
| **Tokens** | 15 placeholders: `{heading_1..10}`, `{body_1}`, `{url_1..4}`. Head = `heading_1` eyebrow, `heading_2` H2, `body_1` lede; then card n = `heading_(2n+1)` name, `heading_(2n+2)` role, `url_n` link |
| **Globals** | 10 native `__globals__` refs (`gfnavydp` section bg, `gforange` eyebrow + dots 1–2, `gfblue` dot 3, `gfwhite` H2 + 4 card backgrounds) · 0 CSS-var rewrites |
| **Unmapped colours** | `#0F1620` (card name — design `--fg-1`), `#65718A` (role — `--fg-3`), `#DCE1EA` (card border — `--border-1`), `#C3CBD8` (hover border), `#F08423` (dot 4 — design `--logo-orange`), `rgba(255,255,255,0.74)` (lede), plus the grid/glow `rgba()` stops in `custom_css` |
| **Notes** | **Dot colours are per card position, not tokens** (orange, orange, blue, `#F08423`): they are the four group brands' colours and the vocabulary has no colour token. A page that needs other colours needs a variant. **Adjustable count:** add or remove a card by duplicating one card container and renumbering its `heading`/`url` pair — then change the `42px` in each card's `calc()` to `(n-1) × 14px` and the `/4` to `/n`. Links are `#split-row-1..4` on 12268 because the section's sibling `split-rows-logo-alternating` fixes those anchors. Every text widget names `Inter` explicitly: on a `page` there is no Code Snippet #10 font rule and Elementor falls back to Roboto. Every nested container sets `padding:0` — Elementor's 10px default otherwise renders an 11px dot at 20×20. Container spacing uses `margin`, never `_margin` (the widget key, silently ignored on a container — cost verify iteration 2). **Verified on 12268 at 1792px** (iteration 3): exact word-for-word text match with the design, legend cards 278×118 = design, section height 610 vs design 616. |

### split-rows-logo-alternating
| | |
|---|---|
| **Snippet** | `reference/snippets/split-rows-logo-alternating.json` |
| **Source** | post `12268` (`pl-auto-about-our-group`, type `page`) section index `1` — minted by run 20260924-100754 (§7) |
| **Used by** | 12268 at index 1 |
| **Signature** | `5dbd8d5829` (sha256 of the elType/widgetType tree, first 10 hex) · 26 containers + 40 widgets · 132,319 bytes |
| **Recognise when** | A white section of **stacked two-column rows that alternate sides** (row 1 visual left, row 2 visual right, …), 96px apart. The visual column is a bordered white **logo panel** (16:10, radius 16, light shadow, a 4px coloured accent bar along its top edge, one centred contained logo, a small monospace pill in its bottom-right corner such as "Since 1946"). The copy column is a coloured dot + uppercase eyebrow, an H2, a bold lead paragraph, a body paragraph, a wrapping row of **3 rounded stat pills** (`<strong>value</strong> label`) and one orange pill button. Discriminators: against `why-choose-inset-cta`, many rows rather than one, no tinted inset card, and the image is a contained logo on a panel rather than a cover photo; against `group-ecosystem-cards`, full-width rows rather than a 4-up card grid. **One image per row** — the design's image count must equal the row count. Row count is adjustable (see Notes). |
| **Structure** | `container:full bg=gfwhite pad 80/24` → `container:boxed` (`boxed_width` 1152) column, `flex_gap` 96 → 4 × row `container` (`_element_id` `split-row-n`, `flex_direction` `row` / `row-reverse` alternating, `column` on mobile, gap 72) → visual `container` (`calc((100% - 72px)/2)`, pad 48, border 1px `#DCE1EA`, radius 16, `aspect-ratio:16/10`, `::before` 4px accent) → `image` (78% wide, max-height 155px, contain) + `heading` pill (absolute bottom-right, JetBrains Mono) ; copy `container` → eyebrow row (9px dot + `heading`) margin-bottom 14 → `heading h2` → `text-editor` lead → `text-editor` body → pill row `container` (3 × `text-editor` pill) margin-bottom 24 → `button` |
| **Tokens** | 44 placeholders: `{image_1..4}`, `{heading_1..12}`, `{body_1..20}`, `{button_1..4}`, `{url_1..4}`. Per row n, in document order: `image_n`, founded pill, eyebrow, H2 (`heading_3n-2..3n`), lead, body, stat 1–3 (`body_5n-4..5n`), `button_n`, `url_n` |
| **Globals** | 35 native `__globals__` refs (`gfwhite` section/panel bg + buttons' text, `gforange` rows 1–2 dot/eyebrow + all buttons, `gfblue` row 3 dot/eyebrow, `gfink` body + pill text) · **3** `var(--e-global-color-*)` rewrites (the `::before` accent bar in `custom_css`: `gforange` ×2, `gfblue` ×1) |
| **Unmapped colours** | `#0F1620` (H2, lead, pill `<strong>`), `#65718A` (founded pill text), `#DCE1EA` (panel + pill borders), `#F6F8FB` (pill fill — design `--bg-subtle`), `#F08423` (row 4 accent/dot/eyebrow — `--logo-orange`), `rgba(15,22,32,.06)`/`.04` (panel shadow), `rgba(245,130,31,.3)` (button shadow) |
| **Notes** | **Accent colours are per row position** (orange, orange, blue, `#F08423`) — the four group brands, same limitation as `legend-cards-dark`. **Anchors are fixed**: rows carry `_element_id` `split-row-1..4` because the vocabulary has no anchor token; jump links must target those. **Adjustable count:** duplicate or delete a whole row container, keep `row`/`row-reverse` alternating, and renumber that row's tokens; stat pills are a fixed 3 per row (a row with fewer leaves an empty pill — drop the widget instead). Pills need `selector{width:auto}` on the text-editor so they size to content. On a `page` the Code Snippet #10 1224px cap does not apply, so `boxed_width` 1152 is set on the section itself (design `.container` 1200 − 2 × 24). **Verified on 12268 at 1792px** (iteration 3): exact word-for-word text match, rows 422–437px vs design 430, logos 345×76 / 345×77 / 345×132 / 297×155 vs design 345×76 / 345×77 / 345×132 / 293×153. Legend keeps full markup. |

### hero-dark-centered-meta
| | |
|---|---|
| **Snippet** | `reference/snippets/hero-dark-centered-meta.json` |
| **Source** | post `12277` (`pl-auto-about-potomac`, type `page`) section index `0` — minted by run 20260924-100754 (§7) |
| **Used by** | 12277 at index 0 |
| **Signature** | `d09ff47676` (sha256 of the elType/widgetType tree, first 10 hex) · 6 containers + 9 widgets · 23,574 bytes |
| **Recognise when** | The page's opening section on dark navy (flat `#0D1B2A` + faint 32px grid + two soft glows), **everything centred**: small uppercase orange eyebrow, one H1 (~54px), one lede paragraph capped ~727px that may carry `<strong>` and an inline link, then a centred row of **exactly 3 meta stats** (white value ~28px over a dim uppercase label) — and **no buttons, no image, no divider**. Discriminators: against `hero-dark-stat-strip`, that one is left-aligned in a 60% column with two CTAs + a tertiary link and a rule above 5 stats; against `legend-cards-dark`, an H1 and stats rather than an H2 and link cards. A centred hero with **no** meta row, or with a CTA instead, is a different variant — this fragment's stat count is fixed at 3. |
| **Structure** | `container:full bg=gfnavydp pad 72/24/64` + `custom_css` grid/glow → `container:boxed` (`boxed_width` 1200) column centred → `heading` eyebrow → `heading h1` (margin 38/0/18, title `max-width:22ch`, `text-wrap:balance`) → `text-editor` lede (`p` max-width 727, `strong` white 600, `a` white underlined) → meta row `container` (row, wrap, centred, gap 28/40, margin-top 32) → 3 × stat `container` (column, gap 4, `width:auto`) → `heading` value + `heading` label |
| **Tokens** | 9 placeholders: `{heading_1..8}`, `{body_1}`. `heading_1` eyebrow, `heading_2` H1, `body_1` lede; stat n = `heading_(2n+1)` value, `heading_(2n+2)` label |
| **Globals** | 6 native `__globals__` refs (`gfnavydp` section bg, `gforange` eyebrow, `gfwhite` H1 + 3 values) · 0 CSS-var rewrites |
| **Unmapped colours** | `rgba(255,255,255,0.74)` (lede), `rgba(255,255,255,0.55)` (stat labels), `#fff` (3-digit, lede `strong`/`a` in `custom_css`), plus the grid/glow `rgba()` stops |
| **Notes** | The eyebrow-to-H1 gap is 38px because the design's eyebrow sits in a 24px line box with a 20px margin and the H1 carries an 18px margin; do not "correct" it to 20. The lede and H1 widths must be capped on the inner `p` / `.elementor-heading-title`, not on the widget — a widget-level `max-width` is ignored inside a flex container (cost verify iteration 1 on 12277). Every text widget names `Inter` and every nested container sets `padding:0` (see `legend-cards-dark` Notes). Inline links in the lede need `font-size:inherit` — the theme sizes bare `a` at 16px (iteration 2). **Verified on 12277 at 1792px** (iteration 3): word-for-word text match; lede 727×150 vs design 727×148. The section is 570px vs the design's 517 **only because the brand-normalised H1** ("The story of Goodfellow Microfabrication") wraps to two lines where the design's "The story of Potomac" is one. |

### split-media-prose
| | |
|---|---|
| **Snippet** | `reference/snippets/split-media-prose.json` |
| **Source** | post `12277` (`pl-auto-about-potomac`, type `page`) section index `1` — minted by run 20260924-100754 (§7) |
| **Used by** | 12277 at index 1 |
| **Signature** | `054b8ffacd` (sha256 of the elType/widgetType tree, first 10 hex) · 6 containers + 6 widgets · 23,915 bytes |
| **Recognise when** | A white two-column section: **left, one photo** shown whole (not cropped) in a rounded 18px frame with a deep soft shadow; **right, prose** — orange uppercase eyebrow, an H2 (~36px), one paragraph, then **two pill buttons side by side** (solid orange primary + white outlined-orange secondary). Photo on the left. Discriminators: against `why-choose-inset-cta`, no tinted inset card and the image is an `<img>` in a frame, not a cover-photo background; against `split-rows-logo-alternating`, one row, a photo rather than a logo panel, and no stat pills. A split whose copy column is a **list** instead of a paragraph + buttons, or whose image is on the **right**, is a different variant. |
| **Structure** | `container:full bg=gfwhite pad 80/24` → `container:boxed` → row `container` (wrap, centred, gap 72; each column `calc((100% - 72px)/2)`, full width under 980px) → media `container` (bg `gfnavydp`, border 1px `#DCE1EA`, radius 18, `overflow:hidden`, shadow) → `image` ; prose `container` (column, flex-start) → `heading` eyebrow (mb 14) → `heading h2` (mb 18) → `text-editor` (mb 16) → button row `container` (gap 12, mt 8) → 2 × `button` |
| **Tokens** | 8 placeholders: `{image_1}`, `{heading_1..2}`, `{body_1}`, `{button_1..2}`, `{url_1..2}` |
| **Globals** | 9 native `__globals__` refs (`gfwhite` section bg + primary text + secondary bg, `gfnavydp` media bg, `gforange` eyebrow + primary bg + secondary text + secondary border, `gfink` paragraph) · 0 CSS-var rewrites. The secondary button's `border_color` was mapped to `gforange` at tokenisation (colour-map step) — the verified post 12277 still stores it as the literal hex, which renders identically |
| **Unmapped colours** | `#0F1620` (H2), `#DCE1EA` (frame border), `rgba(15,42,68,.12)` (frame shadow), `rgba(245,130,31,.3)` (primary button shadow) |
| **Notes** | **Verified on 12277 at 1792px** (iteration 3): word-for-word text match; photo 538×227 vs design 540×229 (the 1px frame border). Section 511px vs design 480 **only because the brand-normalised paragraph** ("Goodfellow Microfabrication combines…" for "Potomac combines…") wraps to 4 lines at the same 540px column where the design's is 3 — confirmed by measuring the design mock in the same browser. |

### icon-cards-3
| | |
|---|---|
| **Snippet** | `reference/snippets/icon-cards-3.json` |
| **Source** | post `12277` (`pl-auto-about-potomac`, type `page`) section index `2` — minted by run 20260924-100754 (§7) |
| **Used by** | 12277 at index 2 |
| **Signature** | `9788c68030` (sha256 of the elType/widgetType tree, first 10 hex) · 7 containers + 11 widgets · 30,175 bytes |
| **Recognise when** | A light-grey (`#F6F8FB`) section: **centred** eyebrow + H2 with **no lede**, then **3 equal white cards** in a row, each a small **48px icon** top-left, a short bold title (~17.6px, navy) and one paragraph of grey text (links allowed inline). No buttons, no card links, no photos. Discriminators: against `testimonials-avatar-cards`, no stars, no quote, no initials circle; against `group-ecosystem-cards`, light background, 3 cards, icons not logos, no feature list or badge; against `stat-cards-6`, an icon and a title rather than a label + big value. |
| **Structure** | `container:full bg=#F6F8FB pad 80/24` → `container:boxed` column centred → head `container` width 760 (eyebrow `heading` + `heading h2` margin-top 18) margin-bottom 48 → card row `container` (wrap, stretch, gap 20; children `calc((100% - 40px)/3)`, full width under 980px) → 3 × card `container` (bg `gfwhite`, border 1px `#DCE1EA`, radius 8, pad 28/26, gap 14, shadow) → `image` (48×48) + `heading h3` + `text-editor` |
| **Tokens** | 11 placeholders: `{heading_1..5}`, `{body_1..3}`, `{image_1..3}`. `heading_1` eyebrow, `heading_2` H2; card n = `image_n`, `heading_(n+2)`, `body_n` |
| **Globals** | 10 native `__globals__` refs (`gforange` eyebrow, `gfwhite` 3 card backgrounds, `gfnavy` 3 titles, `gfbody` 3 texts) · **6** `var(--e-global-color-*)` rewrites (card text link colour `gfnavy` / hover `gforange`, ×3) |
| **Unmapped colours** | `#F6F8FB` (section bg — design `--bg-subtle`), `#0F1620` (H2), `#DCE1EA` (card border), `rgba(0,0,0,.07)` (card shadow) |
| **Notes** | The eyebrow/H2 head is shared with `profile-cards-4` and `stat-cards-6` (same measurements); the 18px H2 offset reproduces the design's 12px margin inside a 24px eyebrow line box — `legend-cards-dark`, minted earlier with 12px, sits 6px shorter than its design for this reason. SVG icons upload through Safe SVG, which sanitises (rewrites) the file, so an icon's stored SHA-256 differs from the source. **Verified on 12277 at 1792px** (iteration 3): cards 371×319 = design, section 607 = design, icons 48×48, word-for-word text match. |

### profile-cards-4
| | |
|---|---|
| **Snippet** | `reference/snippets/profile-cards-4.json` |
| **Source** | post `12277` (`pl-auto-about-potomac`, type `page`) section index `3` — minted by run 20260924-100754 (§7) |
| **Used by** | 12277 at index 3 |
| **Signature** | `96de263766` (sha256 of the elType/widgetType tree, first 10 hex) · 12 containers + 19 widgets · 56,493 bytes |
| **Recognise when** | A white "team / leadership" section: **centred** eyebrow + H2 with no lede, then **4 equal-height cards** in one row, each a **square portrait photo flush to the top**, then a padded body of orange uppercase role, bold navy name, **bio paragraphs**, and an uppercase "LinkedIn profile"-style link pinned to the card's bottom. **This fragment is irregular, exactly as the source design is:** cards 1–2 have bio + link, card 3 has a bio and **no link**, card 4 is **name-only** (photo + role + name). Discriminators: against `testimonials-avatar-cards`, real photos not initials, no stars or quotes; against `icon-cards-3`, full-bleed photos and a role line. |
| **Structure** | `container:full bg=gfwhite pad 80/24` → `container:boxed` column centred → head (as `icon-cards-3`) → card row (`calc((100% - 60px)/4)`, stretch) → 4 × card `container` (bg `gfwhite`, border 1px `#DCE1EA`, radius 8, pad 0, `overflow:hidden`, shadow) → `image` (1:1, cover) + body `container` (pad 20/22/24, gap 10, `flex:1 1 auto`) → `heading` role + `heading h3` name [+ `text-editor` bio] [+ `text-editor` link, `margin-top:auto`] |
| **Tokens** | 19 placeholders: `{heading_1..10}`, `{body_1..5}`, `{image_1..4}`. `heading_1` eyebrow, `heading_2` H2; card 1 = `image_1` `heading_3` role `heading_4` name `body_1` bio `body_2` link; card 2 = `image_2` `heading_5/6` `body_3/4`; card 3 = `image_3` `heading_7/8` `body_5` (bio only); card 4 = `image_4` `heading_9/10` |
| **Globals** | 19 native `__globals__` refs (`gfwhite` section + 4 cards, `gforange` eyebrow + 4 roles, `gfnavy` 4 names + 2 links, `gfbody` 3 bios) · **8** `var(--e-global-color-*)` rewrites (photo backdrop `gfnavydp` ×4, link colour `gfnavy` / hover `gforange`) |
| **Unmapped colours** | `#0F1620` (H2), `#DCE1EA` (card border), `rgba(0,0,0,.07)` (card shadow) |
| **Notes** | **Why irregular:** `tools/validate_spec.py` rejects an empty token value, and a §7 validator failure discards the pattern (§7.8), so "optional" slots cannot be expressed as empty strings. To reuse for a team whose cards all have bio + link, copy card 1's bio/link `text-editor` pair into cards 3–4 and renumber; to drop a link, delete that widget. The bio slot is one `text-editor` holding one or more `<p>` (`p + p` gets 10px). The link is its own widget with `margin-top:auto`, which is what pins it to the bottom of an equal-height card. **Verified on 12277 at 1792px** (iteration 3): cards 273×1050 = design, section 1339 vs 1338, portraits 271×271, word-for-word text match (one typographic difference: WordPress curls the apostrophe in "Potomac's"). |

### stat-cards-6
| | |
|---|---|
| **Snippet** | `reference/snippets/stat-cards-6.json` |
| **Source** | post `12277` (`pl-auto-about-potomac`, type `page`) section index `4` — minted by run 20260924-100754 (§7) |
| **Used by** | 12277 at index 4 |
| **Signature** | `be331053a6` (sha256 of the elType/widgetType tree, first 10 hex) · 10 containers + 20 widgets · 57,558 bytes |
| **Recognise when** | A light-grey (`#F6F8FB`) "by the numbers" section: **centred** eyebrow + H2 with no lede, then **6 white cards in a 3 × 2 grid**, each an orange uppercase label, one **big navy value** (~35px, a number *or* a single word such as "Rapid"), and one short grey line. No icons, no images, no links. Discriminators: against `spec-table-dark`, light cards in a grid rather than dark label/value rows; against `hero-dark-stat-strip` / `hero-dark-centered-meta`, a standalone light section with a description per value; against `icon-cards-3`, no icon and a big value in place of a title. |
| **Structure** | `container:full bg=#F6F8FB pad 80/24` → `container:boxed` column centred → head (as `icon-cards-3`) → card row (`calc((100% - 40px)/3)`, wrap, stretch, gap 20) → 6 × card `container` (bg `gfwhite`, border 1px `#DCE1EA`, radius 8, pad 26/24, gap 8, shadow) → `heading` label + `heading` value + `text-editor` |
| **Tokens** | 20 placeholders: `{heading_1..14}`, `{body_1..6}`. `heading_1` eyebrow, `heading_2` H2; card n = `heading_(2n+1)` label, `heading_(2n+2)` value, `body_n` line |
| **Globals** | 25 native `__globals__` refs (`gforange` eyebrow + 6 labels, `gfwhite` 6 cards, `gfnavy` 6 values, `gfbody` 6 lines) · 0 CSS-var rewrites |
| **Unmapped colours** | `#F6F8FB` (section bg), `#0F1620` (H2), `#DCE1EA` (card border), `rgba(0,0,0,.07)` (card shadow) |
| **Notes** | Six is fixed in the fragment; a 3-card row is the same structure with cards 4–6 deleted and their tokens dropped (renumber). **Verified on 12277 at 1792px** (iteration 3): cards 371×170 = design, section 648 = design, word-for-word text match. |

### hero-dark-centered
| | |
|---|---|
| **Snippet** | `reference/snippets/hero-dark-centered.json` |
| **Source** | post `12295` (`pl-auto-case-studies`, type `page`) section index `0` — minted by run 20260924-125928 (§7) |
| **Used by** | 12295 at index 0, 12296 (`pl-auto-news`) at index 0 |
| **Signature** | `4f1fa16177` (sha256 of the elType/widgetType tree, first 10 hex) · 2 containers + 3 widgets · 6,921 bytes |
| **Recognise when** | The page's opening section on dark navy (flat `#0D1B2A` + faint 32px grid + two soft glows), **everything centred**, holding only a small uppercase orange eyebrow, one H1 (~54px) and one lede paragraph (may carry `<strong>` / an inline link) — **nothing else**: no meta stats, no buttons, no image. Discriminators: with a row of 3 stats it is `hero-dark-centered-meta`; with a CTA or 2 CTAs + stats it is `hero-dark-centered-cta` / `hero-dark-stat-strip`. |
| **Structure** | `container:full bg=gfnavydp pad 72/24/64` + `custom_css` grid/glow → `container:boxed` (`boxed_width` 1200) column centred → `heading` eyebrow → `heading h1` (margin 43/0/18, title `max-width:22ch`, `text-wrap:balance`) → `text-editor` lede (`p` max-width 727) |
| **Tokens** | 3 placeholders: `{heading_1}` eyebrow, `{heading_2}` H1, `{body_1}` lede |
| **Globals** | 3 native `__globals__` refs (`gfnavydp` bg, `gforange` eyebrow, `gfwhite` H1) · 0 CSS-var rewrites |
| **Unmapped colours** | `rgba(255,255,255,0.74)` (lede), `#fff` (3-digit, lede `strong`/`a`), grid/glow `rgba()` stops |
| **Notes** | Same builder as `hero-dark-centered-meta` minus the meta row, **with one correction**: the H1 top margin is 43px (24px eyebrow line box + 20 + 18 − the widget's own 18px line) — at 38 the section is 5px short, which is also the residual on `hero-dark-centered-meta` (minted with 38; not edited). **Verified**: 12295 332px = design; 12296 390px = design 332 + one extra H1 line from the brand-normalised "News from Goodfellow Microfabrication". Tokenised positionally (build ≡ template, 0 leaf mismatches). |

### image-link-cards-5
| | |
|---|---|
| **Snippet** | `reference/snippets/image-link-cards-5.json` |
| **Source** | post `12295` (`pl-auto-case-studies`, type `page`) section index `1` — minted by run 20260924-125928 (§7) |
| **Used by** | 12295 at index 1 |
| **Signature** | `6f5b0b1d1c` (sha256 of the elType/widgetType tree, first 10 hex) · 13 containers + 25 widgets · 74,151 bytes |
| **Recognise when** | A light-grey (`#F6F8FB`) section with **no section head** holding a 3-column grid of **exactly 5** white cards, each card **one link** (the whole card is an `<a>`): an image flush to the top at 16:10, then an orange uppercase tag (category/date), a bold navy title, one grey paragraph, and an uppercase "Read the …" label pinned to the bottom; hover lifts the card and draws an orange bar along its bottom edge. Discriminators: against `profile-cards-4`, no head, 16:10 not square, whole-card link; against `services-image-cards`, 3-up not 5-up and no section head; with 12 cards and a closing button it is `image-link-cards-12-button`. |
| **Structure** | `container:full bg=#F6F8FB pad 80/24` → `container:boxed` → card row (wrap, stretch, gap 20; `calc((100% - 40px)/3)`) → 5 × card `container` `html_tag:a` + `link` (border 1px `#DCE1EA`, radius 8, `overflow:hidden`, shadow, `::after` orange bar) → `image` (16:10 cover on `gfnavydp`) + body `container` (pad 20/22/24, gap 10) → `heading` tag + `heading h3` + `text-editor` + `text-editor` label (`margin-top:auto`) |
| **Tokens** | 30 placeholders: `{image_1..5}`, `{heading_1..10}`, `{body_1..10}`, `{url_1..5}`. Card n = `image_n`, `heading_(2n-1)` tag, `heading_(2n)` title, `body_(2n-1)` text, `body_(2n)` label, `url_n` |
| **Globals** | 25 native `__globals__` refs (`gfwhite` ×5 card bg, `gforange` ×5 tags, `gfnavy` ×10 titles + labels, `gfbody` ×5 text) · 15 `var(--e-global-color-*)` in `custom_css` (hover bar `gforange`, image backdrop `gfnavydp`, label `gfnavy`) |
| **Unmapped colours** | `#F6F8FB` (section bg), `#DCE1EA` (card border), `rgba(0,0,0,.07)` / `rgba(15,42,68,.08)` (shadows) |
| **Notes** | Card links open in a new tab (`is_external`), as the design's `target="_blank"`. Rows equalise per flex line, like the design's grid rows (478 / 455). The count is fixed at 5 — for other counts see `image-link-cards-12-button` or mint a sibling. **Verified on 12295** (iteration 2): cards 371×478 / 371×455 and images 369×230 = design; section 1114 = design; word-for-word text match (222/222). Tokenised positionally: the five "Read the case study" labels are identical, so value-based inversion would be ambiguous. |

### image-link-cards-12-button
| | |
|---|---|
| **Snippet** | `reference/snippets/image-link-cards-12-button.json` |
| **Source** | post `12296` (`pl-auto-news`, type `page`) section index `1` — minted by run 20260924-125928 (§7) |
| **Used by** | 12296 at index 1 |
| **Signature** | `efe3827ff7` (sha256 of the elType/widgetType tree, first 10 hex) · 28 containers + 61 widgets · 177,876 bytes |
| **Recognise when** | As `image-link-cards-5` — light grey, no head, whole-card links with a 16:10 image, tag, title, text and a pinned "Read the …" label — but **12 cards** (4 rows of 3) **followed by one centred white pill button outlined in orange** ("Older news"), 40px below the grid. |
| **Structure** | as `image-link-cards-5`, with 12 cards, then a row `container` (centred, margin-top 40) → `button` (white bg, orange text and 1px orange border) |
| **Tokens** | 74 placeholders: `{image_1..12}`, `{heading_1..24}`, `{body_1..24}`, `{url_1..13}`, `{button_1}`. Card n as `image-link-cards-5`; `url_13` is the button's link |
| **Globals** | 63 native `__globals__` refs (incl. the button's `border_color` → `gforange`, mapped at tokenisation) · 36 `var(--e-global-color-*)` in `custom_css` |
| **Unmapped colours** | as `image-link-cards-5` |
| **Notes** | **Verified on 12296** (iteration 2): section 2329 vs design 2328, row heights 524/478/524/501 = design, button 132×41 centred, word-for-word text match (507/507), 12/12 images. |

### hero-dark-centered-cta
| | |
|---|---|
| **Snippet** | `reference/snippets/hero-dark-centered-cta.json` |
| **Source** | post `12298` (`pl-auto-employment`, type `page`) section index `0` — minted by run 20260924-125928 (§7) |
| **Used by** | 12298 at index 0 |
| **Signature** | `a876b67d24` (sha256 of the elType/widgetType tree, first 10 hex) · 3 containers + 4 widgets · 10,898 bytes |
| **Recognise when** | As `hero-dark-centered` (dark navy grid, everything centred, eyebrow + H1 + lede) **plus exactly one** large orange pill CTA centred 30px below the lede — and no meta stats. With 3 stats instead of a button it is `hero-dark-centered-meta`; with nothing it is `hero-dark-centered`. |
| **Structure** | as `hero-dark-centered`, then a row `container` (centred, margin-top 30) → `button` (15px/600, padding 15/28, 1px transparent border, orange glow) |
| **Tokens** | 5 placeholders: `{heading_1}` eyebrow, `{heading_2}` H1, `{body_1}` lede, `{button_1}`, `{url_1}` |
| **Globals** | 5 native `__globals__` refs (`gfnavydp`, `gforange` ×2, `gfwhite` ×2) · 0 CSS-var rewrites |
| **Unmapped colours** | as `hero-dark-centered`, plus `rgba(245,130,31,.3)` (button glow) |
| **Notes** | **Verified on 12298** (iteration 2): button 165×47 = design; section 526 = design 468 + one extra H1 line from the brand-normalised "Careers at Goodfellow Microfabrication". |

### split-prose-list-media
| | |
|---|---|
| **Snippet** | `reference/snippets/split-prose-list-media.json` |
| **Source** | post `12298` (`pl-auto-employment`, type `page`) section index `1` — minted by run 20260924-125928 (§7) |
| **Used by** | 12298 at index 1 |
| **Signature** | `127ff3cc50` (sha256 of the elType/widgetType tree, first 10 hex) · 5 containers + 5 widgets · 16,554 bytes |
| **Recognise when** | A white two-column section: **left, prose** — orange eyebrow, H2 (~36px), one paragraph, then a **check-list** whose items are each a bordered white card (radius 12) led by an orange check mark; **right, one framed photo** (radius 18, deep soft shadow). Photo on the **right**. Discriminators: against `split-media-prose`, photo on the right and a check-list instead of two buttons; a list + a **captioned figure** is a different variant. |
| **Structure** | `container:full bg=gfwhite pad 80/24` → `container:boxed` → row (gap 72, `calc((100% - 72px)/2)`, stacks under 980px) → prose `container` (eyebrow `heading` mb 20, `heading h2` mb 18, `text-editor` mb 16, `text-editor` list) + media `container` (`gfnavydp`, border, radius 18) → `image` |
| **Tokens** | 5 placeholders: `{heading_1}` eyebrow, `{heading_2}` H2, `{body_1}` paragraph, `{body_2}` list (`<ul><li>…</li></ul>`), `{image_1}` |
| **Globals** | 5 native `__globals__` refs · 1 `var(--e-global-color-gfink)` (list text in `custom_css`) |
| **Unmapped colours** | `#0F1620` (H2), `#DCE1EA` (item + frame borders), `rgba(15,42,68,.12)` (frame shadow); the check icon is an inline SVG data URI stroked `#F5821F` |
| **Notes** | **The list is one `{body_2}` token**, so the item count is free — every `<li>` becomes a card with a CSS `::before` check (no per-item widgets). The eyebrow's bottom margin is 20 (design 14 + its 24px line box). **Verified on 12298** (iteration 2): section 703 vs design 702, list items 540×60 = design, photo 538×359 = design, word-for-word text match. |

### text-link-cards-6-filter
| | |
|---|---|
| **Snippet** | `reference/snippets/text-link-cards-6-filter.json` |
| **Source** | post `12298` (`pl-auto-employment`, type `page`) section index `2` — minted by run 20260924-125928 (§7) |
| **Used by** | 12298 at index 2 |
| **Signature** | `aa512218fd` (sha256 of the elType/widgetType tree, first 10 hex) · 10 containers + 27 widgets · 74,277 bytes |
| **Recognise when** | A light-grey section: **centred** eyebrow + H2, then a centred row of **category filter chips** (uppercase pills, the active one filled orange, "All" first), then a 3-column grid of **exactly 6 text-only** white cards, each a whole-card link with an orange uppercase category, a bold navy title, one short grey line (e.g. "Full time · …") and an uppercase "View details" label. No images. A chip shows only the cards whose category label equals the chip's text. |
| **Structure** | `container:full bg=#F6F8FB pad 80/24` (`_element_id` `openings`) → `container:boxed` column centred → head (as `icon-cards-3`) → `html` widget (chips + scoped style + filter script), margin-bottom 28 → card row (`calc((100% - 40px)/3)`) → 6 × card `container` `html_tag:a` (`css_classes: pl-filter-card`, pad 24/24/26, gap 10) → `heading` category + `heading h3` + `text-editor` + `text-editor` label |
| **Tokens** | 33 placeholders: `{heading_1..14}`, `{body_1..12}`, `{url_1..6}`, `{embed_1}`. `heading_1` eyebrow, `heading_2` H2; `embed_1` = the chips' `<button data-filter="…">` markup; card n = `heading_(2n+1)` category, `heading_(2n+2)` title, `body_(2n-1)` line, `body_(2n)` label, `url_n` |
| **Globals** | 31 native `__globals__` refs · 6 `var(--e-global-color-gfnavy)` (labels) |
| **Unmapped colours** | `#F6F8FB`, `#0F1620`, `#DCE1EA`, card shadows; the chips' own colours (`#F5821F`, `#15253D`, `#6B7280`, `#DCE1EA`) live in the html widget's scoped `<style>` |
| **Notes** | **Behaviour-tested, not just screenshotted** (AUDIT.md B15): on 12298, Sales → 3 cards, HR → 1, Engineering → 1, All → 6, `aria-pressed` tracks the active chip. The script matches a chip's `data-filter` (the lower-cased label) against each card's first heading, so categories are content, not classes. **It must query the cards at click time**: the widget's script runs before the grid below it exists, and a load-time query made the filter inert on iteration 1. Cards stay native, editable widgets (the zip's CLAUDE.md "JS only shows/hides" rule). **Verified** (iteration 2): section 719 = design, chips 36px tall = design, cards 371×162 / 371×185, word-for-word text match. |

### faq-accordion-filter-10
| | |
|---|---|
| **Snippet** | `reference/snippets/faq-accordion-filter-10.json` |
| **Source** | post `12300` (`pl-auto-faqs`, type `page`) section index `1` — minted by run 20260924-125928 (§7) |
| **Used by** | 12300 at index 1 |
| **Signature** | `6667f3c965` (sha256 of the elType/widgetType tree, first 10 hex) · 14 containers + 21 widgets · 69,140 bytes |
| **Recognise when** | A white section holding a **narrow (~880px) column** with **no heading**: a centred row of category **filter chips**, then a flat list of **exactly 10** questions separated by hairlines, each a bold navy question with a **28px outlined "+" circle** on the right that rotates to "×" and turns the question orange when open; answers are plain paragraphs. Discriminators: against `faq-toggle`, no left rail (eyebrow + H2 + intro + CTA) and it has chips; against `text-link-cards-6-filter`, questions not cards. |
| **Structure** | `container:full bg=gfwhite pad 80/24` → `container:boxed` → column `container` width 832 → `html` chips widget (as `text-link-cards-6-filter`, margin-bottom 28) → list `container` (top hairline) → 10 × item `container` (`css_classes: pl-filter-card`, bottom hairline) → `heading` category (`display:none`) + `toggle` (one tab; FA plus/minus icon kept only so Elementor renders `.elementor-toggle-icon`, glyphs hidden, circle drawn in CSS) |
| **Tokens** | 31 placeholders: `{embed_1}` chips, `{heading_1..10}` item categories, `{faq_q_1..10}`, `{faq_a_1..10}` (answers are HTML) |
| **Globals** | 1 native `__globals__` ref (section bg) · 40 `var(--e-global-color-*)` in the toggles' `custom_css` (`gfnavy` title, `gforange` active title + "+", `gfink` answer) |
| **Unmapped colours** | `#DCE1EA` (hairlines, circle border); the chips' colours live in the html widget |
| **Notes** | **A category is a hidden heading whose text equals a chip label** ("Ordering", "Technical"), so the shared chip script filters questions exactly as it filters cards. **An empty `selected_icon` makes Elementor omit the icon element**: iteration 1 rendered no circle and 65px rows (design 73). **Behaviour-tested on 12300** (iteration 2): Technical 4 / Ordering 6 / All 10; a question opens to 121px (73 + a 48px answer) with the circle rotated to "×". Rows 73px = design, section 955 = design; text matches the design except the 10 hidden category words. |

### split-list-figure
| | |
|---|---|
| **Snippet** | `reference/snippets/split-list-figure.json` |
| **Source** | post `12301` (`pl-auto-quality-policy`, type `page`) section index `1` — minted by run 20260924-125928 (§7) |
| **Used by** | 12301 at index 1 |
| **Signature** | `d650f3c81d` (sha256 of the elType/widgetType tree, first 10 hex) · 6 containers + 5 widgets · 18,111 bytes |
| **Recognise when** | A white two-column section, **top-aligned**: **left**, orange eyebrow + H2 + a check-list (bordered item cards with orange checks) and **no paragraph**; **right**, a **document-style figure** — the image inset 18px inside a white rounded frame with a soft shadow — with a small grey centred **caption** under it. Discriminators: against `split-prose-list-media`, no paragraph, the image is inset (not full-bleed in a dark frame), a caption, and top alignment. |
| **Structure** | `container:full bg=gfwhite pad 80/24` → `container:boxed` → row (`flex_align_items:flex-start`, gap 72) → prose `container` (eyebrow mb 20, `heading h2` mb 18, `text-editor` list) + figure `container` → frame `container` (bg `gfwhite`, pad 18, border, radius 18, shadow) → `image` ; `heading` caption (13px, `#65718A`, margin-top 12) |
| **Tokens** | 5 placeholders: `{heading_1}` eyebrow, `{heading_2}` H2, `{body_1}` list (`<ul><li>…</li></ul>`, count free), `{image_1}`, `{heading_3}` caption |
| **Globals** | 4 native `__globals__` refs · 1 `var(--e-global-color-gfink)` (list text) |
| **Unmapped colours** | `#0F1620` (H2), `#65718A` (caption), `#DCE1EA` (borders), `rgba(15,42,68,.12)` (shadow) |
| **Notes** | **Verified on 12301** (iteration 1): section 879 = design; list items 540×111/60/60/85 = design; certificate 502×650 = design; caption 540×20 = design; word-for-word text. |

### check-list-centered
| | |
|---|---|
| **Snippet** | `reference/snippets/check-list-centered.json` |
| **Source** | post `12301` (`pl-auto-quality-policy`, type `page`) section index `2` — minted by run 20260924-125928 (§7) |
| **Used by** | 12301 at index 2 |
| **Signature** | `a89d9c9dc6` (sha256 of the elType/widgetType tree, first 10 hex) · 4 containers + 3 widgets · 10,151 bytes |
| **Recognise when** | A light-grey section with a **centred** eyebrow + H2 (no lede) and, below it, **one check-list** in a ~900px column — bordered white item cards with orange checks — and nothing else. |
| **Structure** | `container:full bg=#F6F8FB pad 80/24` → `container:boxed` column centred → head (as `icon-cards-3`) → `container` width 852 → `text-editor` list |
| **Tokens** | 3 placeholders: `{heading_1}` eyebrow, `{heading_2}` H2, `{body_1}` list (count free) |
| **Globals** | 2 native `__globals__` refs · 1 `var(--e-global-color-gfink)` |
| **Unmapped colours** | `#F6F8FB`, `#0F1620`, `#DCE1EA` |
| **Notes** | **Verified on 12301** (iteration 1): section 640 = design; items 852×85/85/85/60 = design. |

### hero-split-contact-form
| | |
|---|---|
| **Snippet** | `reference/snippets/hero-split-contact-form.json` |
| **Source** | post `12302` (`pl-auto-contact`, type `page`) section index `0` — minted by run 20260924-125928 (§7) |
| **Used by** | 12302 at index 0 |
| **Signature** | `89e2db97a9` (sha256 of the elType/widgetType tree, first 10 hex) · 5 containers + 6 widgets · 26,490 bytes |
| **Recognise when** | The page's opening section on dark navy with a faint 32px grid (no glows), **wide (≈1392px) and split**: left, a white uppercase eyebrow, a very large H1 (~64px, may carry a `<br>` and an orange accent word), a lede and **two** CTAs (orange pill + white-outlined ghost); right, a **white contact form card** — orange kicker, H2, a "Fields marked * are required" line, then first/last name, email/phone, company/website (in pairs), a message textarea and one "Send message" button with a small note beside it. Discriminators: against `quote-form-hubspot`, this sits in the hero, has no timeline, no upload and no two-step indicator; against `hero-dark-stat-strip`, a form instead of stats. |
| **Structure** | `container:full bg=gfnavydp pad 72/24/56` + grid `custom_css` → `container:boxed` (`boxed_width` 1392, row, gap 64) → left `container` (`calc((100% - 64px) * .55)`: `heading` eyebrow, `heading h1` with `.pl-accent`, `text-editor` lede, button row) + right `container` (`* .45`) → ONE `html` widget: scoped `<style>`, the card markup, and the submit `<script>` |
| **Tokens** | 27 placeholders: `{heading_1..20}`, `{body_1..2}`, `{button_1..3}`, `{url_1..2}`. Inside the html widget (plain text, like `quote-form-hubspot`): `heading_1` kicker, `heading_2` card title, `body_1` required-fields line (carries `<em>*</em>`), `heading_3` success message, `heading_4..15` field labels + placeholders in pairs, `heading_16/17` message label/placeholder, `button_1` submit, `heading_18` note; then the left column: `heading_19` eyebrow, `heading_20` H1, `body_2` lede, `button_2/3` + `url_1/2` CTAs |
| **Globals** | 6 native `__globals__` refs · 1 `var(--e-global-color-gforange)` (H1 accent) |
| **Unmapped colours** | `rgba(255,255,255,0.78)` (lede), `rgba(255,255,255,0.32)` (ghost border); form colours in its scoped `<style>` (`#0F1620`, `#65718A`, `#DCE1EA`, `#9AA4B5`, success `#15803D`/`#EFFAF3`, error `#B91C1C`/`#FEF2F2`, focus orange) |
| **Notes** | **Wired, not decorative:** posts to the HubSpot Forms API v3, portal `143181153`, form **`[Potomac] Contact Form`** `54d0ec75-106d-43eb-a420-0ff22e448e6d` (reference/HUBSPOT-FORMS.md, feed #18): `email`, `firstname`, `lastname`, `phone`, `company`, `website`, `potomac_message`, plus `hs_lead_status: NEW` and UTM; `context` carries `pageName`, `pageUri` and `hutk`; analytics `lead_form_*` with no PII values. The design's own handler only faked success. **Behaviour-tested short of sending** (12302): an empty submit and a bad email each show the in-card error, and nothing is posted. **Not yet proven end-to-end**: a live test submission creates a real HubSpot contact, so it needs a human go-ahead (HUBSPOT-FORMS.md §Verifying). Only the widget's own plain-text slots are `heading_*`; a `body_*` there fails the validator (it expects block markup) — the first tokenisation made that mistake and was replaced before commit. **Verified** (iteration 2): section 808 = design, card 598×680 = design, inputs 254×44, textarea 524×96. |

### hq-panel-map
| | |
|---|---|
| **Snippet** | `reference/snippets/hq-panel-map.json` |
| **Source** | post `12302` (`pl-auto-contact`, type `page`) section index `1` — minted by run 20260924-125928 (§7) |
| **Used by** | 12302 at index 1 |
| **Signature** | `b00612bb21` (sha256 of the elType/widgetType tree, first 10 hex) · 7 containers + 4 widgets · 20,853 bytes |
| **Recognise when** | A white section with **two equal-height panels side by side**: left, a dark navy card (faint grid) with an orange dot + uppercase "Headquarters"-style flag, a white city heading and **3 contact lines** (address, phone, email) with orange icons and hairlines between them; right, a slightly wider rounded **map embed**. |
| **Structure** | `container:full bg=gfwhite pad 80/24` → `container:boxed` → row (stretch, gap 24) → panel `container` (`gfnavydp`, pad 30, radius 16, `flex:1`, grid `::before`) → flag row (7px dot + `heading`) mb 11, `heading h3` city mb 20, `icon-list` (3 items, 11px padding, hairlines) ; map `container` (`flex:1.3`, border, radius 16) → `html` iframe (min-height 260) |
| **Tokens** | 8 placeholders: `{heading_1}` flag, `{heading_2}` city, `{heading_3..5}` the three lines (the address may carry `<br>`), `{url_1..2}` phone / email links, `{embed_1}` the map `<iframe>` |
| **Globals** | 5 native `__globals__` refs · 2 `var(--e-global-color-gforange)` |
| **Unmapped colours** | `rgba(255,255,255,0.86)` (lines), `rgba(255,255,255,.1)` (hairlines), `#DCE1EA` (map border) |
| **Notes** | Icons are Font Awesome (`map-marker-alt`, `phone`, `envelope`) in a native `icon-list`, standing in for the design's inline SVGs, so the lines stay editable. The flag's bottom margin is 11 (6 + its 24px line box; iteration 1 was 5px short). **Verified on 12302** (iteration 2): section 462 = design; lines 463×69 / 46 / 46 = design; map 603×295 against 603×300. |

### offices-grid-6-social
| | |
|---|---|
| **Snippet** | `reference/snippets/offices-grid-6-social.json` |
| **Source** | post `12302` (`pl-auto-contact`, type `page`) section index `2` — minted by run 20260924-125928 (§7) |
| **Used by** | 12302 at index 2 |
| **Signature** | `dcdaf0b0cd` (sha256 of the elType/widgetType tree, first 10 hex) · 11 containers + 18 widgets · 68,870 bytes |
| **Recognise when** | A light-grey section with a **left-aligned** head (eyebrow + H2 + one grey lede), a **2-column** grid of **5 office cards** (city + an address line and a phone line, each with an orange icon) and **one highlighted card** in an orange tint ("Can't find your region?" + a line + an outlined button), then a "Follow us" row of **4 circular social icons**. |
| **Structure** | `container:full bg=#F6F8FB pad 80/24` → `container:boxed` → head `container` (width 760, mb 40) → card row (`calc((100% - 18px)/2)`, gap 18, stretch) → 5 × office `container` (pad 26/24, border, radius 8, hover lift + orange left bar) → `heading h3` + `icon-list` (2 items) ; 1 × region `container` (`#FEF9F5`, border `#F9B067`) → `heading h3` + `text-editor` + `button` ; social row → `heading` + `social-icons` (4) |
| **Tokens** | 32 placeholders: `{heading_1..19}`, `{body_1..2}`, `{button_1}`, `{url_1..10}`. Head = `heading_1` eyebrow, `heading_2` H2, `body_1` lede; office n = `heading_(3n)` city, `heading_(3n+1)` address, `heading_(3n+2)` phone, `url_n` tel link; region card = `heading_18`, `body_2`, `button_1`, `url_6`; `heading_19` "Follow us"; `url_7..10` social links |
| **Globals** | 10 native `__globals__` refs · 26 `var(--e-global-color-*)` (`gforange` icons/bars/hover, `gfink` text) |
| **Unmapped colours** | `#0F1620`, `#65718A`, `#DCE1EA`, `#C3CBD8`, `#FEF9F5` (region tint), `#F9B067` (region border) |
| **Notes** | Social icons are the native `social-icons` widget (Instagram, Facebook, LinkedIn, X); their screen-reader labels come from the icon names ("facebook-f") rather than the design's aria-labels — a small accessibility regression to fix by hand if it matters. **Verified on 12302** (iteration 2): section 947 = design, cards 567×147 / 567×190 = design, social circles 40×40 = design. |

### hero-dark-centered-meta-4
| | |
|---|---|
| **Snippet** | `reference/snippets/hero-dark-centered-meta-4.json` |
| **Source** | post `12357` (`pl-auto-project-gallery`, type `page`) section index `0` — minted by run 20260924-125928 (§7) |
| **Used by** | 12357 at index 0 |
| **Signature** | `ccd9ca296e` (sha256 of the elType/widgetType tree, first 10 hex) · 7 containers + 11 widgets · 28,520 bytes |
| **Recognise when** | As `hero-dark-centered-meta` (dark navy grid + glows, centred eyebrow + H1 + lede, no buttons) but with **exactly 4** meta stats in a tighter row (28px gaps), a **white** eyebrow and a narrower H1 (18ch). With 3 stats it is `hero-dark-centered-meta`. |
| **Structure** | as `hero-dark-centered-meta`: outer `gfnavydp` + grid/glow → boxed 1200 → eyebrow, `heading h1` (margin 43/0/18, `max-width:18ch`), `text-editor` lede (`p` max 704), meta row (gap 28, margin-top 32) → 4 × stat `container` (value + label) |
| **Tokens** | 11 placeholders: `{heading_1}` eyebrow, `{heading_2}` H1, `{body_1}` lede, `{heading_3..10}` stat value/label pairs |
| **Globals** | 7 native `__globals__` refs (`gfnavydp`, `gfwhite` ×6) · 0 CSS-var rewrites |
| **Unmapped colours** | `rgba(255,255,255,0.74)`, `rgba(255,255,255,0.55)`, grid/glow stops |
| **Notes** | The first stat ("54 projects shown") is static copy; the gallery's own runtime count is the separate "Showing N projects" line. **Verified on 12357** (iteration 2): section 513 = design. |

### gallery-grid-filter-lightbox
| | |
|---|---|
| **Snippet** | `reference/snippets/gallery-grid-filter-lightbox.json` |
| **Source** | post `12357` (`pl-auto-project-gallery`, type `page`) section index `1` — minted by run 20260924-125928 (§7) |
| **Used by** | 12357 at index 1 |
| **Signature** | `47adfb8371` (sha256 of the elType/widgetType tree, first 10 hex) · 112 containers + 164 widgets · 529,946 bytes |
| **Recognise when** | A project gallery: a **sticky, full-width white filter bar** ("Filter" label + wrapping category chips, each with a count pill, "All" first and orange when active), a small "Showing N projects" line, then a **3-column grid of 54 image cards** (4:3, 7px radius, image slightly zoomed) whose category badge + title appear on **hover**, and a **lightbox** that opens on click with the image, category, title, an "N / M" counter, prev/next, and two CTAs. |
| **Structure** | `container:full bg=gfwhite` → bar `container` (full width, `rgba(255,255,255,.92)`, bottom hairline, `position:sticky`) → ONE `html` widget: bar markup (`{embed_1}` chips), the lightbox markup, scoped `<style>`, script ; boxed 1200 `container` (pad 40/24/80) → `text-editor` count (`.pl-gal-count`) + card row (`calc((100% - 36px)/3)`, gap 18; 2-up ≤760, 1-up ≤460) → 54 × card `container` (`css_classes: pl-gal-card`, bg `#ECEFF4`, radius 7, `overflow:hidden`) → `image` (4:3 cover, `scale(1.2)`) + overlay `container` (absolute, gradient, opacity 0 → 1 on hover) → `heading` category badge + `heading h3` title |
| **Tokens** | 168 placeholders: `{image_1..54}`, `{heading_1..111}`, `{body_1}`, `{embed_1}`, `{url_1}`. `heading_1` "Filter", `heading_2/3` lightbox CTA labels, `url_1` their link, `embed_1` the chips' `<button data-filter>` markup (label + count), `body_1` the count line; card n = `image_n`, `heading_(2n+2)` category, `heading_(2n+3)` title; `heading_111`… see legend |
| **Globals** | 109 native `__globals__` refs (`gfwhite`) · 0 CSS-var rewrites (the bar/lightbox colours live in the html widget) |
| **Unmapped colours** | `#ECEFF4` (card backdrop), `rgba(14,99,168,.92)` (category badge — design value), overlay gradient `rgba(11,26,44,…)`; chips/lightbox colours in the widget's `<style>` |
| **Notes** | **Behaviour-tested** (12357 iteration 2): Metal Micromachining → 8 and "Showing 8 projects", Diamond → 2, All → 54; a click opens the lightbox on that card ("2 / 2", category, title, image); next steps within the filtered set; Esc closes it and restores page scroll; CTA links resolve. **Scope rule:** the script must scope to the page section — the element whose parent carries `data-elementor-id` — **not** `closest(".e-parent")`, which stops at the bar's own container and left filter and lightbox inert on iteration 1. The lightbox is moved to `<body>` so `position:fixed` escapes any transformed ancestor. The chip counts are static copy in `{embed_1}` — keep them in step with the cards. Cards are native widgets (editable); the design's duplicate `PROJECTS` JS array is not used. Geometry: cards 388×291 = design, images 466×349 (the 1.2 crop) = design; section 26px taller than the design's filter bar + grid (5882 vs 5856). |

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
