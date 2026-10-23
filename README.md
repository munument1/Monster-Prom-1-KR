# Monster Prom 1 KR

몬스터 프롬 1편 한글화 작업 저장소입니다. 원문 추출과 한글 폰트·일부 텍스트·이미지 패치 제작 및 로컬 적용까지 진행했습니다. **전체 번역은 미완료이며, v2 한글 출력은 사용자 화면으로 확인했습니다. 최신 변경의 화면 재확인은 대기 중입니다.**

## 작업 현황 · 2026-10-23

| 작업 | 상태 |
| --- | --- |
| Unity 에셋·씬 구조 분석 | 완료 · Unity 2017.4.40f1 |
| 언어 사전 원문 추출 | 34,208개 · 중복 제외 30,822개 |
| UI 표 / 씬 라벨 추출 | 686개 / 818개 · 상호 중복 포함 |
| 코드 문자열 추출 | 검토 대상 4,509개 · 로그와 내부 식별자 포함 |
| 한글 폰트 테스트 | 내장 폰트의 한글 11,172자 확인 및 테스트 패치 제작 |
| 번역 데이터 | 영어 문구 1,167개 · 언어 사전 1,687개 위치에 대응 |
| 퀴즈 | 42문항·선택지 201개 및 도입부 번역 |
| 상점 | 아이템 이름·설명·상인 대사 110개 위치 번역 |
| 공통 장소 / 이벤트 | 초반 이벤트 1~145번 연결 확인 · 반복 장소 이벤트와 클럽 선택지·네 갈래 결과 |
| 폰트 수정 v2 | NGUI 비트맵 폰트 8개를 한글 동적 폰트에 연결 · 사용자 출력 확인 |
| 한글 이미지 | 로고, 메인 메뉴 6개, 학기 선택판 2개, 인원 1~4명, 뒤로·신규 표시, 학교 장소 표지 13개 |
| 줄바꿈 v3 | 음성 설정 창 문구 축약·명시적 개행·글자 크기 조정 |
| 적용·복원 | 로컬에서 해시 검증 완료 |
| 게임 화면 확인 | v2 출력 확인 · 최신 이미지·번역·개행 재확인 대기 |
| 전체 번역 / 배포용 패치 | 미완료 |

[상세 작업 기록](docs/STATUS.md) · [추출 집계](reports/extraction_summary.json) · [파일 검증 결과](reports/verification_report.json)

v1에서 한글 폰트가 나오지 않는다는 피드백을 받아 v2에서 영어 UI의 NGUI 폰트 연결을 수정했고, **사용자가 한글 출력을 확인했습니다.** 이후 음성 설정 창에서 단어 중간이 갈라지는 화면을 받아 문구와 줄바꿈 위치·글자 크기를 추가 조정했습니다. 모든 화면의 자동 줄바꿈을 일괄 변경한 것은 아닙니다.

[최신 번역 진도](reports/progress.json) · [음성 설정 창 글자 폭 검사](reports/voice_popup_layout.json)

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
- 선택 화면 이미지·음성 창 조정: `apply_layout_images_v3.py`
- 지정 영역 이미지 교체: `apply_atlas_regions.py`, `artwork/ui/atlas_patches_v4.json`, `artwork/ui/atlas_patches_v5.json`
- 설치 후 번역·게임 진행 데이터 검증: `verify_translation_state.py`
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
python .\apply_layout_images_v3.py
python .\apply_atlas_regions.py artwork/ui/atlas_patches_v4.json
python .\apply_atlas_regions.py artwork/ui/atlas_patches_v5.json
```

이미 해당 수정이 적용된 로컬 작업 폴더에서는 다시 실행할 필요가 없습니다. 번역 파일을 추가한 뒤에는 새로운 `--batch translation_batch07`처럼 미사용 번호를 지정할 수 있습니다. 전체 복원은 `manage_test_patch.py restore`를 사용합니다. 과거 `manage_logo_patch.py`는 v1 상태만 지원하므로 v2 이후에는 사용하지 마세요.

게임 언어를 **ENGLISH**로 두고 확인합니다. 한국어 항목을 새로 추가한 방식이 아니라 영어 슬롯의 일부를 번역한 상태입니다. 테스트 폰트는 영문 서체도 변경합니다.

실행 파일은 게임 설치 폴더의 `MonsterProm.exe`입니다. 실행과 화면 확인은 사용자가 진행합니다.

## 다음 작업

1. 새 번역·선택 화면 이미지·음성 설정 창 줄바꿈 확인
2. 캐릭터 이름, 말투, 용어 및 변수·태그 보존 규칙 정리
3. 미번역 본문·선택지·퀴즈 번역 및 변수·태그 검증 확대
4. 본 번역, 이미지 UI 번역 및 배포 패키징

`translations/*_ko.json`의 영어 원문과 한국어 번역을 `apply_translation_batch.py`가 원본 추출 ID에 연결해 주입합니다. `%WEEKS%`, 숫자 치환자와 주요 서식 태그 보존을 검사하고, 레이아웃을 위한 추가 개행은 허용합니다. 현재 언어 사전 기준 34,208개 위치 중 1,687개에 번역이 있으며 32,521개는 남아 있습니다. UI 표·씬 라벨은 중복이 많으므로 이 진도에 합산하지 않습니다. 전체 본문 번역과 이미지 전체 교체는 아직 완료되지 않았습니다.

이벤트 139~145번은 선택지와 성공·실패 결과를 포함해 305개 위치를 추가 번역했습니다. 영어 대명사·계사는 세 원문에 한해 `translations/grammar_adaptations.json`에 명시하여 한국어 표현으로 대체합니다. 이름·게임 변수와 서식 태그 검증은 유지합니다. 학교 표지는 도서관 5색, 화장실 5색, 체육관 2색, 야외 파랑만 적용했으며 다른 장소·색상과 시간 표시는 남아 있습니다.
