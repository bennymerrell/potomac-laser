#!/usr/bin/env python3
"""Carry a design re-export's copy changes into the five service specs.

    python3 tools/refresh_service_specs.py --old <unzipped old export> --new <unzipped new export>
    python3 tools/refresh_service_specs.py ... --check      # report only, write nothing

The 2026-09-24 re-export of Potomac Laser.zip renamed every page ("CNC Micromachining.html"
-> "Services - CNC Micromachining.html") and applied the Goodfellow content style rules
(uploads/Content_Style_Rules.md): 133 " —" became ",". Every section except the explorer
(index 3) keeps its node count, so old and new design nodes pair 1:1 and the edit set can be
read off the designs rather than re-derived from them.

Each changed node pair is reduced to its character-level edits, and each edit is applied to
the spec token values of the SAME section index, located by the old text around it. Nothing
is matched across sections, so an edit can only land where the design made it.

Then every token value is checked against the NEW design: its plain text must appear in that
section's plain text. The check is what makes the result trustworthy, not the substitution —
an edit that found no home, or a value the design no longer contains, is reported.

Not handled here, by design:
  - section 3, the application explorer. It is being moved inline (decided 2026-09-24) and is
    a new cluster, not a copy edit. Its token map is left as-is and reported.
  - quote-form-hubspot field markup ("Your name" -> First/Last name, Organisation -> Company).
    That markup is fixed inside the fragment and wired to HubSpot, not tokenised; changing it
    is a library change with a test submission, not a spec edit. Reported. (The section's
    TOKENS are handled: rebuild_quote() re-derives them from the legend, which also corrects
    the one-slot shift the four sibling specs shipped with.)
  - CNC's spec, which predates services-image-cards and quote-form-hubspot entering the
    library, is completed to 12 sections from Micro-Hole Drilling, whose design sections 2 and
    9 are checked node-for-node equal to CNC's apart from the quote placeholder.
"""
import argparse, copy, difflib, html, json, os, re, sys
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from align_design_nodes import sections, nodes

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = [  # (spec slug, old design filename, new design filename)
    ('pl-auto-cnc-micromachining', 'CNC Micromachining.html', 'Services - CNC Micromachining.html'),
    ('pl-auto-laser-micromachining', 'Laser Micromachining.html', 'Services - Laser Micromachining.html'),
    ('pl-auto-micro-hole-drilling', 'Micro-Hole Drilling.html', 'Services - Micro-Hole Drilling.html'),
    ('pl-auto-rapid-prototyping', 'Rapid Prototyping.html', 'Services - Rapid Prototyping.html'),
    ('pl-auto-3d-printing', '3D Printing.html', 'Services - 3D Printing.html'),
]
EXPLORER = 3
QUOTE = 9
CTX = (24, 12, 6, 3)


def plain(s):
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = html.unescape(re.sub(r'<[^>]+>', '', s))
    return re.sub(r'\s+', ' ', s).strip()


def text_nodes(sec):
    return [n for n in nodes(sec) if n[0] not in ('IMG', 'IFRAME')]


def edits(old, new, gap=8):
    """Character-level edits old -> new, each with the old text either side of it.

    Edits separated by fewer than `gap` unchanged characters are merged into one. Applied one
    at a time they cannot work: the first rewrites the text the next one's context was read
    from ("Project details" -> "Complete" is three opcodes, and applying them separately
    produced "Coject dete")."""
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    spans = [op[1:] for op in sm.get_opcodes() if op[0] != 'equal']
    merged = []
    for i1, i2, j1, j2 in spans:
        if merged and i1 - merged[-1][1] < gap:
            merged[-1] = (merged[-1][0], i2, merged[-1][2], j2)
        else:
            merged.append((i1, i2, j1, j2))
    for i1, i2, j1, j2 in merged:
        yield old[max(0, i1 - max(CTX)):i1], old[i1:i2], new[j1:j2], old[i2:i2 + max(CTX)]


