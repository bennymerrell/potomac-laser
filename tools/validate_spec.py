#!/usr/bin/env python3
"""Validate a spec.yaml against the fragment library before any WordPress write.

Implements the checks in reference/SPEC-FORMAT.md, which back the potomac-elementor
skill's §2/§3 gates. Nothing here touches WordPress — malformed input is caught on
this side of the wire.

    tools/validate_spec.py path/to/spec.yaml
    tools/validate_spec.py reference/spec.example.yaml --template

Exit 0 = all gates pass. Exit 1 = at least one error. Warnings never fail the run.

Requires PyYAML.
"""

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNIPPETS = os.path.join(REPO, "reference", "snippets")

TOKEN_RE = re.compile(r"\{([a-z_]+_\d+)\}")
HONORIFICS = {"dr", "dr.", "prof", "prof.", "mr", "mr.", "ms", "ms.", "mrs", "mrs."}

# SKILL.md §1. Post type follows what the page IS, because it decides the permalink and
# the theme template: a service page is `post_services` (/services/<slug>/), an
# application or sector page is `post_application`, and `page` is everything else. All
# three are in `elementor_cpt_support`, so "Edit with Elementor" works on any of them.
ALLOWED_POST_TYPES = {"page", "post_services", "post_application"}
# Automation-built posts carry a provenance stamp; the slug is namespaced so the run's
# drafts never collide with live pages (AUDIT.md B5).
AUTO_SLUG_PREFIX = "pl-auto-"

# Structural properties of the fragments, from the legend analysis. These cannot be
# derived from a new spec's copy, so they are declared.
MIRRORED_TITLES = {  # both headings render the same card title (one is mobile/hover)
    "process-comparison-cards": [(3, 4), (6, 7), (9, 10)],
}
DERIVED_INITIALS = {  # (initials_token_n, name_token_n)
    "testimonials-avatar-cards": [(4, 5), (8, 9), (12, 13)],
}
REQUIRED_OPTIONS = {  # pattern -> (option, min, max)
    "group-ecosystem-cards": ("you_are_here_unit", 1, 4),
    "process-steps-numbered": ("highlight_step", 1, 5),
}
HTML_TOKENS = ("body_", "faq_a_")

# Patterns whose tokens substitute INSIDE a single `html` widget rather than filling one
# text-editor per token. Their body_* values are plain text by design, so the HTML-slot
# check below does not apply — it exists to catch legend-sourced values that lost their
# block wrapper (AUDIT.md B9), which cannot happen here.
EMBED_TEXT_PATTERNS = {"quote-form-hubspot"}

# Design-time scaffolding a Claude Design export ships and a live page must never load:
# the Tailwind Play CDN, React/ReactDOM dev builds, Babel standalone, the tweaks panel.
# TRANSLATE.md §2 strips these; this is the mechanical backstop (SKILL.md §2 gates the
# assembled JSON too). No fragment needs an external asset, so any off-site dependency in a
# token value is scaffolding that leaked through.
SCAFFOLDING_RE = re.compile(
    r"cdn\.tailwindcss\.com|unpkg\.com|@?babel/standalone|tweaks-panel|tweaks-root", re.I)
TEMPLATE_LITERAL_RE = re.compile(r"\$\{[^}\n]{1,80}\}")
EXTERNAL_DEP_RE = re.compile(
    r"""<script[^>]+src=["'](?:https?:)?//|<link[^>]+rel=["']stylesheet["'][^>]+href=["'](?:https?:)?//""",
    re.I)


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")


