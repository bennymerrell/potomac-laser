#!/usr/bin/env python3
"""Assemble a spec.yaml into an _elementor_data array (SKILL.md §2 + §3).

    python3 tools/assemble.py specs/<slug>/spec.yaml -o built/<slug>.json
    python3 tools/assemble.py --self-test

Substitutes every `{token}` into its fragment, re-attaches image attachment ids on
both shapes (`image` widget settings AND container `background_image`), regenerates a
unique 7-char hex id on every element, and concatenates the sections in spec order.

Runs SKILL.md §2's gates on this side of the wire: no unfilled token survives, no
design-time scaffolding (Tailwind CDN / unpkg / babel / tweaks panel), no external
script or stylesheet, every image slot carries an id, and the result parses as JSON.

`--self-test` re-assembles tools/fixtures/mhd-preorder/spec.yaml and compares it to
tools/fixtures/mhd-preorder/expected.json with element ids normalised. Any difference
means this assembler does not reproduce a build produced by the earlier, pre-assembler
path, so it must not be trusted on a new page.

That fixture is a FROZEN COPY of the Micro-Hole Drilling spec and build as they stood at
commit e5cffb6, kept only to pin the assembler's *mechanics* — token substitution, image
id re-attachment, re-iding, section order. It is deliberately not updated: the live spec
and build have since had their `services-image-cards` token order corrected (body_3/4 =
card 1's description and link, 5/6 = card 2, …, not five descriptions then five links),
so the fixture still carries that content defect. Do not read it as a content reference,
and do not "fix" it — re-pointing the test at a current build would make it circular,
since both sides would then come from this same assembler.

For the same reason the fixture pins a copy of any fragment the library later revises, in
tools/fixtures/mhd-preorder/snippets/ (searched first, self-test only). First entry:
quote-form-hubspot, as it stood before the 2026-09-24 split-name change.

The two structural `options` (`you_are_here_unit`, `highlight_step`) are verified
against the fragment rather than applied blindly: the fragments were tokenised from
post 12133, whose badge already sits on unit 2 and whose highlight is already step 3,
so those values are no-ops. Any OTHER value is refused rather than silently ignored.
"""
import argparse, copy, hashlib, json, re, sys, os
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNIPPETS = os.path.join(ROOT, 'reference', 'snippets')

TOKEN_RE = re.compile(r'\{(heading|body|button|url|image|embed|faq_q|faq_a)_(\d+)\}')
IMAGE_TOKEN_RE = re.compile(r'^\{image_(\d+)\}$')

SCAFFOLDING = ['cdn.tailwindcss.com', 'unpkg.com', 'babel', 'tweaks-panel', 'tweaks-root']
EXTERNAL_RE = [re.compile(r'<script[^>]+src="http'), re.compile(r'<link[^>]+rel="stylesheet"[^>]+href="http')]

# Fragment-native values of the two structural options, read off post 12133.
NATIVE_OPTIONS = {
    'group-ecosystem-cards': {'you_are_here_unit': 2},
    'process-steps-numbered': {'highlight_step': 3},
}


class Fail(Exception):
    pass


# Directories searched before the library. Only --self-test sets this: its fixture pins
# the fragments the library has since changed, so the test keeps pinning the assembler's
# mechanics instead of failing every time a fragment is revised on purpose.
FRAGMENT_OVERRIDES = []


def load_fragment(pattern):
    p = next((q for q in (os.path.join(d, pattern + '.json') for d in FRAGMENT_OVERRIDES)
              if os.path.exists(q)), os.path.join(SNIPPETS, pattern + '.json'))
    if not os.path.exists(p):
        raise Fail(f'no fragment for pattern {pattern!r}')
    with open(p) as f:
        frag = json.load(f)
    # The two §7 mints (services-image-cards, quote-form-hubspot) were tokenised as a
    # one-element array; the ten originals are bare section objects. Both mean one section.
    if isinstance(frag, list):
        if len(frag) != 1:
            raise Fail(f'fragment {pattern} holds {len(frag)} sections, expected 1')
        frag = frag[0]
    return frag


