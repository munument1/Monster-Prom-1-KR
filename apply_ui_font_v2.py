"""Add Second Term/menu artwork and connect NGUI UIFonts to the Korean TTF."""
from pathlib import Path
import json,hashlib,shutil,copy,math,subprocess
import UnityPy
from PIL import Image,ImageOps
from config import GAME_DATA
from unity_support import generator
from apply_logo_patch import full_rectangle
BASE=Path(__file__).parent
STAGE=BASE/'artwork/ui/patch_v2'
BACKUP=BASE/'backup/before_ui_font_v2'
PATCH=BASE/'test_patch'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if 'MonsterProm.exe' in subprocess.run(['tasklist','/FI','IMAGENAME eq MonsterProm.exe','/FO','CSV','/NH'],capture_output=True,text=True).stdout:raise SystemExit('Close Monster Prom first.')
 if BACKUP.exists():raise SystemExit('Revision backup exists; refusing to overwrite.')
 m=json.loads((PATCH/'manifest.json').read_text(encoding='utf-8'))
 for item in m['files']:assert sha(GAME_DATA/item['file'])==item['patched_sha256'],item['file']
 STAGE.mkdir(parents=True,exist_ok=True);gen=generator(GAME_DATA);records=[]
 for fn in ('resources.assets','sharedassets0.assets','sharedassets1.assets'):
  print('Building',fn,flush=True)
  e=UnityPy.load(str(GAME_DATA/fn));e.typetree_generator=gen
  objects={o.path_id:o for o in e.objects};original={pid:o.get_raw_data() for pid,o in objects.items()};expected={};images={}
  if fn in ('resources.assets','sharedassets0.assets'):
   fileid=0
   if fn=='sharedassets0.assets':
    ext=copy.deepcopy(e.file.externals[0]);ext.path='resources.assets';ext.guid=bytes(16);ext.type=0;e.file.externals.append(ext);fileid=len(e.file.externals)
   for pid in ([5502,5509,5524,5538,5545,5555,5566] if fn=='resources.assets' else [11]):
    o=objects[pid];t=o.read_typetree();assert t['mDynamicFont']['m_PathID']==0
    t['mDynamicFont']={'m_FileID':fileid,'m_PathID':3406}
    t['mDynamicFontSize']=t['mFont']['mSize']
    for key in ('mMat','mAtlas','mReplacement'):t[key]={'m_FileID':0,'m_PathID':0}
    expected[pid]=o.save_typetree(t)
  if fn=='resources.assets':
   pid=1540;o=objects[pid];d=o.read();src=Image.open(BASE/'artwork/logo/monster_prom_second_term_ko_v2.png').convert('RGBA')
   crop=src.crop(src.getchannel('A').point(lambda a:255 if a>8 else 0).getbbox())
   fit=ImageOps.contain(crop,(d.m_Width,d.m_Height),Image.Resampling.LANCZOS)
   canvas=Image.new('RGBA',(d.m_Width,d.m_Height));canvas.paste(fit,((d.m_Width-fit.width)//2,(d.m_Height-fit.height)//2))
   d.set_image(canvas,target_format=4,mipmap_count=d.m_MipCount);d.save();expected[pid]=o.data;images[pid]=canvas
   sprite=objects[4914];t=sprite.read_typetree();full_rectangle(t,d.m_Width,d.m_Height);expected[4914]=sprite.save_typetree(t)
  if fn=='sharedassets1.assets':
   o=objects[6];d=o.read();canvas=d.image.convert('RGBA')
   generated=Image.open(BASE/'artwork/ui/generated/main_menu_ko_v2.png').convert('RGBA').resize(canvas.size,Image.Resampling.LANCZOS)
   for pid in (31,32,37,39,41,49):
    t=objects[pid].read_typetree();r=t['m_RD']['textureRect'];assert ((t['m_RD']['settingsRaw']>>2)&15)==0
    box=(math.floor(r['x']),canvas.height-math.ceil(r['y']+r['height']),math.ceil(r['x']+r['width']),canvas.height-math.floor(r['y']))
    canvas.paste(generated.crop(box),box[:2])
   canvas.save(STAGE/'main_menu_installed.png');d.set_image(canvas,target_format=4,mipmap_count=d.m_MipCount);d.save();expected[6]=o.data;images[6]=canvas
  out=STAGE/fn;out.write_bytes(e.file.save())
  check=UnityPy.load(str(out));primary=list(check.objects);check.typetree_generator=gen;check.load_file(str(GAME_DATA/'globalgamemanagers.assets'))
  assert len(primary)==len(original)
  for o in primary:
   assert o.get_raw_data()==expected.get(o.path_id,original[o.path_id]),(fn,o.path_id)
   if o.path_id in images:assert o.read().image.convert('RGBA').tobytes()==images[o.path_id].tobytes()
   if o.path_id in ([5502,5509,5524,5538,5545,5555,5566] if fn=='resources.assets' else [11] if fn=='sharedassets0.assets' else []):assert o.read_typetree()['mDynamicFont']['m_PathID']==3406
  records.append({'file':fn,'before_sha256':sha(GAME_DATA/fn),'patched_sha256':sha(out),'changed_objects':sorted(expected),'object_count':len(original)})
  print('Verified',fn,sorted(expected),flush=True)
 BACKUP.mkdir(parents=True);shutil.copy2(PATCH/'manifest.json',BACKUP/'manifest.json')
 for r in records:shutil.copy2(GAME_DATA/r['file'],BACKUP/r['file'])
 for r in records:
  item=next((x for x in m['files'] if x['file']==r['file']),None)
  if item is None:
   original_backup=BASE/'backup/original'/r['file'];assert not original_backup.exists();shutil.copy2(GAME_DATA/r['file'],original_backup)
   item={'file':r['file'],'original_sha256':r['before_sha256'],'changed_objects':[],'object_count':r['object_count']};m['files'].append(item)
  item['patched_sha256']=r['patched_sha256'];item['changed_objects']=sorted(set(item['changed_objects'])|set(r['changed_objects']))
  m['changes'].append({'file':r['file'],'feature':'Second Term, menu images and NGUI dynamic font v2','objects':r['changed_objects']})
  shutil.copy2(STAGE/r['file'],GAME_DATA/r['file']);shutil.copy2(STAGE/r['file'],PATCH/'MonsterProm_Data'/r['file']);assert sha(GAME_DATA/r['file'])==r['patched_sha256']
 (PATCH/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
 (STAGE/'verification.json').write_text(json.dumps({'files':records,'font_connection':'8 NGUI UIFonts -> resources.assets:3406','visual_verification':'pending user'},ensure_ascii=False,indent=2),encoding='utf-8')
 print('Installed v2; screen check pending user.')
if __name__=='__main__':main()
