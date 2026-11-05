"""Cross-language contract test with an ephemeral in-memory Java signing key."""
from pathlib import Path
import tempfile, subprocess, os
from build_release import build
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='nx-contract-') as temp:
    r=Path(temp);base=r/'base';target=r/'target'
    for p in (base,target):(p/'res').mkdir(parents=True)
    (base/'res/change').write_bytes(b'old');(target/'res/change').write_bytes(b'new')
    (base/'res/delete').write_bytes(b'old');(target/'res/add').write_bytes(b'new')
    manifest=build(base,target,r/'out','0.1.1','0.1.0','https://github.com/example/feed/releases/download/v0.1.1')
    cp=os.pathsep.join(str(ROOT/'client-java/build'/s) for s in ('classes','tests'))
    subprocess.run(['java','-cp',cp,'nx.updater.PublisherContractAudit',str(manifest)],check=True)
