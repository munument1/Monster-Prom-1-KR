"""Verify archive extraction, folder merging and manual backup restoration."""
from pathlib import Path
import hashlib,json,shutil,tempfile,zipfile
BASE=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 archive=BASE/'release_dist/Monster-Prom-1-KR-v0.1-Overwrite.zip';parent=BASE/'release_test';parent.mkdir(exist_ok=True);root=Path(tempfile.mkdtemp(prefix='덮어쓰기 검증 ',dir=parent));game=root/'게임 폴더';data=game/'MonsterProm_Data';data.mkdir(parents=True);backup=root/'수동 백업';backup.mkdir();manifest=json.loads((BASE/'release_build/package/patch_manifest.json').read_text(encoding='utf-8'));entries=manifest['files']
 for row in entries:
  source=BASE/'backup/original'/row['file'];shutil.copy2(source,data/row['file']);shutil.copy2(source,backup/row['file'])
 sentinel=data/'패치하지 않는 기존 파일.txt';sentinel.write_text('원래 있던 파일 보존',encoding='utf-8')
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None;paths=z.namelist();expected={'MonsterProm_Data/'+r['file'] for r in entries};actual={p for p in paths if p.startswith('MonsterProm_Data/')};assert actual==expected
  assert not any(p.lower().endswith(('.exe','.dll','.sh','.bat','.ps1')) for p in paths)
  for p in paths:assert not Path(p).is_absolute() and '..' not in Path(p).parts and '\\' not in p
  z.extractall(game)
  checksum_lines=z.read('PATCHED_SHA256SUMS.txt').decode('ascii').splitlines()
  for line in checksum_lines:
   expected_hash,name=line.split('  ',1);assert sha(game/name)==expected_hash
 for row in entries:assert sha(data/row['file'])==row['patched_sha256']
 assert sentinel.read_text(encoding='utf-8')=='원래 있던 파일 보존'
 for row in entries:shutil.copy2(backup/row['file'],data/row['file'])
 for row in entries:assert sha(data/row['file'])==row['original_sha256']
 assert sentinel.read_text(encoding='utf-8')=='원래 있던 파일 보존'
 report={'archive_sha256':sha(archive),'zip_integrity':'passed','safe_relative_paths':'passed','case_sensitive_archive_names':'exact MonsterProm_Data and original file names','modified_file_count':len(entries),'overwrite_file_hashes':'all matched Windows v0.1','unmodified_existing_files':'preserved during merge','manual_backup_restore_hashes':'all original hashes matched','checksum_list':'matches extracted files','installer_executable_in_archive':False,'actual_game_installation':'not modified','steam_deck_runtime_test':'not performed','target':'Windows version via Proton'}
 (BASE/'reports/release_overwrite_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
if __name__=='__main__':main()
