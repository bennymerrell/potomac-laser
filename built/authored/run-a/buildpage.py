"""Write a page's spec.yaml from candidate/library values, assemble it, emit the staging file.

    python3 built/authored/run-a/buildpage.py <page.json> [--version N]

<page.json>: {"slug", "title", "design_page", "header": "<# comment block>",
              "sections": [{"pattern": id, "values": "<file in candidates/>" | {tokens}}],
              "assets": ["cs_img_1", ...]}     # keys looked up in candidates/assets.json

Assembly goes through tools/assemble.py with candidates/ as FRAGMENT_OVERRIDES (as
assemble_candidates.py). Output: specs/<slug>/spec.yaml, built/<slug>.json, and the
minified staging file in the scratchpad, whose sha256/bytes are printed for the §4 write.
"""
import argparse, hashlib, json, os, sys
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import assemble as A

A.FRAGMENT_OVERRIDES[:] = [os.path.join(HERE, 'candidates')]  # library patterns not in candidates/ fall through to reference/snippets/
SCRATCH = '/private/tmp/claude-501/-Users-admin-orca-potomac-laser/d79e1efa-e1f9-4dfb-b04f-d08b0ac7ba4e/scratchpad/'

ap = argparse.ArgumentParser()
ap.add_argument('page')
ap.add_argument('--version', type=int, default=1)
a = ap.parse_args()
pg = json.load(open(a.page))
amap = json.load(open(os.path.join(HERE, 'candidates', 'assets.json')))
spec = {'spec_version': 1,
        'page': {'title': pg['title'], 'slug': pg['slug'], 'post_type': 'page', 'post_status': 'draft'}}
if pg.get('assets'):
    spec['assets'] = {k: amap[k] for k in pg['assets']}
secs = []
for s in pg['sections']:
    v = s['values']
    toks = json.load(open(os.path.join(HERE, 'candidates', v))) if isinstance(v, str) else v
    secs.append({'pattern': s['pattern'], 'tokens': toks})
spec['sections'] = secs
d = os.path.join(ROOT, 'specs', pg['slug'])
os.makedirs(d, exist_ok=True)
with open(os.path.join(d, 'spec.yaml'), 'w') as f:
    f.write(pg['header'].rstrip() + '\n\n' + yaml.safe_dump(spec, sort_keys=False, allow_unicode=True, width=4000))
spec2, data = A.assemble(os.path.join(d, 'spec.yaml'))
with open(os.path.join(ROOT, 'built', pg['slug'] + '.json'), 'w') as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
raw = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()
name = f'{pg["slug"]}.v{a.version}.elementor.json'
open(SCRATCH + name, 'wb').write(raw)


def count(o):
    return (1 if isinstance(o, dict) and 'elType' in o else 0) + sum(
        count(x) for x in (o.values() if isinstance(o, dict) else o if isinstance(o, list) else []))


print(json.dumps({'file': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                  'sections': len(data), 'elements': count(data)}))
