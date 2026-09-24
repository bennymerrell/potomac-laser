"""Bundle several staging files into one upload: {"files": {name: text}, "sha256": {name: hex}}."""
import hashlib, json, sys
S = '/private/tmp/claude-501/-Users-admin-orca-potomac-laser/d79e1efa-e1f9-4dfb-b04f-d08b0ac7ba4e/scratchpad/'
out, names = sys.argv[1], sys.argv[2:]
b = {'files': {}, 'sha256': {}}
for n in names:
    raw = open(S + n, 'rb').read()
    b['files'][n] = raw.decode('utf-8'); b['sha256'][n] = hashlib.sha256(raw).hexdigest()
data = json.dumps(b, ensure_ascii=False).encode()
open(S + out, 'wb').write(data)
print(json.dumps({'bundle': out, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'files': b['sha256']}))
