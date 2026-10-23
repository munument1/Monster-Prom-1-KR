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
| 테스트 번역 | 설정 메뉴 일부와 프롤로그 첫 5개 문장 |
| 한글 로고 | 시안 제작, 기본·축소 로고 3개 교체 |
| 적용·복원 | 로컬에서 해시 검증 완료 |
| 게임 화면 확인 | 사용자 확인 대기 |
| 전체 번역 / 배포용 패치 | 미완료 |

[상세 작업 기록](docs/STATUS.md) · [추출 집계](reports/extraction_summary.json) · [파일 검증 결과](reports/verification_report.json)

## 한글 로고 시안

![몬스터 프롬 한글 로고](artwork/logo/monster_prom_logo_ko_v1.png)

내장 이미지 생성 도구로 원본 로고를 참고해 제작했습니다. [사용 프롬프트와 적용 메모](artwork/logo/generation-notes.md)를 함께 보관합니다.

## 저장소 구성

- 원문 추출: `inspect_assets.py`, `extract_catalog.py`, `extract_managed_strings.py`
- Unity 직렬화 타입 보정: `unity_support.py`
- 폰트·텍스트 테스트 빌드: `build_test_patch.py`
- 한글 로고 테스트 적용: `apply_logo_patch.py`
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

로고는 폰트·텍스트 패치를 적용한 다음 `python .\apply_logo_patch.py`로 제작·적용합니다. 첫 적용에서 백업이 생성됩니다. 이후 로고만 복원하거나 재적용할 때는 아래 명령을 사용합니다.

```powershell
python .\manage_logo_patch.py restore
python .\manage_logo_patch.py apply
```

게임 언어를 **ENGLISH**로 두고 확인합니다. 한국어 항목을 새로 추가한 방식이 아니라 영어 슬롯 일부를 시험 번역한 상태입니다. 테스트 폰트는 영문 서체도 변경합니다.

실행 파일은 게임 설치 폴더의 `MonsterProm.exe`입니다. 실행과 화면 확인은 사용자가 진행합니다.

## 다음 작업

1. 한글 글리프·대사 줄바꿈·로고 표시 확인
2. 캐릭터 이름, 말투, 용어 및 변수·태그 보존 규칙 정리
3. JSONL 번역 재주입과 자동 검증 도구 구현
4. 본 번역, 이미지 UI 번역 및 배포 패키징

`korean` 필드를 채우는 것만으로 게임이 자동 갱신되지는 않습니다. 현재 적용 코드는 작은 테스트 문구 집합을 대상으로 합니다.
