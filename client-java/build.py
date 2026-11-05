"""Build only the updater and its screen; preserve every U09 gameplay class."""
from pathlib import Path
import subprocess, zipfile, sys, os

ROOT = Path(__file__).resolve().parent
def run(args):
    result = subprocess.run(args, text=True, capture_output=True)
    print(result.stdout, end=''); print(result.stderr, end='', file=sys.stderr)
    if result.returncode: raise SystemExit(result.returncode)

def main():
    classes = ROOT / 'build/classes'
    classes.mkdir(parents=True, exist_ok=True)
    compiler = ['java', '-m', 'jdk.compiler/com.sun.tools.javac.Main']
    run(compiler + ['-source', '8', '-target', '8', '-encoding', 'UTF-8', '-d', str(classes)] +
        [str(p) for p in sorted((ROOT/'src').rglob('*.java'))])
    helper = ROOT/'build/nx-updater.jar'
    with zipfile.ZipFile(helper, 'w', zipfile.ZIP_DEFLATED) as out:
        out.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\nMain-Class: nx.updater.Launcher\n\n')
        for p in sorted((classes/'nx').rglob('*.class')): out.write(p, p.relative_to(classes))
    tests = ROOT/'build/tests'; tests.mkdir(exist_ok=True)
    run(compiler + ['-encoding','UTF-8','-cp',str(classes),'-d',str(tests)] +
        [str(p) for p in sorted((ROOT/'tests').glob('*.java'))])
    cp = os.pathsep.join(map(str,[classes,tests]))
    run(['java','-cp',cp,'nx.updater.UpdaterAudit',str(helper)])
    run(['java','-cp',cp,'nx.updater.RepositoryIntegrationAudit'])
    if len(sys.argv)>1:
        root=Path(sys.argv[1]).resolve(); jar=root/'street-cbtis4-multiplayer.jar'
        overlay={p.relative_to(classes).as_posix():p.read_bytes() for p in classes.rglob('*.class')}
        temp=jar.with_suffix('.u10.tmp')
        with zipfile.ZipFile(jar) as old, zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as out:
            for name in old.namelist():
                if name not in overlay: out.writestr(name,old.read(name))
            for name,data in sorted(overlay.items()):out.writestr(name,data)
        temp.replace(jar)
        (root/'nx-updater.jar').write_bytes(helper.read_bytes())
        print('PASS applied updater overlay; gameplay and SDL classes preserved')
if __name__=='__main__':main()
