# HubSpot forms — wiring contract

How a built page gets a submission into HubSpot. Established from the live configuration on
2026-08-06, not from memory: every GUID and property name below was read out of the site.

## Portals

| Portal | What it is | Where it appears |
|---|---|---|
| **143181153** | The portal every form on this site targets — Gravity Forms HubSpot add-on `portal_id`, all five interactive funnels, Code Snippets #5 and #17 | authoritative for form submissions |
| 677962 | `leadin_portalId`, the HubSpot WordPress plugin (tracking/chat) | **suspect** — if the on-page tracking script belongs to 677962, the `hubspotutk` cookie forwarded with submissions will not resolve against 143181153 and first-touch attribution is silently lost. Unresolved (AUDIT.md B11) |
| **145800879** | The **sandbox**, per the project owner | **referenced nowhere on this site** — verified by sweeping 12,969 files under `wp-content` plus every option, postmeta, post_content, snippet and GF feed |

## The forms

Do **not** delete or edit these HubSpot forms. Build against them as they are.

| Form | GUID | Reached today via |
|---|---|---|
| `[Potomac] Start a Project` | `9dba7d36-e36b-4a10-9411-9dc073dab7a0` | GF form #2 → feed #19 (add-on, OAuth) |
| `[Potomac] Contact Form` | `54d0ec75-106d-43eb-a420-0ff22e448e6d` | GF form #1 → feed #18 |
| `[Potomac] Subscribe - Newsletter` | `986597b1-ebce-4c39-98ac-ccfe1a21398d` | GF form #5 → feed #20 |

A **fourth**, bespoke form is used by the five interactive funnels and is not one of the above:
`9eb36566-4364-4467-8592-15c743bdc901`. New work must not use it. Whether it still exists inside
143181153 is unverified — if it was created in the sandbox, those funnels are dropping submissions
today, and they are embedded by 38 posts. Open question for a human.

## Property names — read from the live GF feeds

These are contact-property internal names. The v3 submit endpoint **rejects the entire submission**
if it carries a field the target form does not have, so send only these.

**`[Potomac] Start a Project`** (feed #19):

| Property | Source on the new quote section |
|---|---|
| `email` | Email * |
| `firstname` / `lastname` | "Your name" split on the first space |
| `company` | Organisation |
| `phone` | not collected by this design — omit |
| `potomac_project_name` | derive, e.g. `Rapid Response Quote — <page title>`, so the record is identifiable |
| `potomac_project_description` | Part description **plus** the folded step-2 values (see below) |
| `potomac_file_submission` | public URL returned by the upload endpoint |
| ~~`potomac_second_file_submission`~~ / ~~`potomac_third_file_submission`~~ | **not used** — single upload only |

Always also send `hs_lead_status: NEW`; the feeds set lifecycle `lead`.

**`[Potomac] Contact Form`** (feed #18): `email`, `firstname`, `lastname`, `phone`, `company`,
`website`, `potomac_message`.

### Folding step 2

The design's step 2 collects **Tolerance** and **Quantity**. Neither has a HubSpot property, and the
form may not be edited, so they are appended to `potomac_project_description` as labelled lines
rather than sent as fields — sending them would 400 the whole submission.

## Submission mechanism — direct Forms API, not Gravity Forms

```
POST https://api.hsforms.com/submissions/v3/integration/submit/143181153/<form-guid>
Content-Type: application/json

{ "fields": [ { "objectTypeId": "0-1", "name": "<property>", "value": "<string>" }, … ],
  "context": { "pageName": …, "pageUri": …, "hutk": <hubspotutk cookie> } }
```

Mirror the working implementation in `novamira-drafts/*-interactive.html` (`submitToHubSpot`), which
has run against this portal since July: it sets `hs_lead_status`, merges UTM, drops empty values,
maps to `objectTypeId:'0-1'`, sends `context`, and reports in-situ rather than with `alert()`.

- **UTM** — querystring on first load, persisted as `cnc_utm_first` / `cnc_utm_last` in
  `localStorage`, merged into `fields` on submit.
- **`hutk`** — `document.cookie` match on `hubspotutk`. See the 677962 caveat above.
- **Analytics** — `lead_form_{start,field,submit,submit_success,submit_error}` to GA4
  `G-MQSBBH2M4J`; PII sends `field_filled` only, never the value.
- **File upload** — POST the file to the existing `/wp-json/cnc-quote/v1/upload` (Code Snippet #12),
  take the returned public URL, pass it as `potomac_file_submission`. HubSpot re-hosts it. Do not
  build a second upload endpoint.
- **Not an iframe.** The funnels are iframes because a `position:fixed` drawer gets clipped
  mid-page; a form needs no overlay, so build it as one Elementor `html` widget. WindPress compiles
  Tailwind classes in rendered DOM, which includes `html` widgets but **not** iframe documents — so
  the widget route also keeps the design's classes working.

## Verifying a wiring

The v3 endpoint names an offending field precisely on 400, so one submission settles whether the
property list is right. Project convention (HANDOFF Stage H) is: submit **one** test with a
deliverable address, confirm the contact and its properties, then archive it. That creates a real
contact in a live portal, so it needs a human's go-ahead each time.
