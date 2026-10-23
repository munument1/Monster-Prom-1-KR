"""Repair voice-popup wrapping and localize remaining setup image captions."""
from pathlib import Path
import json,subprocess
import UnityPy
from PIL import Image
from config import GAME_DATA
from unity_support import generator
from patch_revision import sha,install_revision
BASE=Path(__file__).parent
def main():
 if 'MonsterProm.exe' in subprocess.run(['tasklist','/FI','IMAGENAME eq MonsterProm.exe','/FO','CSV','/NH'],capture_output=True,text=True).stdout:raise SystemExit('Close Monster Prom first.')
 stage=BASE/'artwork/ui/patch_v3';stage.mkdir(parents=True,exist_ok=True);gen=generator(GAME_DATA);records=[]
 for fn in ('level1','sharedassets1.assets','sharedassets2.assets'):
  print('Layout/images',fn,flush=True)
  e=UnityPy.load(str(GAME_DATA/fn));e.typetree_generator=gen;objects={o.path_id:o for o in e.objects};original={pid:o.get_raw_data() for pid,o in objects.items()};expected={};images={}
  if fn=='level1':
   for pid,size in [(784,34),(925,52),(1035,28)]:
    # IDs refer to fixed labels in this game build; fail if the shape changed.
    o=objects[pid];t=o.read_typetree();assert 'mText' in t,(fn,pid)
    if pid==1035:
     assert 'MAKE YOUR' in t['mText'] or '연기' in t['mText'],t['mText']
     t['mText']='직접 연기하기\n(음성 효과 없음)'
    t['mFontSize']=size;t['mSpacingX']=0;t['mFloatSpacingX']=0.0;t['mMaxLineCount']=2
    expected[pid]=o.save_typetree(t)
  else:
   texids=[4] if fn=='sharedassets1.assets' else [8,10]
   for pid in texids:
    o=objects[pid];d=o.read();canvas=d.image.convert('RGBA')
    srcname={('sharedassets1.assets',4):'players234_ko_v3.png',('sharedassets2.assets',8):'expansion_boards_ko_v3.png',('sharedassets2.assets',10):'player1_ko_v3.png'}[(fn,pid)]
    generated=Image.open(BASE/'artwork/ui/generated'/srcname).convert('RGBA').resize(canvas.size,Image.Resampling.LANCZOS)
    boxes={('sharedassets1.assets',4):[(0,605,416,703),(0,1100,440,1210),(1280,1381,1696,1484)],('sharedassets2.assets',8):[(225,890,870,1185),(100,1530,700,1735),(165,1735,640,1850)],('sharedassets2.assets',10):[(699,1955,983,2048)]}[(fn,pid)]
    for box in boxes:canvas.paste(generated.crop(box),box[:2])
    canvas.save(stage/(fn+'_'+str(pid)+'.png'));d.set_image(canvas,target_format=4,mipmap_count=d.m_MipCount);d.save();expected[pid]=o.data;images[pid]=canvas
  out=stage/fn;out.write_bytes(e.file.save());check=UnityPy.load(str(out));primary=list(check.objects);check.typetree_generator=gen;check.load_file(str(GAME_DATA/'globalgamemanagers.assets'));assert len(primary)==len(original)
  for o in primary:
   assert o.get_raw_data()==expected.get(o.path_id,original[o.path_id]),(fn,o.path_id)
   if o.path_id in images:assert o.read().image.convert('RGBA').tobytes()==images[o.path_id].tobytes()
  records.append({'file':fn,'before_sha256':sha(GAME_DATA/fn),'patched_sha256':sha(out),'changed_objects':sorted(expected),'object_count':len(original)})
 install_revision(stage,records,'layout_images_v3')
 print('Installed v3; voice dialog uses explicit line breaks and bounded font sizes.')
if __name__=='__main__':main()
