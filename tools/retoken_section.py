#!/usr/bin/env python3
"""Re-token one section of an ALREADY-BUILT page, in place, preserving element ids.

    python3 tools/retoken_section.py specs/<slug>/spec.yaml built/<slug>.json --section 2

Why this exists rather than just re-running assemble.py: the builds for
pl-auto-laser-micromachining and pl-auto-micro-hole-drilling were produced by the
pre-assembler path, so re-assembling them regenerates every element id. The live posts
carry the committed ids, and Elementor keys per-element CSS off them — so correcting ten
text values by way of a full re-assembly would rewrite all 292 ids on a live page to fix
ten strings. This walks the assembled-from-spec tree and the built tree in lockstep and
copies across only widget TEXT values, leaving ids, styling and structure untouched.

Refuses to run if the two trees are not structurally identical, which is the only thing
that makes the lockstep walk meaningful.
"""
import argparse, json, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assemble as A

# Widget settings keys that hold substituted text. Image slots are deliberately absent:
# they carry attachment ids that must not be disturbed.
TEXT_KEYS = ('title', 'editor')


def shape(o, p=''):
    """Structural fingerprint: every leaf path, values excluded."""
    out = []
    if isinstance(o, dict):
        for k in sorted(o):
            out += shape(o[k], f'{p}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out += shape(v, f'{p}[{i}]')
    else:
        out.append(p)
    return out


def copy_text(src, dst, changes):
    if isinstance(src, dict) and isinstance(dst, dict):
        if 'widgetType' in dst:
            s_set, d_set = src.get('settings', {}), dst.get('settings', {})
            for k in TEXT_KEYS:
                if k in d_set and k in s_set and d_set[k] != s_set[k]:
                    changes.append((dst.get('id'), dst.get('widgetType'), k, d_set[k], s_set[k]))
                    d_set[k] = s_set[k]
        for k in dst:
            if k in src:
                copy_text(src[k], dst[k], changes)
    elif isinstance(src, list) and isinstance(dst, list):
        for a, b in zip(src, dst):
            copy_text(a, b, changes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('spec')
    ap.add_argument('built')
    ap.add_argument('--section', type=int, required=True)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    _, fresh = A.assemble(args.spec)
    with open(args.built) as f:
        raw = f.read()
    built = json.loads(raw)
    # Round-trip the file's own serialisation so the diff shows only changed values.
    # The pre-assembler builds are one minified line; assemble.py writes indent=1.
    trailing = raw[len(raw.rstrip('\n')):]
    indent = None if json.dumps(built, ensure_ascii=False) == raw.rstrip('\n') else 1

    i = args.section
    if not (0 <= i < len(built) and i < len(fresh)):
        sys.exit(f'FAIL: section {i} out of range')
    if shape(fresh[i]) != shape(built[i]):
        sys.exit(f'FAIL: section {i} is not structurally identical in spec vs build — '
                 'lockstep copy is unsafe; re-assemble the page instead')

    changes = []
    copy_text(fresh[i], built[i], changes)
    for eid, wt, k, old, new in changes:
        print(f'  {eid} {wt}.{k}\n    - {old}\n    + {new}')
    print(f'{len(changes)} text value(s) changed in section {i}')

    if args.dry_run:
        return
    with open(args.built, 'w') as f:
        f.write(json.dumps(built, ensure_ascii=False, indent=indent) + trailing)
    print(f'wrote {args.built}')


if __name__ == '__main__':
    main()
