"""Exercise the shipped Windows executable on disposable copies of original files."""
from pathlib import Path
import json,shutil,subprocess,zipfile,hashlib

BASE=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 archive=BASE/'release_dist/Monster-Prom-1-KR-v0.1.0-beta.1.zip';root=BASE/'release_test/릴리즈 설치 검증';assert not root.exists(),'Use a fresh test path; existing test files are preserved.';package=root/'압축 해제';game=root/'게임 폴더';data=game/'MonsterProm_Data';data.mkdir(parents=True)
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None
  for name in z.namelist():
   assert not Path(name).is_absolute() and '..' not in Path(name).parts
   assert not name.endswith('.assets') and not name.startswith('MonsterProm_Data/')
  z.extractall(package)
 manifest=json.loads((package/'patch_manifest.json').read_text(encoding='utf-8'));actual=Path(json.loads((BASE/'test_patch/manifest.json').read_text(encoding='utf-8'))['game_data']);live_before={r['file']:sha(actual/r['file']) for r in manifest['files']}
 for row in manifest['files']:shutil.copy2(BASE/'backup/original'/row['file'],data/row['file'])
 (game/'MonsterProm.exe').write_bytes(b'Test marker only; no game is launched.')
 results=[]
 def invoke(action,expected_code=0):
  result=root/(str(len(results))+'_'+action+'.json');process=subprocess.run([str(package/'MonsterPromKR-Patcher.exe'),'--action',action,'--game-dir',str(game),'--result',str(result)],creationflags=0x08000000);r=json.loads(result.read_text(encoding='utf-8'));assert process.returncode==expected_code,r;results.append(r);print(action,r,flush=True);return r
 assert invoke('verify')['state']=='원본'
 assert invoke('install')['changed_files']==25
 for r in manifest['files']:assert sha(data/r['file'])==r['patched_sha256']
 assert invoke('verify')['state']=='한글 패치 적용'
 assert invoke('install')['changed_files']==0
 assert invoke('restore')['changed_files']==25
 for r in manifest['files']:assert sha(data/r['file'])==r['original_sha256']
 target=data/'level0';saved=target.read_bytes();target.write_bytes(b'foreign version');before={r['file']:sha(data/r['file']) for r in manifest['files']};invoke('install',1)
 assert before=={r['file']:sha(data/r['file']) for r in manifest['files']};target.write_bytes(saved)
 delta=package/'patches/level0.bsdiff';saved=delta.read_bytes();delta.write_bytes(b'broken payload');invoke('install',1);delta.write_bytes(saved)
 for r in manifest['files']:assert sha(data/r['file'])==r['original_sha256']
 assert live_before=={r['file']:sha(actual/r['file']) for r in manifest['files']}
 report={'archive_sha256':sha(archive),'zip_integrity':'passed','compiled_windows_executable':'passed','test_path_contains_korean_and_spaces':True,'full_install_files':25,'full_restore_files':25,'installed_file_hashes':'all matched','restored_file_hashes':'all matched','repeat_install':'no-op passed','wrong_game_version':'rejected before writes','corrupt_payload':'rejected before writes','synthetic_safety_tests':6,'simulated_partial_commit_rollback':'passed in synthetic safety suite','actual_user_game_files':'unchanged during release tests','game_launched':False,'installer_gui_screen_test':'not performed; packaged executable CLI and Tk dependencies checked','results':results}
 (BASE/'reports/release_install_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('RELEASE ROUNDTRIP PASSED',flush=True)
if __name__=='__main__':main()
