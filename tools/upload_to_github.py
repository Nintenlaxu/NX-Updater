"""Upload this prepared control repository, preserving existing remote files."""
from pathlib import Path
import json, subprocess, tempfile, shutil
ROOT=Path(__file__).resolve().parents[1]
REPO='Nintenlaxu/NX-Updater'
def run(*args,cwd=None,capture=False):
    return subprocess.run(args,cwd=cwd,check=True,text=True,stdout=subprocess.PIPE if capture else None).stdout
def main():
    run('gh','auth','status')
    if run('gh','api','user','--jq','.login',capture=True).strip().lower()!='nintenlaxu':
        raise SystemExit('Use the authorized Nintenlaxu GitHub account.')
    view=subprocess.run(['gh','repo','view',REPO,'--json','visibility,defaultBranchRef'],text=True,capture_output=True)
    exists=view.returncode==0
    if exists and json.loads(view.stdout)['visibility']!='PRIVATE':
        raise SystemExit('Expected PRIVATE repository; refusing upload.')
    with tempfile.TemporaryDirectory(prefix='nx-control-') as temp:
        dest=Path(temp)/'repo'
        if exists:run('gh','repo','clone',REPO,str(dest))
        else:
            dest.mkdir();run('git','init','-b','main',str(dest))
        files=json.loads((ROOT/'UPLOAD_FILES.json').read_text())
        for name in files:
            if name.startswith('/') or '..' in Path(name).parts: raise ValueError('Invalid upload path')
            src=ROOT/name;out=dest/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,out)
        run('git','add','--',*files,cwd=dest)
        delta=subprocess.run(['git','diff','--cached','--quiet'],cwd=dest)
        if delta.returncode==0: print('Already synchronized.');return
        run('git','-c','user.name=NX GAMES','-c','user.email=Nintenlaxu@users.noreply.github.com','commit','-m','Integrate NX Updater with Java U10 and verified release publishing',cwd=dest)
        if exists:run('git','push','origin','HEAD',cwd=dest)
        else:run('gh','repo','create',REPO,'--private','--source',str(dest),'--push')
    state=json.loads(run('gh','repo','view',REPO,'--json','visibility,url',capture=True))
    if state['visibility']!='PRIVATE':raise SystemExit('Unexpected repository visibility')
    print('PASS private control repository:',state['url'])
if __name__=='__main__':main()
