"""Read installed strings and compare them to the reviewed translation catalog."""
from pathlib import Path
import json,collections,copy
import UnityPy
from config import GAME_DATA
from unity_support import generator
from apply_translation_batch import pointer
from translation_snapshot import load_catalog
BASE=Path(__file__).parent
def main():
 tr,basis=load_catalog(BASE)
 rows=[json.loads(x) for x in (BASE/'extracted/dialogue_and_localized_text.jsonl').read_text(encoding='utf-8').splitlines()]
 groups=collections.defaultdict(list)
 for r in rows:
  if r['english'] in tr:groups[r['file']].append(r)
 gen=generator(GAME_DATA);verified=0
 for fn,items in groups.items():
  print('Verify strings',fn,flush=True)
  e=UnityPy.load(str(GAME_DATA/fn));e.typetree_generator=gen;objects={o.path_id:o for o in e.objects};trees={}
  for r in items:
   pid=r['path_id']
   if pid not in trees:trees[pid]=objects[pid].read_typetree()
   value=pointer(trees[pid],r['field']);i=next(i for i,k in enumerate(value['_Keys'][:value['_Count']]) if k==0)
   assert value['_Values'][i]==tr[r['english']],r['id'];verified+=1
 # Prove story progression and quiz outcomes were not changed by string injection.
 comparisons=[]
 for fn,pid in [('level6',2888),('level5',334)]:
  old=UnityPy.load(str(BASE/'backup/original'/fn));old.typetree_generator=gen;old.load_file(str(GAME_DATA/'globalgamemanagers.assets'))
  new=UnityPy.load(str(GAME_DATA/fn));new.typetree_generator=gen
  a=next(o for o in old.objects if o.path_id==pid and o.type.name=='MonoBehaviour').read_typetree()
  b=next(o for o in new.objects if o.path_id==pid and o.type.name=='MonoBehaviour').read_typetree()
  def strip_english(value):
   if isinstance(value,dict):
    if '_Keys' in value and '_Values' in value:
     for i,key in enumerate(value['_Keys'][:value.get('_Count',0)]):
      if key==0:value['_Values'][i]='<english-slot>'
    else:
     for child in value.values():strip_english(child)
   elif isinstance(value,list):
    for child in value:strip_english(child)
  strip_english(a);strip_english(b);assert a==b,(fn,pid)
  comparisons.append({'file':fn,'path_id':pid,'non_english_text_and_gameplay_fields':'unchanged'})
 report={'verified_localized_occurrences':verified,'catalog_basis':basis,'gameplay_comparisons':comparisons,'visual_verification':'v2 font output user-confirmed; new changes pending user'}
 (BASE/'reports/translation_state.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
