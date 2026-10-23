from pathlib import Path
import UnityPy,io,json,hashlib,re,copy
from fontTools import subset
from fontTools.ttLib import TTFont
from unity_support import generator
BASE=Path(__file__).parent
from config import GAME_DATA
ROOT=GAME_DATA
OUT=BASE/'test_patch'/'MonsterProm_Data';OUT.mkdir(parents=True,exist_ok=True)
GEN=generator(ROOT)
translations={
 'MUSIC':'음악','SOUND EFFECTS':'효과음','VOICE:':'음성:',
 'LANGUAGE:':'언어:','WINDOW MODE:':'화면 모드:', 'DISPLAY:':'모니터:',
 'BLUR EFFECT:':'흐림 효과:', 'RESET PROGRESS':'진행 초기화',
 'FULLSCREEN':'전체 화면','WINDOWED':'창 모드',
 'RESTART THE GAME TO APPLY THE CHANGES!':'변경 사항을 적용하려면 게임을 다시 시작하세요!',
 'LOADING...':'불러오는 중...',
 'Ah... Spooky High School... the sweetest years of our lives.':'아... 스푸키 고등학교... 우리 인생에서 가장 달콤했던 시절.',
 'Back then we were young and unafraid...':'그때의 우리는 젊었고, 두려울 게 없었지...',
 'Sometimes reckless, sometimes brilliant, sometimes just stupid; but always willing to live life to the fullest.':'때로는 무모하고, 때로는 기발하고, 때로는 그냥 멍청했지만... 언제나 인생을 마음껏 즐기려 했어.',
 'We were on a wild journey to discover who we really were.':'우리는 진짜 자신을 찾아가는 거침없는 여정 한가운데 있었지.',
 'And we had yet to experience its ultimate challenge: the Monster Prom.':'그리고 아직 마지막 도전이 남아 있었어. 바로 몬스터 프롬.',
}
changes=[];manifest=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def change_dict(v,path,objid,filename):
 changed=False
 if isinstance(v,dict):
  if '_Keys' in v and '_Values' in v:
   for i,k in enumerate(v['_Keys'][:v.get('_Count',0)]):
    if k==0 and v['_Values'][i] in translations:
     old=v['_Values'][i];v['_Values'][i]=translations[old];changes.append(dict(file=filename,path_id=objid,field=path,english=old,korean=translations[old]));changed=True
  else:
   for k,x in v.items():
    if k=='mText' and x in translations:
     v[k]=translations[x];changes.append(dict(file=filename,path_id=objid,field=path+'/mText',english=x,korean=v[k]));changed=True
    elif isinstance(x,(dict,list)):changed=change_dict(x,path+'/'+k,objid,filename) or changed
 elif isinstance(v,list):
  for i,x in enumerate(v):changed=change_dict(x,path+'/'+str(i),objid,filename) or changed
 return changed
font_raw=None
for filename in ('resources.assets','level0','level1','level2','level3','level7'):
 print('Patch',filename,flush=True)
 env=UnityPy.load(str(ROOT/filename));env.typetree_generator=GEN
 reuse=filename=='resources.assets' and (OUT/filename).exists()
 original={o.path_id:o.get_raw_data() for o in env.objects};changed_ids=set();expected={}
 if filename=='resources.assets':
  font_obj=next(o for o in env.objects if o.path_id==3406)
  font=TTFont(io.BytesIO(bytes(font_obj.read_typetree()['m_FontData'])))
  options=subset.Options();options.name_IDs=['*'];options.name_legacy=True;options.name_languages=['*']
  sub=subset.Subsetter(options=options)
  sub.populate(unicodes=list(range(0x20,0x250))+list(range(0x1100,0x1200))+list(range(0x2000,0x2070))+list(range(0x3000,0x3100))+list(range(0x3130,0x3190))+list(range(0xac00,0xd7a4))+[0xfffd])
  sub.subset(font)
  for record in font['name'].names:
   if record.nameID in (1,2,3,4,6):
    value='Regular' if record.nameID==2 else 'MonsterPromKRTest'
    record.string=value.encode(record.getEncoding())
  font.recalcTimestamp=False
  buf=io.BytesIO();font.save(buf);font_raw=buf.getvalue()
  if reuse:
   staged=UnityPy.load(str(OUT/filename))
   font_raw=bytes(next(o for o in staged.objects if o.path_id==3393).read_typetree()['m_FontData'])
   font=TTFont(io.BytesIO(font_raw))
  cmap=font.getBestCmap();assert all(c in cmap for c in range(0xac00,0xd7a4))
  (OUT.parent/'test_font.ttf').write_bytes(font_raw)
 for obj in env.objects:
  if obj.type.name not in ('Font','TextAsset','MonoBehaviour'):continue
  t=obj.read_typetree();before=copy.deepcopy(t);changed=False
  if obj.type.name=='Font':
   t['m_FontData']=list(font_raw);t['m_FontNames']=['MonsterPromKRTest'];t['m_FallbackFonts']=[]
   size=t['m_FontSize'];t['m_LineSpacing']=size;t['m_Ascent']=size*0.859375;t['m_Descent']=-size*0.140625
   changed=True
   changes.append(dict(file=filename,path_id=obj.path_id,font=t['m_Name'],replacement='MonsterPromKRTest',hangul_syllables=11172))
  elif obj.type.name=='TextAsset':
   lines=t['m_Script'].splitlines(keepends=True);new=[]
   for line in lines:
    ending='\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
    cols=line.rstrip('\r\n').split('\t')
    if len(cols)>1 and cols[1] in translations:
     old=cols[1];cols[1]=translations[old];changed=True
     changes.append(dict(file=filename,path_id=obj.path_id,field=cols[0],english=old,korean=cols[1]))
    new.append('\t'.join(cols)+ending)
   t['m_Script']=''.join(new)
  else:changed=change_dict(t,'',obj.path_id,filename)
  if changed:
   # Confirm the generated schema preserves the original object byte-for-byte.
   if not reuse:
    obj.save_typetree(before)
    if obj.data!=original[obj.path_id]:raise RuntimeError(f'Roundtrip mismatch: {filename}:{obj.path_id}')
    obj.save_typetree(t)
   changed_ids.add(obj.path_id);expected[obj.path_id]=t
 if not changed_ids:continue
 dest=OUT/filename
 if not reuse:dest.write_bytes(env.file.save())
 check=UnityPy.load(str(dest));check.typetree_generator=GEN
 primary=list(check.objects)
 check.load_file(str(ROOT/'globalgamemanagers.assets'))
 assert len(primary)==len(original)
 for obj in primary:
  if obj.path_id in changed_ids:assert obj.read_typetree()==expected[obj.path_id],(filename,obj.path_id)
  else:assert obj.get_raw_data()==original[obj.path_id],(filename,obj.path_id)
 manifest.append(dict(file=filename,original_sha256=sha(ROOT/filename),patched_sha256=sha(dest),changed_objects=sorted(changed_ids),object_count=len(original)))
 print('Verified',filename,len(changed_ids),'objects',flush=True)
(OUT.parent/'manifest.json').write_text(json.dumps(dict(game_data=str(ROOT),files=manifest,changes=changes,font_source='Bundled game cjkFonts_allseto_v1.11, Korean/Latin subset; local test only',visual_verification='pending user'),ensure_ascii=False,indent=2),encoding='utf-8')
print('DONE',len(changes),'changes',flush=True)
