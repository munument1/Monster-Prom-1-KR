"""Windows patch installer. No game executable is launched or modified."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,threading
import bsdiff4

def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()

def package_dir():
 return Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]/'release_build/package'

def run(action,game,package,log=lambda message:None):
 game=Path(game).resolve();package=Path(package).resolve()
 manifest=json.loads((package/'patch_manifest.json').read_text(encoding='utf-8'))
 if manifest.get('format')!=1:raise RuntimeError('지원하지 않는 패치 형식입니다.')
 rows=manifest['files'];names=[r['file'] for r in rows]
 if not rows or len(names)!=len(set(names)) or any(Path(n).name!=n or '/' in n or '\\' in n for n in names):raise RuntimeError('패치 목록이 손상되었습니다.')
 if not (game/'MonsterProm.exe').is_file() or not (game/'MonsterProm_Data').is_dir():raise RuntimeError('MonsterProm.exe와 MonsterProm_Data가 있는 게임 폴더를 선택하세요.')
 if os.name=='nt':
  processes=subprocess.run(['tasklist','/FI','IMAGENAME eq MonsterProm.exe','/FO','CSV','/NH'],capture_output=True,creationflags=0x08000000).stdout
  if b'monsterprom.exe' in processes.lower():raise RuntimeError('몬스터 프롬을 종료한 뒤 다시 시도하세요.')
 data=game/'MonsterProm_Data';backup=game/'_MonsterPromKR_Backup';current={};changes=[]
 for row in rows:
  name=row['file'];target=data/name
  if not target.is_file():raise RuntimeError('게임 파일을 찾을 수 없습니다: '+name)
  digest=sha(target);current[name]=digest
  if digest not in (row['original_sha256'],row['patched_sha256']):raise RuntimeError('지원 대상과 다른 파일입니다: '+name+'\n다른 모드 또는 다른 게임 버전인지 확인하세요. 파일은 변경하지 않았습니다.')
  saved=backup/name
  if saved.exists() and sha(saved)!=row['original_sha256']:raise RuntimeError('원본 백업이 손상되었거나 다른 버전입니다: '+name)
  if digest==row['patched_sha256'] and action!='verify' and not saved.is_file():raise RuntimeError('복원에 필요한 원본 백업이 없습니다: '+name+'\nSteam 파일 무결성 검사로 원본을 복구한 뒤 설치하세요.')
  if action=='install':
   delta=(package/row['delta']).resolve()
   if not delta.is_relative_to(package) or not delta.is_file() or sha(delta)!=row['delta_sha256']:raise RuntimeError('패치 데이터가 손상되었습니다: '+name+'\nZIP을 다시 내려받아 압축을 풀어 주세요.')
  wanted=row['original_sha256'] if action=='restore' else row['patched_sha256']
  if digest!=wanted:changes.append(row)
  log('검사 완료: '+name)
 state='한글 패치 적용' if all(current[r['file']]==r['patched_sha256'] for r in rows) else '원본' if all(current[r['file']]==r['original_sha256'] for r in rows) else '일부 파일에 패치 적용'
 if action=='verify':return {'action':action,'version':manifest['version'],'state':state,'files_checked':len(rows)}
 if not changes:return {'action':action,'version':manifest['version'],'state':state,'changed_files':0}
 required=sum((r['patched_size'] if action=='install' else r['original_size'])+(r['original_size'] if action=='install' else r['patched_size']) for r in changes)+128*1024*1024
 if shutil.disk_usage(game).free<required:raise RuntimeError('작업 공간이 부족합니다. 게임 드라이브에 약 '+str(round(required/1024**3,1))+'GB 이상의 여유 공간을 확보하세요.')
 stage=Path(tempfile.mkdtemp(prefix='.mpkr-stage-',dir=game));replaced=[]
 try:
  backup.mkdir(exist_ok=True)
  for row in changes:
   name=row['file'];target=data/name;saved=backup/name;out=stage/name
   if action=='install':
    if not saved.exists():shutil.copy2(target,saved)
    if sha(saved)!=row['original_sha256']:raise RuntimeError('원본 백업 검증 실패: '+name)
    log('패치 생성: '+name);out.write_bytes(bsdiff4.patch(saved.read_bytes(),(package/row['delta']).read_bytes()))
   else:
    log('원본 준비: '+name);shutil.copy2(saved,out)
   wanted=row['patched_sha256'] if action=='install' else row['original_sha256']
   if sha(out)!=wanted:raise RuntimeError('결과 파일 검증 실패: '+name)
   # Keep the exact pre-operation file for rollback until all replacements finish.
   rollback=stage/(name+'.rollback');shutil.copy2(target,rollback)
   if sha(rollback)!=current[name]:raise RuntimeError('롤백 파일 검증 실패: '+name)
  # Recheck all live files before replacing the first target.
  for row in rows:
   if sha(data/row['file'])!=current[row['file']]:raise RuntimeError('작업 도중 게임 파일이 변경되었습니다. 게임과 다른 모드 도구를 종료하세요.')
  (backup/'patch_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
  for row in changes:
   name=row['file'];log('파일 적용: '+name);os.replace(stage/name,data/name);replaced.append(name)
  for row in rows:
   wanted=row['patched_sha256'] if action=='install' else row['original_sha256']
   if sha(data/row['file'])!=wanted:raise RuntimeError('설치 후 검증 실패: '+row['file'])
  (backup/'installed.json').write_text(json.dumps({'version':manifest['version'],'state':action},indent=2),encoding='utf-8')
  return {'action':action,'version':manifest['version'],'state':'한글 패치 적용' if action=='install' else '원본','changed_files':len(changes),'all_hashes_verified':True}
 except BaseException:
  rollback_failed=[]
  for name in reversed(replaced):
   try:shutil.copy2(stage/(name+'.rollback'),data/name)
   except OSError:rollback_failed.append(name)
  if rollback_failed:raise RuntimeError('자동 되돌리기에 실패했습니다. 작업 폴더를 보존했습니다: '+str(stage)+'\n대상: '+', '.join(rollback_failed))
  raise
 finally:
  # Never remove a folder unless it is the exact temporary child we created.
  if not any((stage/(n+'.rollback')).exists() and sha(data/n)!=current[n] for n in replaced):
   assert stage.parent==game and stage.name.startswith('.mpkr-stage-');shutil.rmtree(stage)

def find_game():
 candidates=[Path(r'C:\Games\Steam\steamapps\common\Monster Prom'),Path(r'C:\Program Files (x86)\Steam\steamapps\common\Monster Prom')]
 try:
  import winreg,re
  with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Valve\Steam') as key:steam=Path(winreg.QueryValueEx(key,'SteamPath')[0])
  roots=[steam];vdf=steam/'steamapps/libraryfolders.vdf'
  if vdf.exists():roots += [Path(p.replace('\\\\','\\')) for p in re.findall(r'"path"\s+"([^"]+)"',vdf.read_text(encoding='utf-8'))]
  candidates += [p/'steamapps/common/Monster Prom' for p in roots]
 except (OSError,ImportError):pass
 return next((str(p) for p in candidates if (p/'MonsterProm.exe').exists()),'')

def gui(package):
 import tkinter as tk
 from tkinter import filedialog,messagebox,ttk
 window=tk.Tk();window.title('몬스터 프롬 1 한국어 패치');window.geometry('650x440');window.minsize(580,400);path=tk.StringVar(value=find_game());busy=False
 ttk.Label(window,text='몬스터 프롬 1 한국어 패치',font=('Malgun Gothic',17,'bold')).pack(pady=(16,5))
 ttk.Label(window,text='게임을 종료하고 설치하세요. 게임 언어는 ENGLISH를 선택합니다.').pack()
 row=ttk.Frame(window);row.pack(fill='x',padx=18,pady=15);entry=ttk.Entry(row,textvariable=path);entry.pack(side='left',fill='x',expand=True)
 def browse():
  selected=filedialog.askdirectory(title='MonsterProm.exe가 있는 게임 폴더 선택')
  if selected:path.set(selected)
 browse_button=ttk.Button(row,text='폴더 선택',command=browse);browse_button.pack(side='left',padx=(6,0))
 buttons=ttk.Frame(window);buttons.pack();progress=ttk.Progressbar(window,mode='indeterminate');progress.pack(fill='x',padx=18,pady=12);output=tk.Text(window,height=11,state='disabled',font=('Malgun Gothic',9));output.pack(fill='both',expand=True,padx=18,pady=(0,15))
 def log(message):
  def append():output.configure(state='normal');output.insert('end',message+'\n');output.see('end');output.configure(state='disabled')
  window.after(0,append)
 controls=[entry,browse_button]
 def start(action):
  nonlocal busy
  if busy:return
  busy=True
  for control in controls:control.configure(state='disabled')
  progress.start()
  def worker():
   try:result=run(action,path.get(),package,log);window.after(0,lambda:messagebox.showinfo('완료',result['state']+'\n검증을 마쳤습니다.'))
   except Exception as error:
    message=str(error);log(message);window.after(0,lambda:messagebox.showerror('작업 중단',message))
   finally:window.after(0,finish)
  threading.Thread(target=worker,daemon=False).start()
 def finish():
  nonlocal busy
  busy=False;progress.stop()
  for control in controls:control.configure(state='normal')
 for label,action in [('한글 패치 설치','install'),('원본으로 복원','restore'),('설치 상태 검사','verify')]:
  button=ttk.Button(buttons,text=label,command=lambda a=action:start(a));button.pack(side='left',padx=5);controls.append(button)
 def close():
  if busy:messagebox.showinfo('작업 중','파일 작업이 끝난 뒤 닫아 주세요.')
  else:window.destroy()
 window.protocol('WM_DELETE_WINDOW',close);window.mainloop()

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--action',choices=['install','restore','verify']);parser.add_argument('--game-dir');parser.add_argument('--package',default=str(package_dir()));parser.add_argument('--result');args=parser.parse_args()
 if args.action:
  try:
   if not args.game_dir:raise RuntimeError('--game-dir is required')
   result=run(args.action,args.game_dir,args.package);code=0
  except Exception as error:result={'error':str(error)};code=1
  if args.result:Path(args.result).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
  if sys.stdout:print(json.dumps(result,ensure_ascii=False))
  sys.exit(code)
 else:gui(Path(args.package))
