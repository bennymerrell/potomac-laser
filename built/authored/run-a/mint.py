"""§7.4–7.5 local half: download server-tokenised fragments, verify SHA-256, write legends.

    python3 mint.py <run_id> <pattern>:<sha256>:<bytes>:<spec_slug>:<section_index>:<post_id>[:<cv>] ...

For each: curl patterns/<pattern>.json -> reference/snippets/, check the hash, write
<pattern>.legend.json from that spec section's token values (image tokens -> asset URL),
append the file to the run manifest, and print signature/colour stats for the PATTERNS entry.
"""
import collections, hashlib, json, os, re, subprocess, sys
import yaml
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
run = sys.argv[1]
man_p = os.path.join(ROOT, 'built', f'run-{run}.manifest.json')
man = json.load(open(man_p))
for arg in sys.argv[2:]:
    parts = arg.split(':')
    pat, sha, nbytes, slug, idx, pid = parts[:6]
    cv = parts[6] if len(parts) > 6 else '?'
    dst = os.path.join(ROOT, 'reference', 'snippets', pat + '.json')
    assert not os.path.exists(dst), f'{pat} already in the library'
    subprocess.run(['curl', '-s', '-o', dst, f'https://www.potomac-laser.com/wp-content/uploads/novamira-drafts/patterns/{pat}.json'], check=True)
    raw = open(dst, 'rb').read()
    if hashlib.sha256(raw).hexdigest() != sha:
        os.remove(dst)
        sys.exit(f'{pat}: SHA-256 MISMATCH — removed')
    spec = yaml.safe_load(open(os.path.join(ROOT, 'specs', slug, 'spec.yaml')))
    assets = {k: v['url'] for k, v in (spec.get('assets') or {}).items()}
    sec = spec['sections'][int(idx)]
    assert sec['pattern'] == pat
    leg = {'pattern': pat, 'source_post': int(pid), 'source_section_index': int(idx),
           'tokens': {'{' + k + '}': (assets[v['asset']] if isinstance(v, dict) else v) for k, v in sec['tokens'].items()}}
    json.dump(leg, open(os.path.join(ROOT, 'reference', 'snippets', pat + '.legend.json'), 'w'), indent=4, ensure_ascii=False)
    j = json.loads(raw)[0]
    skel = lambda e: (e['elType'], e.get('widgetType', ''), [skel(c) for c in e.get('elements', [])])
    cnt = lambda e, t: (1 if (e['elType'] == 'widget') == (t == 'w') else 0) + sum(cnt(c, t) for c in e.get('elements', []))
    txt = raw.decode()
    toks = sorted(set(re.findall(r'\{(\w+_\d+)\}', txt)), key=lambda x: (x.rsplit('_', 1)[0], int(x.rsplit('_', 1)[1])))
    kinds = collections.OrderedDict()
    for tk in toks:
        k, n = tk.rsplit('_', 1); kinds.setdefault(k, []).append(int(n))
    print(json.dumps({'pattern': pat, 'sig': hashlib.sha256(json.dumps(skel(j)).encode()).hexdigest()[:10],
                      'containers': cnt(j, 'c'), 'widgets': cnt(j, 'w'), 'bytes': len(raw),
                      'tokens': len(toks), 'token_ranges': {k: f'{min(v)}..{max(v)}' for k, v in kinds.items()},
                      'globals': dict(collections.Counter(re.findall(r'globals/colors\?id=(\w+)', txt))),
                      'cssvar': dict(collections.Counter(re.findall(r'var\(--e-global-color-(\w+)\)', txt))),
                      'hex': sorted(set(h.upper() for h in re.findall(r'#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?\b', txt))),
                      'rgba': sorted(set(re.findall(r'rgba\([^)]*\)', txt)))}))
    man['files_uploaded'].append({'path': f'wp-content/uploads/novamira-drafts/patterns/{pat}.json', 'bytes': int(nbytes),
                                  'sha256': sha, 'role': f'§7.4 tokenised fragment from post {pid} §{idx} (positional; {cv} css var rewrites)'})
json.dump(man, open(man_p, 'w'), indent=1)
