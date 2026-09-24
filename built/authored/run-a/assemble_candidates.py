"""Assemble a spec whose sections include §7 CANDIDATE patterns (not yet in the library).

Same code path as tools/assemble.py — substitution, image-id re-attachment, re-id, §2 gates —
with built/authored/run-a/candidates/ searched before reference/snippets/ via the
assembler's own FRAGMENT_OVERRIDES hook. Once a candidate is minted into the library this
is no longer needed for that pattern.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import assemble as A
A.FRAGMENT_OVERRIDES[:] = [os.path.join(HERE, 'candidates')]
spec, data = A.assemble(sys.argv[1])
out = sys.argv[2]
with open(out, 'w') as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
n = sum(1 for _ in A.normalise(data).__iter__()) if False else None
def count(o):
    return (1 if isinstance(o, dict) and 'elType' in o else 0) + sum(count(v) for v in (o.values() if isinstance(o, dict) else o if isinstance(o, list) else []))
print(f'{spec["page"]["slug"]}: {len(data)} sections, {count(data)} elements -> {out}')
