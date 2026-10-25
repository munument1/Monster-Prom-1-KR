"""Package the exact v0.1 patched files for manual copy/merge installation."""
from pathlib import Path
import hashlib,json,zipfile

BASE=Path(__file__).resolve().parents[1]
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()
def main():
 manifest=json.loads((BASE/'release_build/package/patch_manifest.json').read_text(encoding='utf-8'))
 assert manifest['version']=='0.1'
 current=json.loads((BASE/'test_patch/manifest.json').read_text(encoding='utf-8'));current_by_name={r['file']:r for r in current['files']}
 dest=BASE/'release_dist';dest.mkdir(exist_ok=True);out=dest/'Monster-Prom-1-KR-v0.1-Overwrite.zip';original=[];patched=[]
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for row in manifest['files']:
   name=row['file'];assert Path(name).name==name and '/' not in name and '\\' not in name
   assert row['patched_sha256']==current_by_name[name]['patched_sha256'],name
   source=BASE/'test_patch/MonsterProm_Data'/name;assert sha(source)==row['patched_sha256'],name
   target='MonsterProm_Data/'+name;print('Packing:',target,flush=True);z.write(source,target)
   original.append(row['original_sha256']+'  '+target);patched.append(row['patched_sha256']+'  '+target)
  z.write(BASE/'release/INSTALL_OVERWRITE_KO.md','설치 안내_SteamDeck.txt')
  z.write(BASE/'release/RELEASE_NOTES_KO.md','변경 내역.txt')
  z.writestr('ORIGINAL_SHA256SUMS.txt','\n'.join(original)+'\n');z.writestr('PATCHED_SHA256SUMS.txt','\n'.join(patched)+'\n')
  z.writestr('overwrite_manifest.json',json.dumps({'version':'0.1','format':'manual overwrite','target':'Windows build 20786767; Steam Deck via Proton','steam_deck_runtime_test':'not performed','files':manifest['files']},ensure_ascii=False,indent=2)+'\n')
 report={'version':'0.1','archive':out.name,'archive_size':out.stat().st_size,'sha256':sha(out),'modified_files':len(manifest['files']),'uncompressed_game_file_bytes':sum(r['patched_size'] for r in manifest['files']),'same_file_hashes_as_windows_v01':True,'contains_install_exe':False,'format':'MonsterProm_Data directory merge/overwrite','steam_deck_target':'Windows build via Proton','steam_deck_runtime_test':'not performed'}
 (BASE/'reports/release_overwrite_package.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 checks=[]
 for name in ['Monster-Prom-1-KR-v0.1.zip',out.name]:
  path=dest/name;checks.append(sha(path)+'  '+name)
 (dest/'SHA256SUMS.txt').write_text('\n'.join(checks)+'\n',encoding='ascii');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
