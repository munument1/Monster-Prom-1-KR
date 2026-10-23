"""Validate and inject reviewed Korean strings using the original extraction IDs."""
from pathlib import Path
import json,re,collections,hashlib,shutil,subprocess,argparse
import UnityPy
from config import GAME_DATA
from unity_support import generator
BASE=Path(__file__).parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def readrows(name):return [json.loads(l) for l in (BASE/'extracted'/name).read_text(encoding='utf-8').splitlines()]
def pointer(tree,path):
 for part in path.strip('/').split('/'):
  tree=tree[int(part)] if isinstance(tree,list) else tree[part]
 return tree
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--batch',default='translation_batch01');args=parser.parse_args()
 assert re.fullmatch(r'translation_batch[0-9]+',args.batch)
 if 'MonsterProm.exe' in subprocess.run(['tasklist','/FI','IMAGENAME eq MonsterProm.exe','/FO','CSV','/NH'],capture_output=True,text=True).stdout:raise SystemExit('Close Monster Prom first.')
 tr={}
 for p in sorted((BASE/'translations').glob('*_ko.json')):
  for en,ko in json.loads(p.read_text(encoding='utf-8')).items():
   if en in tr:assert tr[en]==ko,en
   tr[en]=ko
 token=re.compile(r'%[^%]+%|\[\d+\]|\[(?:/?[biusc]|n|[0-9a-fA-F]{6,8}|-)\]')
 for en,ko in tr.items():
  assert collections.Counter(x for x in token.findall(en) if x!='[n]')==collections.Counter(x for x in token.findall(ko) if x!='[n]'),en
  assert ko.count('[n]')+ko.count('\n')>=en.count('[n]')+en.count('\n'),en
 rows=readrows('dialogue_and_localized_text.jsonl');labels=readrows('scene_labels.jsonl');ui=readrows('ui_tables.jsonl')
 targets=collections.defaultdict(lambda:collections.defaultdict(list))
 for kind,items in [('dict',rows),('label',labels)]:
  for r in items:
   source=r['english'] if r['english'] in tr else r['english'].replace('\n','[n]')
   if source in tr:targets[r['file']][r['path_id']].append((kind,{**r,'english':source}))
 ui_lookup={(r['path_id'],r['key']):r for r in ui if r['english'] in tr}
 for pid,key in ui_lookup:targets['resources.assets'][pid]
 stage=BASE/'test_patch'/args.batch;backup=BASE/'backup'/('before_'+args.batch)
 if backup.exists():raise SystemExit('Batch backup already exists; refusing to overwrite.')
 stage.mkdir(parents=True,exist_ok=True);patch=BASE/'test_patch';m=json.loads((patch/'manifest.json').read_text(encoding='utf-8'))
 for item in m['files']:assert sha(GAME_DATA/item['file'])==item['patched_sha256'],item['file']
 gen=generator(GAME_DATA);records=[];occurrences=0
 for fn,ids in sorted(targets.items()):
  print('Translate',fn,flush=True)
  e=UnityPy.load(str(GAME_DATA/fn));e.typetree_generator=gen
  objects={o.path_id:o for o in e.objects};original={pid:o.get_raw_data() for pid,o in objects.items()};expected={};count=0
  for pid,items in ids.items():
   o=objects[pid];t=o.read_typetree()
   if o.type.name=='TextAsset':
    new=[]
    for line in t['m_Script'].splitlines(keepends=True):
     ending='\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
     cols=line.rstrip('\r\n').split('\t');r=ui_lookup.get((pid,cols[0]))
     if r and len(cols)>1:cols[1]=tr[r['english']];count+=1
     new.append('\t'.join(cols)+ending)
    t['m_Script']=''.join(new)
   else:
    for kind,r in items:
     ko=tr[r['english']]
     if kind=='label':
      assert r['field']=='/mText';t['mText']=ko.replace('[n]','\n')
     else:
      value=pointer(t,r['field']);index=next(i for i,k in enumerate(value['_Keys'][:value['_Count']]) if k==0);value['_Values'][index]=ko
     count+=1
   encoded=o.save_typetree(t)
   if encoded!=original[pid]:expected[pid]=encoded
  if not expected:continue
  dest=stage/fn;dest.write_bytes(e.file.save());check=UnityPy.load(str(dest));primary=list(check.objects);check.typetree_generator=gen;check.load_file(str(GAME_DATA/'globalgamemanagers.assets'))
  assert len(primary)==len(original)
  for o in primary:assert o.get_raw_data()==expected.get(o.path_id,original[o.path_id]),(fn,o.path_id)
  records.append({'file':fn,'before_sha256':sha(GAME_DATA/fn),'patched_sha256':sha(dest),'changed_objects':sorted(expected),'object_count':len(original),'translated_occurrences':count});occurrences+=count
 backup.mkdir(parents=True);shutil.copy2(patch/'manifest.json',backup/'manifest.json')
 for r in records:shutil.copy2(GAME_DATA/r['file'],backup/r['file'])
 for r in records:
  item=next((x for x in m['files'] if x['file']==r['file']),None)
  if item is None:
   original=BASE/'backup/original'/r['file'];assert not original.exists();shutil.copy2(GAME_DATA/r['file'],original)
   item={'file':r['file'],'original_sha256':r['before_sha256'],'changed_objects':[],'object_count':r['object_count']};m['files'].append(item)
  item['patched_sha256']=r['patched_sha256'];item['changed_objects']=sorted(set(item['changed_objects'])|set(r['changed_objects']))
  m['changes'].append({'file':r['file'],'feature':'Korean UI/prologue '+args.batch,'objects':r['changed_objects']})
  for dest in (GAME_DATA/r['file'],patch/'MonsterProm_Data'/r['file']):shutil.copy2(stage/r['file'],dest);assert sha(dest)==r['patched_sha256']
 (patch/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
 summary={'unique_translations':len(tr),'localized_dictionary_matches':sum(r['english'] in tr for r in rows),'prologue_matches':sum(r['file']=='level2' and r['english'] in tr for r in rows),'ui_table_matches':sum(r['english'] in tr for r in ui),'scene_label_matches':sum(r['english'] in tr or r['english'].replace('\n','[n]') in tr for r in labels),'changed_files':len(records),'translated_occurrences_in_changed_files':occurrences,'tag_variable_validation':'passed','visual_verification':'pending user'}
 (BASE/'reports'/(args.batch+'.json')).write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 (stage/'verification.json').write_text(json.dumps({'summary':summary,'files':records},ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
