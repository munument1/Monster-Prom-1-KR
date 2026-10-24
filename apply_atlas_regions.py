"""Install generated lettering regions while preserving unrelated atlas pixels."""
from pathlib import Path
import argparse,json,collections,re,subprocess
import UnityPy
from PIL import Image
from config import GAME_DATA
from patch_revision import sha,install_revision
BASE=Path(__file__).parent.resolve()
def main():
 p=argparse.ArgumentParser();p.add_argument('spec');args=p.parse_args()
 if 'MonsterProm.exe' in subprocess.run(['tasklist','/FI','IMAGENAME eq MonsterProm.exe','/FO','CSV','/NH'],capture_output=True,text=True).stdout:raise SystemExit('Close Monster Prom first.')
 spec=json.loads(Path(args.spec).read_text(encoding='utf-8'));name=spec['revision'];assert re.fullmatch('[a-z0-9_]+',name)
 grouped=collections.defaultdict(list)
 seen=set()
 for item in spec['patches']:
  assert Path(item['file']).name==item['file']
  key=(item['file'],item['texture_id']);assert key not in seen,'Combine regions for the same texture in one patch entry.';seen.add(key)
  grouped[item['file']].append(item)
 stage=BASE/'test_patch'/name;stage.mkdir(parents=True,exist_ok=True);records=[]
 for fn,items in grouped.items():
  e=UnityPy.load(str(GAME_DATA/fn));objects={o.path_id:o for o in e.objects};original={pid:o.get_raw_data() for pid,o in objects.items()};expected={};images={}
  for item in items:
   pid=item['texture_id'];o=objects[pid];assert o.type.name=='Texture2D';d=o.read();canvas=d.image.convert('RGBA');source=(BASE/item['source']).resolve();assert source.is_relative_to(BASE)
   if item.get('baseline'):
    baseline=(BASE/item['baseline']).resolve();assert baseline.is_relative_to(BASE/'backup') and baseline.name==fn
    reference=UnityPy.load(str(baseline));reference_objects={x.path_id:x for x in reference.objects}
    if (GAME_DATA/(fn+'.resS')).exists():reference.load_file(str(GAME_DATA/(fn+'.resS')))
    restored=reference_objects[pid].read().image.convert('RGBA');assert restored.size==canvas.size
    canvas=restored
   source_image=Image.open(source).convert('RGBA')
   generated=source_image.resize(canvas.size,Image.Resampling.LANCZOS)
   def valid_box(box,size):
    assert len(box)==4 and all(isinstance(v,int) for v in box)
    assert 0<=box[0]<box[2]<=size[0] and 0<=box[1]<box[3]<=size[1],box
   for box in item.get('regions',[]):
    valid_box(box,canvas.size);canvas.paste(generated.crop(box),tuple(box[:2]))
   for placement in item.get('placements',[]):
    src=placement['source_box'];dst=placement['target_box']
    valid_box(src,source_image.size);valid_box(dst,canvas.size)
    fragment=source_image.crop(src).resize((dst[2]-dst[0],dst[3]-dst[1]),Image.Resampling.LANCZOS)
    if placement.get('preserve_target_alpha'):
     fragment.putalpha(canvas.crop(dst).getchannel('A'))
    canvas.paste(fragment,tuple(dst[:2]))
   d.set_image(canvas,target_format=4,mipmap_count=d.m_MipCount);d.save();expected[pid]=o.data;images[pid]=canvas
   canvas.save(stage/(fn+'_'+str(pid)+'.png'))
  out=stage/fn;out.write_bytes(e.file.save());check=UnityPy.load(str(out));assert len(check.objects)==len(original)
  for o in check.objects:
   assert o.get_raw_data()==expected.get(o.path_id,original[o.path_id]),(fn,o.path_id)
   if o.path_id in images:assert o.read().image.convert('RGBA').tobytes()==images[o.path_id].tobytes()
  records.append({'file':fn,'before_sha256':sha(GAME_DATA/fn),'patched_sha256':sha(out),'changed_objects':sorted(expected),'object_count':len(original)})
 install_revision(stage,records,name);print('Installed',name)
if __name__=='__main__':main()
