import UnityPy, json, collections
from unity_support import generator as make_generator
from pathlib import Path
from config import GAME_DATA
root=GAME_DATA
out=Path(__file__).parent/'extracted';out.mkdir(exist_ok=True)
summary=[]
generator=make_generator(root)
for p in root.iterdir():
 if p.suffix!='.assets' and not (p.name.startswith('level') and p.is_file()): continue
 print('Reading',p.name,flush=True)
 env=UnityPy.load(str(p)); env.typetree_generator=generator; counts=collections.Counter(); records=[]
 for obj in env.objects:
  counts[obj.type.name]+=1
  if obj.type.name in ('TextAsset','Font','MonoBehaviour'):
   try:
    tree=obj.read_typetree()
    rec={'path_id':obj.path_id,'type':obj.type.name,'name':tree.get('m_Name',''),'keys':list(tree)}
    if obj.type.name=='TextAsset':
     folder=out/p.name;folder.mkdir(exist_ok=True)
     text=tree.get('m_Script',''); dest=folder/(str(obj.path_id)+'.txt')
     dest.write_bytes(text.encode('utf-8',errors='surrogateescape'));rec.update(chars=len(text),sample=text[:250])
    elif obj.type.name=='Font': rec['details']={k:v for k,v in tree.items() if k not in ('m_FontData','m_CharacterRects','m_KerningValues')};rec['font_bytes']=len(tree.get('m_FontData',[]))
    else:
     rec['sample']=str(tree)[:600]
     folder=out/'monobehaviours'/p.name;folder.mkdir(parents=True,exist_ok=True)
     (folder/(str(obj.path_id)+'.json')).write_text(json.dumps(tree,ensure_ascii=False,default=str),encoding='utf-8',errors='surrogateescape')
    records.append(rec)
   except Exception as e:records.append({'path_id':obj.path_id,'type':obj.type.name,'error':str(e)})
 summary.append({'file':p.name,'counts':dict(counts),'records':records})
 (out/'inventory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8',errors='surrogateescape')
print('DONE',flush=True)
