"""Build a §7.4 positional tokenise job for patterns minted from built posts.

    python3 mkmaps.py <out.json> <pattern>:<post_id>:<section_index> ...

Each job carries the candidate template (candidates/<pattern>.json). The server walks the
BUILT section and the template in lockstep: wherever the template holds a {token} string the
built value is replaced by it (image url -> token, id -> ''); every other leaf must be
identical (element ids excepted), which proves the built post is exactly this template.
Positional, because values are not unique (e.g. repeated "Read the case study" labels).
"""
import json, os, sys, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
S = '/private/tmp/claude-501/-Users-admin-orca-potomac-laser/d79e1efa-e1f9-4dfb-b04f-d08b0ac7ba4e/scratchpad/'
jobs = []
for arg in sys.argv[2:]:
    pat, pid, idx = arg.split(':')
    tpl = json.load(open(os.path.join(HERE, 'candidates', pat + '.json')))[0]
    jobs.append({'pattern': pat, 'post': int(pid), 'index': int(idx), 'template': tpl})
raw = json.dumps(jobs, ensure_ascii=False).encode()
open(S + sys.argv[1], 'wb').write(raw)
print(json.dumps({'file': sys.argv[1], 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                  'jobs': [(j['pattern'], j['post'], j['index']) for j in jobs]}))