def resolve_assets(spec):
    out = {}
    for name, a in (spec.get('assets') or {}).items():
        out[name] = (a['url'], int(a['attachment_id']))
    return out


def substitute(node, tokens, assets, pattern, seen):
    """Walk the fragment in place. Image tokens fill url+id; everything else is a
    string replace so a token embedded in longer markup still resolves."""
    if isinstance(node, dict):
        for key, val in list(node.items()):
            if isinstance(val, dict) and isinstance(val.get('url'), str):
                m = IMAGE_TOKEN_RE.match(val['url'])
                if m:
                    tk = f'image_{m.group(1)}'
                    spec_val = tokens.get(tk)
                    if not isinstance(spec_val, dict) or 'asset' not in spec_val:
                        raise Fail(f'{pattern}.{tk}: expected an {{asset: name}} mapping')
                    aname = spec_val['asset']
                    if aname not in assets:
                        raise Fail(f'{pattern}.{tk}: asset {aname!r} not in the spec asset map')
                    url, aid = assets[aname]
                    val['url'], val['id'] = url, aid
                    seen.add(tk)
                    continue
            if isinstance(val, str):
                node[key] = _sub_str(val, tokens, pattern, seen)
            else:
                substitute(val, tokens, assets, pattern, seen)
    elif isinstance(node, list):
        for i, val in enumerate(node):
            if isinstance(val, str):
                node[i] = _sub_str(val, tokens, pattern, seen)
            else:
                substitute(val, tokens, assets, pattern, seen)


def _sub_str(s, tokens, pattern, seen):
    def repl(m):
        tk = m.group(0)[1:-1]
        if tk not in tokens:
            raise Fail(f'{pattern}: fragment needs {{{tk}}} and the spec does not supply it')
        v = tokens[tk]
        if isinstance(v, dict):
            raise Fail(f'{pattern}.{tk}: mapping supplied for a text slot')
        seen.add(tk)
        return str(v)
    return TOKEN_RE.sub(repl, s)


def reid(node, used, salt):
    """Unique 7-char hex id on every element (SKILL.md §2 — fragments carry the
    source page's ids and duplicates break the editor)."""
    if isinstance(node, dict):
        if 'elType' in node:
            base = node.get('id', '') or 'x'
            n = 0
            while True:
                h = hashlib.sha256(f'{salt}|{base}|{n}'.encode()).hexdigest()[:7]
                if h not in used:
                    break
                n += 1
            used.add(h)
            node['id'] = h
        for v in node.values():
            reid(v, used, salt)
    elif isinstance(node, list):
        for v in node:
            reid(v, used, salt)


def check_options(section):
    pattern = section['pattern']
    given = section.get('options') or {}
    native = NATIVE_OPTIONS.get(pattern)
    if native is None:
        if given:
            raise Fail(f'{pattern}: options given for a pattern that defines none')
        return
    for k, v in given.items():
        if k not in native:
            raise Fail(f'{pattern}: unknown option {k!r}')
        if v != native[k]:
            raise Fail(
                f'{pattern}: {k}={v} differs from the fragment-native {native[k]} — this '
                f'assembler cannot move that widget; author the change or fix the spec')


def assemble(spec_path):
    with open(spec_path) as f:
        spec = yaml.safe_load(f)
    assets = resolve_assets(spec)
    used_ids = set()
    out = []
    for i, section in enumerate(spec['sections']):
        pattern = section['pattern']
        tokens = section.get('tokens') or {}
        check_options(section)
        frag = copy.deepcopy(load_fragment(pattern))
        seen = set()
        substitute(frag, tokens, assets, pattern, seen)
        extra = set(tokens) - seen
        if extra:
            raise Fail(f'sections[{i}] {pattern}: spec supplies unused tokens {sorted(extra)}')
        reid(frag, used_ids, f'{spec["page"]["slug"]}|{i}')
        out.append(frag)
    gates(out, spec)
    return spec, out


