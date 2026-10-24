"""Safety regressions using tiny synthetic game files, never the user's installation."""
import hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import bsdiff4

spec=importlib.util.spec_from_file_location('patcher',Path(__file__).with_name('patcher.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
digest=lambda b:hashlib.sha256(b).hexdigest()

class InstallerSafety(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.game=self.root/'게임 폴더';self.data=self.game/'MonsterProm_Data';self.data.mkdir(parents=True);(self.game/'MonsterProm.exe').write_bytes(b'test marker, never executable');self.package=self.root/'package';(self.package/'patches').mkdir(parents=True);self.rows=[];self.original={}
  for i in range(2):
   name=f'level{i}';old=(f'original{i}\n'*80).encode();new=(f'한국어 번역{i}\n'*100).encode();delta=bsdiff4.diff(old,new);(self.data/name).write_bytes(old);self.original[name]=old;(self.package/'patches'/(name+'.bsdiff')).write_bytes(delta);self.rows.append(dict(file=name,original_sha256=digest(old),patched_sha256=digest(new),original_size=len(old),patched_size=len(new),delta=f'patches/{name}.bsdiff',delta_sha256=digest(delta)))
  self.save()
 def save(self):(self.package/'patch_manifest.json').write_text(json.dumps(dict(format=1,version='test',files=self.rows)),encoding='utf-8')
 def tearDown(self):self.tmp.cleanup()
 def run_patch(self,action):return module.run(action,self.game,self.package)
 def assert_original(self):
  for name,data in self.original.items():self.assertEqual((self.data/name).read_bytes(),data)
 def test_install_repeat_and_restore(self):
  self.assertEqual(self.run_patch('install')['changed_files'],2)
  self.assertEqual(self.run_patch('install')['changed_files'],0)
  self.assertEqual(self.run_patch('verify')['state'],'한글 패치 적용')
  self.assertEqual(self.run_patch('restore')['changed_files'],2);self.assert_original()
 def test_wrong_game_version_blocks_all_writes(self):
  (self.data/'level1').write_bytes(b'foreign mod');before={p.name:p.read_bytes() for p in self.data.iterdir()}
  with self.assertRaises(RuntimeError):self.run_patch('install')
  self.assertEqual(before,{p.name:p.read_bytes() for p in self.data.iterdir()});self.assertFalse((self.game/'_MonsterPromKR_Backup').exists())
 def test_corrupt_payload_blocks_all_writes(self):
  (self.package/'patches/level1.bsdiff').write_bytes(b'broken')
  with self.assertRaises(RuntimeError):self.run_patch('install')
  self.assert_original();self.assertFalse((self.game/'_MonsterPromKR_Backup').exists())
 def test_partial_commit_rolls_back(self):
  real=module.os.replace;count=0
  def failing(source,dest):
   nonlocal count
   count+=1
   if count==2:raise OSError('simulated disk failure')
   return real(source,dest)
  with patch.object(module.os,'replace',side_effect=failing):
   with self.assertRaises(OSError):self.run_patch('install')
  self.assert_original();self.assertFalse(list(self.game.glob('.mpkr-stage-*')))
 def test_existing_corrupt_backup_is_not_overwritten(self):
  backup=self.game/'_MonsterPromKR_Backup';backup.mkdir();(backup/'level0').write_bytes(b'keep this')
  with self.assertRaises(RuntimeError):self.run_patch('install')
  self.assert_original();self.assertEqual((backup/'level0').read_bytes(),b'keep this')
 def test_payload_path_escape_rejected(self):
  self.rows[0]['delta']='../outside.bsdiff';self.save()
  with self.assertRaises(RuntimeError):self.run_patch('install')
  self.assert_original()

if __name__=='__main__':unittest.main()
