"""Install validated local revision files while preserving the original backup."""
from pathlib import Path
import json,hashlib,shutil
BASE=Path(__file__).parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def install_revision(stage,records,name):
 patch=BASE/'test_patch';m=json.loads((patch/'manifest.json').read_text(encoding='utf-8'));root=Path(m['game_data']);backup=BASE/'backup'/('before_'+name)
 if backup.exists():raise RuntimeError('Revision backup exists: '+str(backup))
 for item in m['files']:assert sha(root/item['file'])==item['patched_sha256'],item['file']
 for r in records:assert sha(root/r['file'])==r['before_sha256'];assert sha(stage/r['file'])==r['patched_sha256']
 backup.mkdir(parents=True);shutil.copy2(patch/'manifest.json',backup/'manifest.json')
 for r in records:shutil.copy2(root/r['file'],backup/r['file'])
 for r in records:
  item=next((x for x in m['files'] if x['file']==r['file']),None)
  if item is None:
   original=BASE/'backup/original'/r['file'];assert not original.exists();shutil.copy2(root/r['file'],original)
   item={'file':r['file'],'original_sha256':r['before_sha256'],'changed_objects':[],'object_count':r['object_count']};m['files'].append(item)
  item['patched_sha256']=r['patched_sha256'];item['changed_objects']=sorted(set(item['changed_objects'])|set(r['changed_objects']))
  m['changes'].append({'file':r['file'],'feature':name,'objects':r['changed_objects']})
 try:
  for r in records:
   for dest in [root/r['file'],patch/'MonsterProm_Data'/r['file']]:shutil.copy2(stage/r['file'],dest);assert sha(dest)==r['patched_sha256']
  (patch/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
 except Exception:
  for r in records:
   for dest in [root/r['file'],patch/'MonsterProm_Data'/r['file']]:shutil.copy2(backup/r['file'],dest)
  shutil.copy2(backup/'manifest.json',patch/'manifest.json');raise
 (stage/'verification.json').write_text(json.dumps({'revision':name,'files':records,'visual_verification':'pending user'},ensure_ascii=False,indent=2),encoding='utf-8')