def variants(s):
    """Spellings of design text as it may sit in a token value: parsed text has literal
    characters and keeps inline tags, while stored values escape & and some (post 12133's)
    carry no inline tags at all ("No MOQ — from", not "<strong>No MOQ</strong> — from")."""
    bare = re.sub(r'<[^>]*>?', '', s)
    bare = re.sub(r'^[^<]*>', '', bare)     # a tag cut in half by the context window
    out = [s, s.replace('&', '&amp;'), bare, bare.replace('&', '&amp;')]
    return list(dict.fromkeys(out))


def apply_edit(values, left, seg_old, seg_new, right):
    """Replace seg_old with seg_new in token values where it sits between left and right.
    Widest context first; the first width that finds anything is used, so a short, ambiguous
    context is only ever the fallback. Returns the number of replacements made."""
    for w in CTX:
        l, r = left[-w:] if w else '', right[:w]
        hits = 0
        for k, v in values.items():
            if not isinstance(v, str):
                continue
            for ll in variants(l):
                for rr in variants(r):
                    needle = ll + seg_old + rr
                    if needle and needle in v:
                        n = v.count(needle)
                        values[k] = v = v.replace(needle, ll + seg_new + rr)
                        hits += n
        if hits:
            return hits
    return 0


def load_spec(slug):
    p = os.path.join(REPO, 'specs', slug, 'spec.yaml')
    raw = open(p, encoding='utf-8').read()
    header = ''.join(l for l in raw.splitlines(True) if l.startswith('#'))
    return p, header, yaml.safe_load(raw)


def complete_cnc(cnc, mhd, old_dir, new_dir, report):
    """Insert services-image-cards and quote-form-hubspot into CNC's spec from MHD's."""
    have = [s['pattern'] for s in cnc['sections']]
    if 'services-image-cards' in have and 'quote-form-hubspot' in have:
        return
    c_new = sections(os.path.join(new_dir, 'Services - CNC Micromachining.html'))
    m_new = sections(os.path.join(new_dir, 'Services - Micro-Hole Drilling.html'))
    for idx in (2, QUOTE):
        a, b = text_nodes(c_new[idx]), text_nodes(m_new[idx])
        diff = [(x[1], y[1]) for x, y in zip(a, b) if x[1] != y[1]]
        allowed = 1 if idx == QUOTE else 0      # the per-page textarea placeholder
        if len(a) != len(b) or len(diff) > allowed:
            raise SystemExit(f'CNC section {idx} differs from MHD beyond the placeholder: {diff[:3]}')
    by = {s['pattern']: s for s in mhd['sections']}
    cards = copy.deepcopy(by['services-image-cards'])
    quote = copy.deepcopy(by['quote-form-hubspot'])
    ph = re.search(r'<textarea[^>]*placeholder="([^"]*)"', c_new[QUOTE])
    # CNC's old placeholder, so the style-rule edits below land on it like on the others.
    ph_old = re.search(r'<textarea[^>]*placeholder="([^"]*)"',
                       sections(os.path.join(old_dir, 'CNC Micromachining.html'))[QUOTE])
    quote['tokens']['body_7'] = html.unescape(ph_old.group(1) if ph_old else ph.group(1))
    for k, v in mhd['assets'].items():         # the card images (svc_1-5): same attachments
        if k.startswith('svc_'):
            if k in cnc['assets'] and cnc['assets'][k] != v:
                raise SystemExit(f'CNC asset {k} already set to something else: {cnc["assets"][k]}')
            cnc['assets'][k] = v
    cnc['sections'].insert(2, cards)
    cnc['sections'].insert(QUOTE, quote)
    report.append('CNC: completed to 12 sections — services-image-cards (index 2) and '
                  'quote-form-hubspot (index 9) from MHD; design sections verified equal '
                  'apart from the quote placeholder, which is CNC\'s own.')


