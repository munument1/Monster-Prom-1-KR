from pathlib import Path
import json,re,collections
BASE=Path(__file__).parent
OUT=BASE/'extracted'
inventory=json.loads((OUT/'inventory.json').read_text(encoding='utf-8'))
rows=[];labels=[];aux=[]
def walk(v,path,source,pid,context):
 if isinstance(v,dict):
  context={**context,**{k:v[k] for k in ('EventName','WhoSpeaksNPC','SceneLayout','IsOptionScene') if k in v}}
  if '_Keys' in v and '_Values' in v:
   languages={}
   for i,(key,text) in enumerate(zip(v['_Keys'],v['_Values'])):
    if i>=v.get('_Count',len(v['_Keys'])):break
    if i<len(v.get('_HashCodes',[])) and v['_HashCodes'][i]<0:continue
    languages[str(key)]=text
   if languages.get('0','').strip():
    rows.append(dict(id=f'{source}:{pid}:{path}',file=source,path_id=pid,field=path,context=context,english=languages['0'],korean='',reference_languages=languages))
   return
  for k,val in v.items():
   if k=='mText' and isinstance(val,str) and val.strip():
    labels.append(dict(id=f'{source}:{pid}:{path}/{k}',file=source,path_id=pid,field=f'{path}/{k}',english=val,korean=''))
   elif isinstance(val,str) and len(val)>20 and ' ' in val and not k.startswith('m_'):
    aux.append(dict(id=f'{source}:{pid}:{path}/{k}',field=k,source=val,korean=''))
   elif isinstance(val,(dict,list)):walk(val,f'{path}/{k}',source,pid,context)
 elif isinstance(v,list):
  for i,item in enumerate(v):walk(item,f'{path}/{i}',source,pid,context)
for p in sorted((OUT/'monobehaviours').rglob('*.json')):
 walk(json.loads(p.read_text(encoding='utf-8')),'',p.parent.name,int(p.stem),{})
ui=[]
for entry in inventory:
 for r in entry['records']:
  if r['type']!='TextAsset' or 'error' in r:continue
  p=OUT/entry['file']/(str(r['path_id'])+'.txt')
  text=p.read_text(encoding='utf-8')
  # gallery_images are configuration tables, not language tables.
  if r['name'].startswith('gallery_images') or r['name']=='build_info':continue
  for n,line in enumerate(text.splitlines(),1):
   cols=line.split('\t')
   if len(cols)>1 and cols[0] and cols[1].strip():
    ui.append(dict(id=f"{entry['file']}:{r['path_id']}:{cols[0]}",asset=r['name'],path_id=r['path_id'],line=n,key=cols[0],english=cols[1],korean='',reference_columns=cols[2:]))
def save(name,data):
 with (OUT/name).open('w',encoding='utf-8',newline='\n') as f:
  for row in data:f.write(json.dumps(row,ensure_ascii=False)+'\n')
save('dialogue_and_localized_text.jsonl',rows)
save('scene_labels.jsonl',labels)
save('ui_tables.jsonl',ui)
save('auxiliary_strings_review.jsonl',aux)
summary=dict(localized_entries=len(rows),unique_localized_english=len({r['english'] for r in rows}),localized_english_words=sum(len(re.findall(r"\b[\w'-]+\b",r['english'])) for r in rows),scene_label_entries=len(labels),ui_table_entries=len(ui),auxiliary_review_entries=len(aux),asset_read_errors=[r for e in inventory for r in e['records'] if 'error' in r],by_file=dict(collections.Counter(r['file'] for r in rows)))
(OUT/'extraction_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
