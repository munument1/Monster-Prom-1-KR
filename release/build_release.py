"""Build exact-version binary deltas and a Nexus-ready release archive."""
from pathlib import Path
import argparse,hashlib,json,shutil,zipfile
import bsdiff4

BASE=Path(__file__).resolve().parents[1]
VERSION='0.1.0-beta.1'
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()
def payload():
 source=json.loads((BASE/'test_patch/manifest.json').read_text(encoding='utf-8'))
 dest=BASE/'release_build/package';(dest/'patches').mkdir(parents=True,exist_ok=True);records=[]
 for row in source['files']:
  name=row['file'];old=BASE/'backup/original'/name;new=BASE/'test_patch/MonsterProm_Data'/name;out=dest/'patches'/(name+'.bsdiff')
  assert sha(old)==row['original_sha256'] and sha(new)==row['patched_sha256'],name
  stamp=out.with_suffix('.source.json');signature={'original':row['original_sha256'],'patched':row['patched_sha256']}
  if not out.exists() or not stamp.exists() or json.loads(stamp.read_text())!=signature:
   print('Building delta:',name,flush=True);out.write_bytes(bsdiff4.diff(old.read_bytes(),new.read_bytes()));stamp.write_text(json.dumps(signature))
  # Reconstruct every payload independently before packaging it.
  print('Verifying delta:',name,flush=True);restored=bsdiff4.patch(old.read_bytes(),out.read_bytes());assert hashlib.sha256(restored).hexdigest()==row['patched_sha256'],name;del restored
  records.append({'file':name,'original_sha256':row['original_sha256'],'patched_sha256':row['patched_sha256'],'original_size':old.stat().st_size,'patched_size':new.stat().st_size,'delta':'patches/'+out.name,'delta_sha256':sha(out),'delta_size':out.stat().st_size})
 manifest={'format':1,'version':VERSION,'game':'Monster Prom 1','steam_app_id':743450,'steam_build_id':20786767,'game_exe':'MonsterProm.exe','data_dir':'MonsterProm_Data','language':'ENGLISH','files':records}
 (dest/'patch_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Payload verified:',len(records),'files;',sum(r['delta_size'] for r in records),'delta bytes',flush=True)
def archive():
 package=BASE/'release_build/package';dist=BASE/'release_dist';dist.mkdir(exist_ok=True)
 exe=BASE/'release_build/installer/MonsterPromKR-Patcher.exe';assert exe.is_file();shutil.copy2(exe,package/exe.name)
 for source,target in [('INSTALL_KO.md','설치 안내.txt'),('NEXUS_DESCRIPTION_KO.md','넥서스 소개문.txt'),('RELEASE_NOTES_KO.md','변경 내역.txt')]:shutil.copy2(BASE/'release'/source,package/target)
 import importlib.metadata as metadata,sys
 licenses=package/'licenses';licenses.mkdir(exist_ok=True)
 shutil.copy2(Path(sys.base_prefix)/'LICENSE.txt',licenses/'Python-LICENSE.txt')
 for item in (Path(sys.base_prefix)/'tcl').rglob('license.terms'):shutil.copy2(item,licenses/(item.parent.name+'-license.terms.txt'))
 for name,target in [('bsdiff4','bsdiff4-LICENSE.txt'),('pyinstaller','PyInstaller-COPYING.txt')]:
  d=metadata.distribution(name);item=next(p for p in d.files if '/licenses/' in str(p) and ('LICENSE' in str(p) or 'COPYING' in str(p)));shutil.copy2(d.locate_file(item),licenses/target)
 out=dist/f'Monster-Prom-1-KR-v{VERSION}.zip'
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(package.rglob('*')):
   if p.is_file() and not p.name.endswith('.source.json'):z.write(p,p.relative_to(package).as_posix())
 digest=sha(out);(dist/'SHA256SUMS.txt').write_text(digest+'  '+out.name+'\n',encoding='ascii')
 report={'version':VERSION,'archive':out.name,'archive_size':out.stat().st_size,'sha256':digest,'payload_files':len(json.loads((package/'patch_manifest.json').read_text())['files']),'original_game_files_in_archive':False,'game_screen_check':'pending user'}
 (BASE/'reports/release_package.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('step',choices=['payload','archive']);a=p.parse_args();payload() if a.step=='payload' else archive()
