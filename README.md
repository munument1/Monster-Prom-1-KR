# Monster Prom 1 KR

몬스터 프롬 1편 한글화 작업 저장소입니다. 원문 추출과 한글 폰트·일부 텍스트·로고 테스트 패치 제작 및 로컬 적용까지 진행했습니다. **전체 번역과 실제 게임 화면 검증은 아직 완료되지 않았습니다.**

## 작업 현황 · 2026-10-23

| 작업 | 상태 |
| --- | --- |
| Unity 에셋·씬 구조 분석 | 완료 · Unity 2017.4.40f1 |
| 언어 사전 원문 추출 | 34,208개 · 중복 제외 30,822개 |
| UI 표 / 씬 라벨 추출 | 686개 / 818개 · 상호 중복 포함 |
| 코드 문자열 추출 | 검토 대상 4,509개 · 로그와 내부 식별자 포함 |
| 한글 폰트 테스트 | 내장 폰트의 한글 11,172자 확인 및 테스트 패치 제작 |
| 번역 데이터 | 영어 문구 324개 · 공통 UI, 모드 도구, 본편·Second Term 프롤로그 |
| 폰트 수정 v2 | 영문 NGUI 비트맵 폰트 8개를 한글 동적 폰트에 연결 · 화면 재확인 필요 |
| 한글 이미지 | 기본·축소 로고 + Second Term 로고 + 메인 메뉴 버튼 6개 |
| 적용·복원 | 로컬에서 해시 검증 완료 |
| 게임 화면 확인 | 사용자 확인 대기 |
| 전체 번역 / 배포용 패치 | 미완료 |

[상세 작업 기록](docs/STATUS.md) · [추출 집계](reports/extraction_summary.json) · [파일 검증 결과](reports/verification_report.json)

**v1에서 한글 폰트가 나오지 않는다는 사용자 확인을 받았습니다.** v2에서는 영어 UI가 사용하는 NGUI 폰트 연결을 수정했습니다. 첨부 화면의 영어 로고는 미교체 상태였던 Second Term 전용 이미지로 확인해 추가 교체했습니다. 수정 후 화면 검증은 아직 대기 중입니다.

제공받은 태국어 모드 v1.0.0-R17의 중국어 슬롯·동적 폰트·이미지 번들 구조를 참고했습니다. 모드 파일이나 번역문을 한국어 패치에 덮어쓰지는 않았습니다. [구조 분석 메모](docs/THAI_REFERENCE.md)

## 한글 로고 시안

![몬스터 프롬 한글 로고](artwork/logo/monster_prom_logo_ko_v1.png)

내장 이미지 생성 도구로 원본 로고를 참고해 제작했습니다. [사용 프롬프트와 적용 메모](artwork/logo/generation-notes.md)를 함께 보관합니다.

## 저장소 구성

- 원문 추출: `inspect_assets.py`, `extract_catalog.py`, `extract_managed_strings.py`
- Unity 직렬화 타입 보정: `unity_support.py`
- 폰트·텍스트 테스트 빌드: `build_test_patch.py`
- 한글 로고 테스트 적용: `apply_logo_patch.py`
- Second Term·메뉴 이미지와 NGUI 폰트 연결 수정: `apply_ui_font_v2.py`
- 번역 데이터와 주입: `translations/`, `apply_translation_batch.py`
- 적용·복원: `manage_test_patch.py`, `manage_logo_patch.py`, PowerShell 실행 스크립트
- 환경 설정: `config.py`, `requirements.txt`

게임 원본, 설치 백업, 추출한 원문 전체, 디컴파일 코드, 추출 폰트와 패치 바이너리는 포함하지 않습니다. JSONL 번역 카탈로그는 사용자의 게임 설치본에서 로컬로 생성합니다. 이 저장소는 완성된 한글 패치 배포본이 아닙니다.

## 로컬 재현

Windows와 Python 환경, 본인이 설치한 Monster Prom 1편이 필요합니다. 현재 개발 환경은 Python 3.14입니다.

```powershell
python -m pip install -r requirements.txt
$env:MPKR_GAME_DIR = 'C:\Games\Steam\steamapps\common\Monster Prom'
python .\inspect_assets.py
python .\extract_catalog.py
python .\extract_managed_strings.py
python .\build_test_patch.py
```

설치 위치가 다르면 `MPKR_GAME_DIR`를 변경하세요. **추출과 빌드는 원본 상태의 게임을 입력으로 사용합니다.** 이미 테스트 패치가 적용됐다면 먼저 게임을 종료하고 `python .\manage_test_patch.py restore`로 복원하세요. 기존 산출물을 유지하려면 별도 작업 폴더에서 진행하세요.

폰트·텍스트 패치 적용과 복원:

```powershell
python .\manage_test_patch.py apply
python .\manage_test_patch.py status
python .\manage_test_patch.py restore
```

새 작업 폴더에서는 폰트·텍스트 패치를 적용한 뒤 아래 순서로 이미지·폰트 수정과 번역 데이터를 적용합니다. 각 단계는 적용 직전 상태를 별도로 백업하며, 같은 백업이 있으면 덮어쓰지 않고 중단합니다.

```powershell
python .\apply_logo_patch.py
python .\apply_ui_font_v2.py
python .\apply_translation_batch.py --batch translation_batch01
```

이미 v2와 번역 묶음이 적용된 로컬 작업 폴더에서는 다시 실행할 필요가 없습니다. 번역 파일을 추가한 뒤에는 새로운 `--batch translation_batch03`처럼 미사용 번호를 지정할 수 있습니다. 전체 복원은 `manage_test_patch.py restore`를 사용합니다. 과거 `manage_logo_patch.py`는 v1 상태만 지원하므로 v2 이후에는 사용하지 마세요.

게임 언어를 **ENGLISH**로 두고 확인합니다. 한국어 항목을 새로 추가한 방식이 아니라 영어 슬롯의 일부를 번역한 상태입니다. 테스트 폰트는 영문 서체도 변경합니다.

실행 파일은 게임 설치 폴더의 `MonsterProm.exe`입니다. 실행과 화면 확인은 사용자가 진행합니다.

## 다음 작업

1. 한글 글리프·대사 줄바꿈·로고 표시 확인
2. 캐릭터 이름, 말투, 용어 및 변수·태그 보존 규칙 정리
3. 미번역 본문·선택지·퀴즈 번역 및 변수·태그 검증 확대
4. 본 번역, 이미지 UI 번역 및 배포 패키징

`translations/*_ko.json`의 영어 원문과 한국어 번역을 `apply_translation_batch.py`가 원본 추출 ID에 연결해 주입합니다. `%WEEKS%`, 숫자 치환자와 주요 서식 태그 보존을 검사합니다. 현재 전체 본문 번역은 완료되지 않았으며, 이미지에 박힌 모든 문구를 교체한 것도 아닙니다.
