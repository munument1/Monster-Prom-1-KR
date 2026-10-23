from pathlib import Path
import json,hashlib,shutil,struct,subprocess,copy
import UnityPy
from PIL import Image,ImageOps

BASE=Path(__file__).parent
PATCH=BASE/'test_patch'
from config import GAME_DATA
ROOT=GAME_DATA
BACKUP=BASE/'backup'/'before_logo_v1'
STAGE=BASE/'artwork'/'logo'/'patch_v1'
SOURCE=BASE/'artwork'/'logo'/'monster_prom_logo_ko_v1.png'
TARGETS={'resources.assets':[(224,3593),(915,4289)],'sharedassets0.assets':[(4,8)]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def full_rectangle(t,w,h):
    # Existing sprites have tightly triangulated English-logo silhouettes.
    # A rectangular mesh prevents those old triangles clipping the new artwork.
    ppu=t['m_PixelsToUnits'];pivot=t['m_Pivot']
    l=-pivot['x']*w/ppu;r=(1-pivot['x'])*w/ppu
    b=-pivot['y']*h/ppu;top=(1-pivot['y'])*h/ppu
    rd=t['m_RD'];vd=rd['m_VertexData']
    vd['m_VertexCount']=4
    assert vd['m_Channels'][0]['dimension']==3 and vd['m_Channels'][3]['offset']==12
    vd['m_DataSize']=b''.join(struct.pack('<fffff',x,y,0,u,v) for x,y,u,v in [(l,b,0,0),(l,top,0,1),(r,top,1,1),(r,b,1,0)])
    rd['m_IndexBuffer']=list(struct.pack('<6H',0,1,2,0,2,3))
    sub=copy.deepcopy(rd['m_SubMeshes'][0]);sub.update(firstByte=0,indexCount=6,firstVertex=0,vertexCount=4)
    sub['localAABB']={'m_Center':{'x':(l+r)/2,'y':(b+top)/2,'z':0.0},'m_Extent':{'x':(r-l)/2,'y':(top-b)/2,'z':0.0}}
    rd['m_SubMeshes']=[sub]
    rd['textureRect']={'x':0.0,'y':0.0,'width':float(w),'height':float(h)}
    rd['textureRectOffset']={'x':0.0,'y':0.0}

def main():
    if 'MonsterProm.exe' in subprocess.run(['tasklist','/FI','IMAGENAME eq MonsterProm.exe','/FO','CSV','/NH'],capture_output=True,text=True).stdout:
        raise SystemExit('Close Monster Prom first.')
    if BACKUP.exists():raise SystemExit('Logo v1 backup already exists; refusing to overwrite it.')
    manifest=json.loads((PATCH/'manifest.json').read_text(encoding='utf-8'))
    for item in manifest['files']:
        assert sha(ROOT/item['file'])==item['patched_sha256'],item['file']
        assert sha(BASE/'backup'/'original'/item['file'])==item['original_sha256']
    STAGE.mkdir(parents=True,exist_ok=True)
    generated=Image.open(SOURCE).convert('RGBA')
    bbox=generated.getchannel('A').point(lambda x:255 if x>8 else 0).getbbox()
    cropped=generated.crop(bbox)
    records=[]
    for filename,pairs in TARGETS.items():
        print('Building',filename,flush=True)
        env=UnityPy.load(str(ROOT/filename))
        objects={o.path_id:o for o in env.objects}
        originals={pid:o.get_raw_data() for pid,o in objects.items()}
        changed=set();expected_images={};expected_sprites={}
        for texid,spriteid in pairs:
            obj=objects[texid];data=obj.read();old=data.image.convert('RGBA')
            oldbox=old.getchannel('A').point(lambda x:255 if x>8 else 0).getbbox()
            if oldbox is None:oldbox=(0,0,old.width,old.height)
            fitted=ImageOps.contain(cropped,(oldbox[2]-oldbox[0],oldbox[3]-oldbox[1]),Image.Resampling.LANCZOS)
            canvas=Image.new('RGBA',old.size,(0,0,0,0))
            pos=(oldbox[0]+(oldbox[2]-oldbox[0]-fitted.width)//2,oldbox[1]+(oldbox[3]-oldbox[1]-fitted.height)//2)
            canvas.paste(fitted,pos)
            preview=STAGE/f'{filename}_{texid}.png';canvas.save(preview)
            data.set_image(canvas,target_format=4,mipmap_count=data.m_MipCount);data.save()
            sprite=objects[spriteid];tree=sprite.read_typetree()
            full_rectangle(tree,canvas.width,canvas.height);sprite.save_typetree(tree)
            expected_sprites[spriteid]=sprite.data;expected_images[texid]=canvas
            changed.update([texid,spriteid])
        dest=STAGE/filename;dest.write_bytes(env.file.save())
        check=UnityPy.load(str(dest));checked={o.path_id:o for o in check.objects}
        assert set(checked)==set(objects)
        for pid,o in checked.items():
            if pid not in changed:assert o.get_raw_data()==originals[pid],(filename,pid)
            elif pid in expected_images:
                data=o.read();assert data.image.convert('RGBA').tobytes()==expected_images[pid].tobytes()
                assert not data.m_StreamData.path and data.m_TextureFormat==4
            else:
                assert o.get_raw_data()==expected_sprites[pid]
                assert o.read_typetree()['m_RD']['m_VertexData']['m_VertexCount']==4
        records.append({'file':filename,'before_sha256':sha(ROOT/filename),'patched_sha256':sha(dest),'changed_objects':sorted(changed),'object_count':len(objects)})
        print('Verified',filename,flush=True)
    # Back up the installed font-test state and its manifest before any mutation.
    BACKUP.mkdir(parents=True)
    shutil.copy2(PATCH/'manifest.json',BACKUP/'manifest.json')
    for record in records:shutil.copy2(ROOT/record['file'],BACKUP/record['file'])
    for record in records:
        item=next((x for x in manifest['files'] if x['file']==record['file']),None)
        if item is None:
            original=BASE/'backup'/'original'/record['file']
            assert not original.exists()
            shutil.copy2(ROOT/record['file'],original)
            item={'file':record['file'],'original_sha256':record['before_sha256'],'changed_objects':[],'object_count':record['object_count']}
            manifest['files'].append(item)
        item['patched_sha256']=record['patched_sha256']
        item['changed_objects']=sorted(set(item['changed_objects'])|set(record['changed_objects']))
        manifest['changes'].append({'file':record['file'],'feature':'Korean generated logo v1','objects':record['changed_objects']})
    manifest['logo_source']=str(SOURCE)
    manifest['visual_verification']='pending user'
    (STAGE/'combined_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    try:
        for record in records:
            shutil.copy2(STAGE/record['file'],ROOT/record['file'])
            shutil.copy2(STAGE/record['file'],PATCH/'MonsterProm_Data'/record['file'])
            assert sha(ROOT/record['file'])==record['patched_sha256']
        (PATCH/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    except Exception:
        for record in records:
            shutil.copy2(BACKUP/record['file'],ROOT/record['file'])
            if record['file']!='sharedassets0.assets':shutil.copy2(BACKUP/record['file'],PATCH/'MonsterProm_Data'/record['file'])
        shutil.copy2(BACKUP/'manifest.json',PATCH/'manifest.json')
        raise
    report={'source':str(SOURCE),'backup':str(BACKUP),'files':records,'visual_verification':'pending user','executable':str(ROOT.parent/'MonsterProm.exe')}
    (STAGE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
