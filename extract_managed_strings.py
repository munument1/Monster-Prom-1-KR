from pathlib import Path
import dnfile,json
from config import GAME_DATA
ROOT=GAME_DATA/'Managed'
OUT=Path(__file__).parent/'extracted'/'managed_strings_review.jsonl'
count=0
with OUT.open('w',encoding='utf-8',newline='\n') as f:
 for name in ('Assembly-CSharp.dll','Assembly-CSharp-firstpass.dll'):
  pe=dnfile.dnPE(str(ROOT/name));heap=pe.net.user_strings
  if heap is None:continue
  offset=1
  while offset<len(heap.__data__):
   item=heap.get(offset)
   if item is None or item.raw_size<1:break
   value=str(item)
   if value.strip():
    f.write(json.dumps(dict(id=f'{name}:0x{0x70000000|offset:08X}',source=value,korean='',review_note='Includes internal identifiers and logs; review before translating.'),ensure_ascii=False)+'\n');count+=1
   offset+=item.raw_size
print('Managed strings for review:',count)