def rebuild_quote(spec, old_quote_html, report, slug):
    """Re-derive the quote-form-hubspot token map from the fragment's own legend.

    The sibling specs (LM, MHD, RP, 3DP) numbered this section's tokens from the design's
    text order, not the fragment's: from heading_3 on, every value sits one slot off, so the
    timeline and stepper render shifted ("♢ ♢ Uploads…", "1 | 1 | Now", the step-2 label
    reading "Quote & process path confirmed"). Posts 12240-12243 carry it; CNC (12239)
    does not — its section IS the legend's source. Same defect class as the
    services-image-cards interleave fixed 2026-08-06 (e7d6efa).

    The legend holds post 12239's values, which are the OLD design's text for every token but
    body_7, the per-page textarea placeholder, read here from this page's old design. The
    design edits are then applied on top like everywhere else."""
    leg = json.load(open(os.path.join(REPO, 'reference', 'snippets',
                                      'quote-form-hubspot.legend.json')))['tokens']
    toks = {k.strip('{}'): v for k, v in leg.items()}
    ph = re.search(r'<textarea[^>]*placeholder="([^"]*)"', old_quote_html)
    toks['body_7'] = html.unescape(ph.group(1))
    sec = next(s for s in spec['sections'] if s['pattern'] == 'quote-form-hubspot')
    moved = sum(1 for k, v in toks.items() if sec['tokens'].get(k) != v)
    sec['tokens'] = dict(sorted(toks.items(), key=lambda kv: (kv[0].rsplit('_', 1)[0],
                                                              int(kv[0].rsplit('_', 1)[1]))))
    report.append(f'{slug}: quote-form-hubspot token map rebuilt from the legend '
                  f'({moved} of {len(toks)} values moved or changed)')


def refresh(slug, old_path, new_path, spec, report):
    old_s, new_s = sections(old_path), sections(new_path)
    if len(old_s) != len(spec['sections']) or len(new_s) != len(old_s):
        raise SystemExit(f'{slug}: section counts differ — old {len(old_s)}, new {len(new_s)}, '
                         f'spec {len(spec["sections"])}')
    rebuild_quote(spec, old_s[QUOTE], report, slug)
    applied = unplaced = 0
    notes = []
    for i, (a, b) in enumerate(zip(old_s, new_s)):
        if i == EXPLORER:
            continue
        na, nb = text_nodes(a), text_nodes(b)
        if len(na) != len(nb):
            raise SystemExit(f'{slug} s{i}: node count {len(na)} -> {len(nb)}; not a copy edit')
        toks = spec['sections'][i].setdefault('tokens', {})
        for k, v in toks.items():
            if isinstance(v, str):
                toks[k] = v.replace('&mdash;', '—').replace('&ndash;', '–')
        for (_, x, _), (_, y, _) in zip(na, nb):
            if x == y:
                continue
            for left, so, sn, right in edits(x, y):
                if so == '<span></span>' and sn == '':
                    continue                    # decorative dot on an eyebrow; no token holds it
                n = apply_edit(toks, left, so, sn, right)
                if n:
                    applied += n
                else:
                    unplaced += 1
                    notes.append(f's{i} [{spec["sections"][i]["pattern"]}] {so!r} -> {sn!r} '
                                 f'in "…{plain(left)[-30:]}|{plain(right)[:30]}…"')
    report.append(f'{slug}: {applied} edits applied, {unplaced} with no token home')
    report.extend('    ' + n for n in notes)
    return old_s, new_s