def fragment_tokens(pattern):
    """Every {token} physically present in a fragment."""
    path = os.path.join(SNIPPETS, f"{pattern}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return set(TOKEN_RE.findall(fh.read()))


def plausible_initials(name):
    """Initial forms we accept as 'derived from' a name."""
    words = [w for w in re.split(r"[\s]+", name.strip()) if w]
    words = [w for w in words if w.lower() not in HONORIFICS]
    letters = [w[0].upper() for w in words if w[:1].isalpha()]
    if not letters:
        return set()
    out = {"".join(letters)}
    if len(letters) > 2:
        out.add(letters[0] + letters[-1])  # first + last only
    return out


def check_page(spec, rep, automation=False):
    page = spec.get("page")
    if not isinstance(page, dict):
        rep.error("page", "missing or not a mapping")
        return
    for key in ("title", "slug"):
        if not page.get(key):
            rep.error("page", f"`{key}` is required and must be non-empty")
    if page.get("post_type") not in ALLOWED_POST_TYPES:
        rep.error("page", f"post_type must be one of {sorted(ALLOWED_POST_TYPES)} (SKILL.md §1), "
                          f"got {page.get('post_type')!r}")
    if page.get("post_status") != "draft":
        rep.error("page", f"post_status must be `draft` (SKILL.md §1, §8), got {page.get('post_status')!r}")
    slug = page.get("slug") or ""
    if slug and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        rep.warn("page", f"slug {slug!r} is not lowercase-hyphenated")
    if automation and slug and not slug.startswith(AUTO_SLUG_PREFIX):
        rep.error("page", f"an automation run must namespace its slug {AUTO_SLUG_PREFIX!r} "
                          f"(AUDIT.md B5) so the draft cannot collide with a live page and WP "
                          f"cannot silently suffix it: got {slug!r}")
    if not automation and slug.startswith(AUTO_SLUG_PREFIX):
        rep.warn("page", f"slug carries the {AUTO_SLUG_PREFIX!r} automation prefix on a "
                         f"hand-run spec — intentional?")


def check_assets(spec, rep, template):
    assets = spec.get("assets") or {}
    if not isinstance(assets, dict):
        rep.error("assets", "must be a mapping")
        return {}
    for key, val in assets.items():
        where = f"assets.{key}"
        if not isinstance(val, dict):
            rep.error(where, "must be a mapping with attachment_id and url")
            continue
        aid = val.get("attachment_id")
        if not isinstance(aid, int) or aid <= 0:
            (rep.warn if template and aid == 0 else rep.error)(
                where, f"attachment_id must be a non-zero int (SKILL.md §3 gate), got {aid!r}")
        if not val.get("url"):
            rep.error(where, "url is required")
    return assets


def check_section(idx, sec, assets, rep, template):
    where = f"sections[{idx}]"
    if not isinstance(sec, dict):
        rep.error(where, "must be a mapping")
        return
    pattern = sec.get("pattern")
    if not pattern:
        rep.error(where, "`pattern` is required")
        return
    where = f"sections[{idx}] {pattern}"

    frag = fragment_tokens(pattern)
    if frag is None:
        rep.error(where, f"no fragment at reference/snippets/{pattern}.json")
        return

    tokens = sec.get("tokens")
    if not isinstance(tokens, dict):
        rep.error(where, "`tokens` is required and must be a mapping")
        return

    for key in set(sec) - {"pattern", "tokens", "options"}:
        rep.warn(where, f"unknown section key {key!r} (ignored by the assembler)")

    # --- check 4: token coverage, both directions ---
    supplied = set(tokens)
    missing = frag - supplied
    extra = supplied - frag
    if missing:
        rep.error(where, f"fragment tokens with no spec key -> would ship literal "
                         f"{{token}} to the page: {sorted(missing)}")
    if extra:
        rep.error(where, f"spec keys with no fragment slot -> this copy is silently "
                         f"dropped: {sorted(extra)}")

    # --- per-token value checks ---
    for name, val in tokens.items():
        tw = f"{where}.{name}"
        if name.startswith("image_"):
            if not isinstance(val, dict) or "asset" not in val:
                rep.error(tw, "image tokens must be { asset: <key> }, never an inline URL")
            elif val["asset"] not in assets:
                rep.error(tw, f"asset {val['asset']!r} not found in the assets block")
            continue
        if val is None or (isinstance(val, str) and not val.strip()):
            if template:
                rep.warn(tw, "empty value (template mode)")
            else:
                rep.error(tw, "empty value")
            continue
        if not isinstance(val, str):
            rep.error(tw, f"expected a string, got {type(val).__name__}")
            continue
        # --- design-time scaffolding must never reach a page ---
        hit = SCAFFOLDING_RE.search(val)
        if hit:
            rep.error(tw, f"design-time scaffolding {hit.group(0)!r} — strip it in TRANSLATE "
                          f"(§2); a live page must not load the Tailwind Play CDN, React dev "
                          f"builds, Babel, or the tweaks panel")
        dep = EXTERNAL_DEP_RE.search(val)
        if dep:
            rep.error(tw, "external script/stylesheet dependency — no fragment needs an "
                          "off-site asset, so this is scaffolding that leaked through")
        # --- unrendered JS template literals ---
        # A design export interleaves a cluster's client-side templates with real markup
        # (on the CNC page the explorer's ${a.summary} templates sit in the same section as
        # the closing CTA band). Extracted naively they ship as visible literal text.
        tpl = TEMPLATE_LITERAL_RE.findall(val)
        if tpl:
            rep.error(tw, f"unrendered JS template literal {tpl[:3]} — this is a cluster's "
                          f"client-side template, not page copy; it would render literally")
        # --- check 5: no nested token syntax ---
        nested = TOKEN_RE.findall(val)
        if nested:
            rep.error(tw, f"value contains token syntax {nested} — substitution would leave it unfilled")
        if name.startswith("url_"):
            if not re.match(r"^(https?://|/|#)", val):
                rep.warn(tw, f"{val!r} is not an absolute URL, root path, or anchor")
        if name.startswith(HTML_TOKENS) and "<" not in val and pattern not in EMBED_TEXT_PATTERNS:
            # These sit in text-editor / toggle-content slots, which always store block
            # markup. A bare string means the value came from a legend, and the legends
            # strip HTML: they truncate at the first inline tag and flatten <ul> items
            # together (AUDIT.md B9). Verified against post 12133: hero body_1's real value
            # ends "...applications.</p>" while its legend ends "...— with ".
            rep.error(tw, "HTML slot with no markup — a text-editor/toggle value always "
                          "carries its block wrapper (<p>, <ul>). A bare string here means "
                          "the value came from a legend, which is lossy; take it from the "
                          "design markup instead (TRANSLATE.md §6)")
        if name.startswith(("heading_", "button_", "faq_q_")) and "<" in val:
            rep.warn(tw, "plain-text slot contains markup — it will render literally")

    # --- check 7: mirrored titles ---
    for a, b in MIRRORED_TITLES.get(pattern, []):
        ka, kb = f"heading_{a}", f"heading_{b}"
        va, vb = tokens.get(ka), tokens.get(kb)
        if isinstance(va, str) and isinstance(vb, str) and va.strip() and vb.strip() and va != vb:
            rep.error(where, f"{ka} and {kb} are the same card title in two widgets "
                             f"(mobile/hover label) and must match: {va!r} != {vb!r}")

    # --- check 7: derived initials ---
    for a, b in DERIVED_INITIALS.get(pattern, []):
        ki, kn = f"heading_{a}", f"heading_{b}"
        vi, vn = tokens.get(ki), tokens.get(kn)
        if isinstance(vi, str) and isinstance(vn, str) and vi.strip() and vn.strip():
            ok = plausible_initials(vn)
            if ok and vi.strip().upper() not in ok:
                rep.error(where, f"{ki}={vi!r} must be initials derived from {kn}={vn!r} "
                                 f"(expected one of {sorted(ok)}) — never the source page's")

    # --- check 8: required structural options ---
    opts = sec.get("options") or {}
    if not isinstance(opts, dict):
        rep.error(where, "`options` must be a mapping")
        opts = {}
    if pattern in REQUIRED_OPTIONS:
        name, lo, hi = REQUIRED_OPTIONS[pattern]
        if name not in opts:
            rep.error(where, f"`options.{name}` is required — omitting it leaves the source "
                             f"page's arrangement, which is wrong for any other page")
        else:
            v = opts[name]
            if not isinstance(v, int) or not (lo <= v <= hi):
                rep.error(where, f"options.{name} must be an int in {lo}..{hi}, got {v!r}")
    for name in set(opts) - {REQUIRED_OPTIONS.get(pattern, (None,))[0]}:
        rep.warn(where, f"unknown option {name!r} for this pattern")


def main():
    ap = argparse.ArgumentParser(description="Validate a spec.yaml against the fragment library.")
    ap.add_argument("spec", help="path to spec.yaml")
    ap.add_argument("--template", action="store_true",
                    help="template mode: empty token values and placeholder attachment_id 0 "
                         "become warnings (for checking reference/spec.example.yaml)")
    ap.add_argument("--automation", action="store_true",
                    help="page-sync automation run (AUTOMATION.md): additionally require the "
                         f"`{AUTO_SLUG_PREFIX}` slug namespace")
    args = ap.parse_args()

    try:
        import yaml
    except ImportError:
        print("error: PyYAML is required (pip install pyyaml)", file=sys.stderr)
        return 2

    rep = Report()

    # --- check 1: parses, spec_version ---
    try:
        with open(args.spec, encoding="utf-8") as fh:
            spec = yaml.safe_load(fh)
    except FileNotFoundError:
        print(f"error: no such file: {args.spec}", file=sys.stderr)
        return 2
    except yaml.YAMLError as exc:
        print(f"error: {args.spec} is not valid YAML:\n{exc}", file=sys.stderr)
        return 1

    if not isinstance(spec, dict):
        print(f"error: {args.spec} must be a mapping at the top level", file=sys.stderr)
        return 1

    if spec.get("spec_version") != 1:
        rep.error("spec_version", f"must be 1, got {spec.get('spec_version')!r}")
    for key in set(spec) - {"spec_version", "page", "assets", "sections"}:
        rep.warn("top level", f"unknown key {key!r}")

    check_page(spec, rep, args.automation)
    assets = check_assets(spec, rep, args.template)

    sections = spec.get("sections")
    if not isinstance(sections, list) or not sections:
        rep.error("sections", "required, must be a non-empty list")
        sections = []
    for i, sec in enumerate(sections):
        check_section(i, sec, assets, rep, args.template)

    used = {a.get("asset") for s in sections if isinstance(s, dict)
            for a in (s.get("tokens") or {}).values() if isinstance(a, dict)}
    for key in set(assets) - used:
        rep.warn(f"assets.{key}", "declared but never referenced by an image token")

    name = os.path.basename(args.spec)
    for w in rep.warnings:
        print(f"  warn  {w}")
    for e in rep.errors:
        print(f"  ERROR {e}")

    n_tokens = sum(len(s.get("tokens") or {}) for s in sections if isinstance(s, dict))
    print()
    print(f"{name}: {len(sections)} sections, {n_tokens} tokens, "
          f"{len(rep.errors)} errors, {len(rep.warnings)} warnings")
    if rep.errors:
        print("GATE FAILED — do not write to WordPress (SKILL.md §2, §8)")
        return 1
    print("gates passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
