from pathlib import Path
import json,hashlib,shutil,argparse,subprocess
BASE=Path(__file__).parent
PATCH=BASE/'test_patch'
BACKUP=BASE/'backup'/'original'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('action',choices=('apply','restore','status'));args=parser.parse_args()
 manifest=json.loads((PATCH/'manifest.json').read_text(encoding='utf-8'));root=Path(manifest['game_data'])
 if args.action!='status':
  running=subprocess.run(['tasklist','/FI','IMAGENAME eq MonsterProm.exe','/FO','CSV','/NH'],capture_output=True,text=True).stdout
  if 'MonsterProm.exe' in running:raise SystemExit('Close Monster Prom before applying or restoring the test patch.')
 # Preflight every target before modifying any file.
 for item in manifest['files']:
  target=root/item['file'];current=sha(target)
  if current not in (item['original_sha256'],item['patched_sha256']):raise SystemExit(f'Unexpected game version or external modification: {target}')
  source=PATCH/'MonsterProm_Data'/item['file']
  if sha(source)!=item['patched_sha256']:raise SystemExit(f'Patch hash mismatch: {source}')
  backup=BACKUP/item['file']
  if backup.exists() and sha(backup)!=item['original_sha256']:raise SystemExit(f'Backup hash mismatch: {backup}')
  if current==item['patched_sha256'] and not backup.exists():raise SystemExit(f'Original backup missing: {backup}')
 for item in manifest['files']:
  target=root/item['file'];backup=BACKUP/item['file']
  if args.action=='apply':
   BACKUP.mkdir(parents=True,exist_ok=True)
   if not backup.exists():shutil.copy2(target,backup)
   shutil.copy2(PATCH/'MonsterProm_Data'/item['file'],target)
   assert sha(target)==item['patched_sha256']
  elif args.action=='restore' and backup.exists():
   shutil.copy2(backup,target);assert sha(target)==item['original_sha256']
  print(item['file'], 'PATCHED' if sha(target)==item['patched_sha256'] else 'ORIGINAL')
 if args.action=='apply':shutil.copy2(PATCH/'manifest.json',BACKUP/'manifest.json')
if __name__=='__main__':main()