def verify(slug, spec, before, old_s, new_s, report):
    """Every token value's words must occur in its section of the new design.

    Three outcomes per value:
      - in the new design                → fine;
      - in the OLD design but not the new → NEW: the design changed it and this refresh
        did not follow, the one failure that matters;
      - in neither, and UNTOUCHED by this refresh → carried: a difference the built page
        already had (post 12133's stored values, fragment-owned labels), reported, not failed;
      - in neither, but CHANGED by this refresh   → NEW: the refresh produced text the design
        does not contain (a mangled edit), which must fail."""
    new_bad, carried = [], []
    for i, sec in enumerate(spec['sections']):
        if i == EXPLORER:
            continue
        hay_new = norm(plain(sec_text(new_s[i])))
        hay_old = norm(plain(sec_text(old_s[i])))
        for k, v in sec.get('tokens', {}).items():
            if not isinstance(v, str) or k.startswith('url_') or k.startswith('embed_'):
                continue
            p = norm(plain(v))
            if not p or p in hay_new:
                continue
            line = f's{i} [{sec["pattern"]}] {k}: {plain(v)[:90]!r}'
            was = before.get((i, k))
            if was == v and p not in hay_old:
                carried.append(line)
            elif was is not None and was != v and norm(plain(was)) not in hay_old:
                # already worded differently from the design before this refresh (e.g. LM's
                # "Goodfellow Microfabrication" where the design says "Potomac") AND edited by
                # it: the edit itself cannot be checked against the design, so show the diff
                carried.append(line + '  (EDITED: ' + ' / '.join(
                    f'{a!r}->{b!r}' for _, a, b, _ in edits(was, v)) + ')')
            else:
                new_bad.append(line)
    report.append(f'{slug}: {len(new_bad)} NEW mismatches, {len(carried)} carried from the built page')
    report.extend('    NEW     ' + b for b in new_bad)
    report.extend('    carried ' + c for c in carried)
    return new_bad


def sec_text(sec):
    """Section text as rendered, plus copy the node walk skips: button labels (SKIP drops
    <button>) and attribute copy a token can carry (placeholders)."""
    parts = [n[1] for n in text_nodes(sec)]
    parts += re.findall(r'<button\b[^>]*>(.*?)</button>', sec, re.S)
    parts += re.findall(r'placeholder="([^"]*)"', sec)
    return ' ¦ '.join(parts)


def norm(s):
    """Compare on words, not presentation. The built pages already differ from the design in
    ways the fragments own and the refresh must not "fix": eyebrows uppercased by CSS, list
    items joined, "→"/"●" drawn in CSS but stored literally (see CNC spec header), and
    straight vs curly quotes. What survives this is a real wording difference."""
    s = s.lower().replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'[^0-9a-zµ±×°%+.,:;\'"()/-]+', '', s)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--old', required=True, help='unzipped previous export')
    ap.add_argument('--new', required=True, help='unzipped new export')
    ap.add_argument('--check', action='store_true', help='report only; write nothing')
    a = ap.parse_args()

    report, specs = [], {}
    for slug, _, _ in PAGES:
        specs[slug] = load_spec(slug)
    complete_cnc(specs['pl-auto-cnc-micromachining'][2], specs['pl-auto-micro-hole-drilling'][2],
                 a.old, a.new, report)
    failures = 0
    for slug, old_name, new_name in PAGES:
        path, header, spec = specs[slug]
        before = {(i, k): v for i, sec in enumerate(spec['sections'])
                  for k, v in sec.get('tokens', {}).items()}
        old_s, new_s = refresh(slug, os.path.join(a.old, old_name), os.path.join(a.new, new_name),
                        spec, report)
        failures += len(verify(slug, spec, before, old_s, new_s, report))
        spec['sections'][EXPLORER].setdefault('_refresh', 'PENDING: inline explorer (not yet authored)')
        if not a.check:
            stamp = (f'# REFRESH 2026-09-24 : copy carried from {new_name} (Potomac Laser.zip\n'
                     f'#                      fab7225c…) by tools/refresh_service_specs.py.\n'
                     f'#                      Section {EXPLORER} (explorer) still the iframe embed — the\n'
                     f'#                      inline cluster replaces it in a later step.\n')
            spec['sections'][EXPLORER].pop('_refresh', None)
            body = yaml.dump(spec, sort_keys=False, allow_unicode=True, width=10**7,
                             default_flow_style=False)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(header.replace(f':: {old_name}', f':: {new_name}') + stamp + '\n' + body)
    print('\n'.join(report))
    print(f'\n{"CHECK ONLY — nothing written" if a.check else "specs written"}; '
          f'{failures} unverified token values')
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
