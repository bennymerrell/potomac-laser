# Service drafts vs current designs — comparison, 2026-09-24

**Read-only.** Nothing on the site was changed. The only write was one new file,
`novamira-drafts/compare-services-20260924/draft-text.json`: the drafts' rendered text per section, used for the diff.

**Compared:**
- **Drafts:** 12239 CNC, 12240 Laser Micromachining, 12241 Micro-Hole Drilling, 12242 Rapid Prototyping and 12243 3D
  Printing. All are drafts built 2026-08-06 (runs 20260806-124030 and -173742) from the previous zip revision, and are
  stamped with the old paths (`CNC Micromachining.html` …).
- **Designs:** `Services - *.html` from the current zip (`fab7225c…`), rendered in the user's Chrome because they need the
  Tailwind Play CDN and React.
- **How:** section heights were measured in the browser. Text was diffed per section after normalising the brand name,
  dashes, arrows and extraction whitespace.
- **Width:** drafts were measured at a 1629px viewport (the site's zoom) and designs at 1792px. The design's content column
  is a fixed 1260px; applying CSS zoom did not change its `offsetHeight`, so the heights compare directly.

## Summary

**Same 12-section skeleton, in the same order, on all five pages.** The design itself changed in five ways since the
drafts were built:

1. **The application explorer is now inline.** There are 12 `[data-app-panel]` blocks (~1,900 words), where the drafts
   embed the old `*-interactive.html` in an iframe. This is the refresh that was already decided on. Note that the
   manifest comment says 13 panels; this count found 12.
2. **The quote section is a two-step form.** Step 1 asks for first name, last name, company, email, a part description and
   a file. Step 2 asks for tolerance (±10 µm / ±5 µm / sub-5 µm), quantity and a file. The drafts carry the 5-field
   `quote-form-hubspot`, and the HubSpot wiring would have to be extended for the new fields and the file upload.
3. **Two new page-wide features:**
   - a **"Material + Machining Basket"** side panel (material, machining requirements, tolerance, quantity, drawing,
     optional testing and validation)
   - a **materials drawer** (Kapton, polymers and others; form, size, quantity; "supplied by Goodfellow Materials")
   Both are wired through `data-basket` hooks (29 per page). The "Request a quote" buttons became **"Request material +
   machining quote"** on LM, MHD, RP and 3DP (hero, why-us, comparison and group); CNC already used that label. No library
   pattern covers either panel, and the design's handlers submit nowhere, so they would need a backend (HubSpot or
   otherwise) before they could ship.
4. **Restyle.** Larger type (H2 40–50px vs 31–36px in the drafts), a 1260px content column (most draft sections run
   1517px at this viewport; two are capped at 1224), and different section padding.
   - The drafts are **3,100–4,000px taller** per page.
   - Excluding the explorer, they are ~1,800px taller: why-us +170–218, capabilities +259–303, comparison +209–233,
     group +122–140, testimonials +121–145, and the quote section **+743**.
   - The closing band is a third variant (96px padding, 62px H2, 519px; 582px on LM). It is neither `cta-band-dark` (463,
     used on CNC/LM/MHD) nor `cta-band-dark-display` (453).
5. **Copy (Content Style Rules pass):** most em/en dashes are gone. The drafts have 22–33 per page and the designs 6–9.
   The "→" arrows were **not** removed (17–23 per page in the design sections vs 14–15 in the drafts), so they stay a
   breach to report upstream, as before.

## Section heights (draft / design, px)

