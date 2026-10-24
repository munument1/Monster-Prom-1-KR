"""Verify installed image dimensions, alpha and pixels outside declared lettering regions."""
from pathlib import Path
import argparse,json
import UnityPy
from PIL import Image,ImageDraw,ImageChops
from config import GAME_DATA
BASE=Path(__file__).resolve().parent

def image_from(path,pid):
    env=UnityPy.load(str(path))
    resource=GAME_DATA/(path.name+'.resS')
    if resource.exists():env.load_file(str(resource))
    obj=next(o for o in env.objects if o.path_id==pid)
    return obj.read().image.convert('RGBA')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('specs',nargs='+')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    final={}
    for name in args.specs:
        spec=json.loads((BASE/name).read_text(encoding='utf-8'))
        for entry in spec['patches']:
            final[entry['file'],entry['texture_id']]=(spec['revision'],entry)
    records=[]
    for (fn,pid),(revision,entry) in final.items():
        before=BASE/entry.get('baseline','backup/before_'+revision+'/'+fn)
        original=image_from(before,pid);installed=image_from(GAME_DATA/fn,pid)
        assert original.size==installed.size,(fn,pid,'size')
        mask=Image.new('L',original.size,0);draw=ImageDraw.Draw(mask)
        for box in entry.get('regions',[]):draw.rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=255)
        for placement in entry.get('placements',[]):
            box=placement['target_box'];draw.rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=255)
        diff=ImageChops.difference(original,installed)
        for band in diff.split():assert ImageChops.multiply(band,ImageChops.invert(mask)).getbbox() is None,(fn,pid,'outside region')
        preserve_alpha=all(x.get('preserve_target_alpha') for x in entry.get('placements',[])) and not entry.get('regions')
        if preserve_alpha:assert original.getchannel('A').tobytes()==installed.getchannel('A').tobytes(),(fn,pid,'alpha')
        records.append({'file':fn,'texture_id':pid,'revision':revision,'dimensions':list(installed.size),'outside_patch_pixels':'identical','alpha_policy':'original alpha identical' if preserve_alpha else 'not required by spec','saved_decode':'passed'})
    output=BASE/args.output;output.write_text(json.dumps({'images':records,'unique_textures':len(records),'game_screen_check':'pending user'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Verified',len(records),'textures:',args.output)

if __name__=='__main__':main()
