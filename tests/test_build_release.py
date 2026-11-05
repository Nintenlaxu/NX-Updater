import importlib.util, tempfile, unittest, json
from pathlib import Path
spec=importlib.util.spec_from_file_location('build_release',Path(__file__).parents[1]/'tools/build_release.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ReleaseBuildTest(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup);self.r=Path(self.t.name)
        self.base=self.r/'base';self.target=self.r/'next'
        for p in (self.base,self.target): (p/'res').mkdir(parents=True)
        (self.base/'res/old.txt').write_text('old');(self.target/'res/old.txt').write_text('new')
        (self.base/'res/remove.txt').write_text('gone');(self.target/'res/add.txt').write_text('added')
        (self.target/'config').mkdir();(self.target/'config/private.txt').write_text('never publish')
    def build(self,**kwargs):
        a=dict(base=self.base,target=self.target,output=self.r/'out',version='0.1.1',from_version='0.1.0',asset_base='https://github.com/example/feed/releases/download/v0.1.1')
        a.update(kwargs);return m.build(**a)
    def test_delta(self):
        f=self.build();data=json.loads(f.read_text());self.assertEqual(data['schemaVersion'],1)
        self.assertEqual({x['path']:x['action'] for x in data['files']},{'res/add.txt':'ADD','res/old.txt':'REPLACE','res/remove.txt':'DELETE'})
        for x in data['files']:
            if x['action']!='DELETE':self.assertEqual(m.digest(f.parent/(x['sha256']+'.bin')),x['sha256'])
    def test_no_plain_http(self):
        with self.assertRaises(ValueError): self.build(asset_base='http://github.com/unsafe')
    def test_no_untrusted_host(self):
        with self.assertRaises(ValueError): self.build(asset_base='https://evil.example/release')
    def test_no_overwrite(self):
        self.build()
        with self.assertRaises(ValueError):self.build()
    def test_symlink(self):
        (self.target/'res/leak').symlink_to(self.target/'config/private.txt')
        with self.assertRaises(ValueError): self.build()
    def test_no_stable_prerelease(self):
        with self.assertRaises(ValueError): self.build(channel='STABLE',version='0.1.1-rc.1')
if __name__=='__main__':unittest.main()
