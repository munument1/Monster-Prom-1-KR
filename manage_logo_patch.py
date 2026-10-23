from pathlib import Path
import argparse,json,hashlib,shutil,subprocess
BASE=Path(__file__).parent
STAGE=BASE/'artwork'/'logo'/'patch_v1'
BACKUP=BASE/'backup'/'before_logo_v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['apply','restore']);a=p.parse_args()
    if 'MonsterProm.exe' in subprocess.run(['tasklist','/FI','IMAGENAME eq MonsterProm.exe','/FO','CSV','/NH'],capture_output=True,text=True).stdout:raise SystemExit('Close Monster Prom first.')
    report=json.loads((STAGE/'verification.json').read_text(encoding='utf-8'))
    manifest=json.loads((STAGE/'combined_manifest.json').read_text(encoding='utf-8'))
    root=Path(manifest['game_data'])
    for r in report['files']:
        assert sha(root/r['file']) in (r['before_sha256'],r['patched_sha256']),r['file']
        assert sha(BACKUP/r['file'])==r['before_sha256']
        assert sha(STAGE/r['file'])==r['patched_sha256']
    for r in report['files']:
        source=(STAGE if a.action=='apply' else BACKUP)/r['file']
        for dest in (root/r['file'],BASE/'test_patch'/'MonsterProm_Data'/r['file']):
            shutil.copy2(source,dest);assert sha(source)==sha(dest)
    source_manifest=STAGE/'combined_manifest.json' if a.action=='apply' else BACKUP/'manifest.json'
    shutil.copy2(source_manifest,BASE/'test_patch'/'manifest.json')
    print('Korean logo applied.' if a.action=='apply' else 'Logo restored; Korean font and text test retained.')
if __name__=='__main__':main()
