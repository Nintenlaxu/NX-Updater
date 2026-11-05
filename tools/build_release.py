"""Build a delta in the actual Java client's signed-manifest format. No private keys."""
import argparse, hashlib, json, re, shutil
from pathlib import Path
from urllib.parse import urlparse

CHANNELS = ('DEVELOPMENT', 'RELEASE CANDIDATE', 'STABLE')
VERSION = re.compile(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?')
HOSTS = {'github.com', 'api.github.com', 'release-assets.githubusercontent.com', 'objects.githubusercontent.com'}

def inventory(root):
    result = {}
    for folder in ('res', 'lib', 'runtime'):
        if (root/folder).is_symlink(): raise ValueError('Symbolic directory: '+folder)
        for p in sorted((root/folder).rglob('*')):
            if p.is_symlink(): raise ValueError('Symbolic link: '+str(p))
            if p.is_file(): result[p.relative_to(root).as_posix()] = p
    for name in ('street-cbtis4-multiplayer.jar', 'version.properties'):
        p=root/name
        if p.is_symlink(): raise ValueError('Symbolic link: '+name)
        if p.is_file(): result[name]=p
    for name in result:
        if len(name)>220 or any(c in name for c in '\\:<>|?*"') or any(ord(c)<32 for c in name):
            raise ValueError('Unsafe client path: '+name)
        for part in name.split('/'):
            if part in ('','.','..') or part.endswith((' ','.')) or re.fullmatch(r'(?i)(con|prn|aux|nul|com[0-9]|lpt[0-9])(\..*)?',part):
                raise ValueError('Unsafe client path: '+name)
    if len({n.lower() for n in result})!=len(result): raise ValueError('Case collision')
    return result

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def build(base, target, output, version, from_version, asset_base, channel='DEVELOPMENT', notes=''):
    if not VERSION.fullmatch(version) or not VERSION.fullmatch(from_version): raise ValueError('Invalid SemVer')
    if channel not in CHANNELS: raise ValueError('Invalid channel')
    if channel=='STABLE' and '-' in version.split('+')[0]: raise ValueError('Stable prerelease')
    u=urlparse(asset_base)
    if u.scheme!='https' or u.hostname not in HOSTS or u.username or u.password or u.query or u.fragment:
        raise ValueError('Expected trusted GitHub HTTPS asset base')
    old,new=inventory(base),inventory(target)
    if output.exists(): raise ValueError('Output already exists')
    entries=[]; blobs={}; total=0
    for name in sorted(set(old)|set(new)):
        before=digest(old[name]) if name in old else None
        after=digest(new[name]) if name in new else None
        if before==after: continue
        entry={'path':name,'action':'DELETE' if after is None else ('REPLACE' if before else 'ADD')}
        if before: entry['oldSha256']=before
        if after:
            size=new[name].stat().st_size
            if size>512*1024*1024: raise ValueError('File too large')
            total+=size
            entry.update(size=size,sha256=after,url=asset_base.rstrip('/')+'/'+after+'.bin')
            blobs[after]=new[name]
        entries.append(entry)
    if not entries or len(entries)>20000 or total>4*1024**3: raise ValueError('Empty or oversized delta')
    manifest={'schemaVersion':1,'version':version,'platform':'PC_JAVA','channel':channel,
              'protocol':'CB4-LAN-3','mode':'PATCH','fromVersion':from_version,'notes':notes,
              'dependencies':{'javaMajor':17},'files':entries}
    raw=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    if len(raw)>4*1024*1024: raise ValueError('Manifest too large')
    output.mkdir(parents=True)
    for sha,p in blobs.items(): shutil.copyfile(p,output/(sha+'.bin'))
    name='NX_UPDATE_PC_JAVA_'+channel.replace(' ','_')+'.json'
    (output/name).write_bytes(raw)
    return output/name

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ('base','target','output'): p.add_argument('--'+arg,type=Path,required=True)
    for arg in ('version','from-version','asset-base'): p.add_argument('--'+arg,required=True)
    p.add_argument('--channel',choices=CHANNELS,default='DEVELOPMENT');p.add_argument('--notes',default='')
    a=p.parse_args();print(build(a.base,a.target,a.output,a.version,a.from_version,a.asset_base,a.channel,a.notes))