| Section | CNC 12239 | LM 12240 | MHD 12241 | RP 12242 | 3DP 12243 |
|---|---|---|---|---|---|
| 0 Hero | 968 / 947 (+21) | 1045 / 947 (+98) | 1062 / 890 (+172) | 1021 / 854 (+167) | 1021 / 839 (+182) |
| 1 Why us | 1183 / 965 (+218) | 1183 / 990 (+193) | 1135 / 965 (+170) | 1135 / 965 (+170) | 1135 / 965 (+170) |
| 2 Services | 798 / 788 (+10) | 798 / 787 (+11) | 798 / 788 (+10) | 798 / 788 (+10) | 798 / 788 (+10) |
| 3 Explorer | 2387 / 1048 (+1339) | 3200 / 1046 (+2154) | 3144 / 1048 (+2096) | 3119 / 1048 (+2071) | 3144 / 1048 (+2096) |
| 4 Capabilities | 1061 / 802 (+259) | 1181 / 878 (+303) | 1061 / 802 (+259) | 1061 / 802 (+259) | 1085 / 826 (+259) |
| 5 Comparison | 1099 / 866 (+233) | 1075 / 865 (+210) | 1075 / 866 (+209) | 1075 / 866 (+209) | 1075 / 866 (+209) |
| 6 Process | 724 / 682 (+42) | 724 / 703 (+21) | 724 / 682 (+42) | 722 / 682 (+40) | 746 / 682 (+64) |
| 7 Group | 807 / 667 (+140) | 807 / 684 (+123) | 807 / 685 (+122) | 807 / 685 (+122) | 807 / 685 (+122) |
| 8 Testimonials | 575 / 430 (+145) | 551 / 429 (+122) | 551 / 430 (+121) | 551 / 430 (+121) | 551 / 430 (+121) |
| 9 Quote | 1621 / 878 (+743) | 1621 / 877 (+744) | 1621 / 878 (+743) | 1621 / 878 (+743) | 1621 / 878 (+743) |
| 10 FAQ | 726 / 680 (+46) | 726 / 679 (+47) | 726 / 680 (+46) | 726 / 680 (+46) | 726 / 680 (+46) |
| 11 Closing band | 463 / 519 (−56) | 463 / 582 (−119) | 463 / 519 (−56) | 505 / 519 (−14) | 505 / 519 (−14) |
| **Total** | 12412 / 9272 (+3140) | 13374 / 9467 (+3907) | 13167 / 9233 (+3934) | 13141 / 9197 (+3944) | 13214 / 9206 (+4008) |

The Services section (2) is the only one within ~10px everywhere.

## Copy differences (after normalisation)

Only a few real copy changes remain, and they repeat across the pages:

- **All five heroes:** the design adds "No redesign required to start, we'll help optimise your part." under the CTAs.
  The drafts already carry the sentence in why-us, comparison and quote; only the hero is new.
- **LM, MHD, RP, 3DP:** the "Request a quote" labels become "Request material + machining quote", in 4 places per page.
- **Quote section:** the new two-step copy ("Step 1 Tell us about your part", "2 Complete", First name / Last name /
  Company, the tolerance options). The drafts read "Organisation" and have a single step.
- **CNC FAQ:** "…add it to your **basket**" where the draft says "quote request".
- **Defect in the drafts: RP 12242 and 3DP 12243 FAQs still say "Potomac"** (6 and 7 times, present tense). The design
  now reads "Goodfellow Microfabrication", and the other three drafts were normalised.
- **Everything else is word-for-word the same** once dashes are normalised: why-us, services, capabilities, comparison,
  process, group, testimonials, and the other FAQ answers.

## What a refresh would involve (for the supervised job)

- **Needs new §7 patterns:**
  - the inline explorer (12 panels, the largest section)
  - the two-step quote form (with new HubSpot fields and a file upload)
  - the basket panel and materials drawer, plus the backend decision above
  - the service-page closing band variant
- **Rebuild the rest from the current design:** hero, why-us, capabilities, comparison, group, testimonials and FAQ keep
  their structure, but the restyle means the existing fragments do not match the design's geometry. They need either
  restyled variants or a re-extraction from the new design.
- **Unchanged and reusable:** the Services section (`services-image-cards`) and the process steps (~20–60px off, mostly
  type scale).
- **Also at refresh time:** re-stamp `_pl_auto_page` to the `Services - *.html` paths (already decided), fix the RP/3DP FAQ
  brand text, and report the remaining arrows and dashes to the designer.