def gates(data, spec):
    blob = json.dumps(data, ensure_ascii=False)
    left = TOKEN_RE.findall(blob)
    if left:
        raise Fail(f'unfilled tokens survive assembly: {sorted(set(left))[:8]}')
    for s in SCAFFOLDING:
        if s in blob:
            raise Fail(f'design-time scaffolding reached the assembled JSON: {s!r}')
    for rx in EXTERNAL_RE:
        if rx.search(blob):
            raise Fail(f'external asset reference in assembled JSON: {rx.pattern}')
    # image id gate — both shapes (SKILL.md §3; AUDIT.md B12)
    missing = []

    def walk(o, path=''):
        if isinstance(o, dict):
            if o.get('widgetType') == 'image':
                img = o.get('settings', {}).get('image') or {}
                if not img.get('id'):
                    missing.append(f'{path} image widget')
            for k, v in o.items():
                if k == 'background_image' and isinstance(v, dict):
                    if v.get('url') and not v.get('id'):
                        missing.append(f'{path}.background_image')
                walk(v, f'{path}.{k}')
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f'{path}[{i}]')
    walk(data)
    if missing:
        raise Fail(f'image slots without an attachment id: {missing}')
    ids = []

    def collect(o):
        if isinstance(o, dict):
            if 'elType' in o:
                ids.append(o['id'])
            for v in o.values():
                collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)
    collect(data)
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise Fail(f'duplicate element ids: {sorted(dupes)[:8]}')
    bad = [i for i in ids if not re.fullmatch(r'[0-9a-f]{7}', i)]
    if bad:
        raise Fail(f'element ids not 7-char hex: {bad[:8]}')
    json.loads(blob)  # parse gate
    return len(ids)


def normalise(data):
    """Strip element ids so two assemblies can be compared on content alone."""
    d = copy.deepcopy(data)

    def walk(o):
        if isinstance(o, dict):
            if 'elType' in o and 'id' in o:
                o['id'] = ''
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(d)
    return d


def self_test():
    spec_path = os.path.join(ROOT, 'tools', 'fixtures', 'mhd-preorder', 'spec.yaml')
    ref_path = os.path.join(ROOT, 'tools', 'fixtures', 'mhd-preorder', 'expected.json')
    FRAGMENT_OVERRIDES[:] = [os.path.join(ROOT, 'tools', 'fixtures', 'mhd-preorder', 'snippets')]
    _, got = assemble(spec_path)
    with open(ref_path) as f:
        want = json.load(f)
    a = json.dumps(normalise(got), sort_keys=True, ensure_ascii=False)
    b = json.dumps(normalise(want), sort_keys=True, ensure_ascii=False)
    if a == b:
        print('self-test PASS — reproduces tools/fixtures/mhd-preorder/expected.json '
              '(ids normalised)')
        return 0
    print('self-test FAIL — assembly differs from the frozen pre-assembler MHD build')
    import difflib
    la = json.dumps(normalise(got), indent=1, sort_keys=True, ensure_ascii=False).splitlines()
    lb = json.dumps(normalise(want), indent=1, sort_keys=True, ensure_ascii=False).splitlines()
    for line in list(difflib.unified_diff(lb, la, 'verified', 'assembled', lineterm=''))[:60]:
        print(line)
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('spec', nargs='?')
    ap.add_argument('-o', '--out')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    if args.self_test:
        sys.exit(self_test())
    if not args.spec:
        ap.error('spec path required')
    try:
        spec, data = assemble(args.spec)
    except Fail as e:
        print(f'FAIL: {e}', file=sys.stderr)
        sys.exit(1)
    n = gates(data, spec)
    print(f'{spec["page"]["slug"]}: {len(data)} sections, {n} elements, gates passed')
    if args.out:
        with open(args.out, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        print(f'wrote {args.out}')


if __name__ == '__main__':
    main()
