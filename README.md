# Monster Prom 1 KR

몬스터 프롬 1편의 비공식 한글화 작업 저장소입니다. 원문 추출, 한글 폰트 수정, 한국어 텍스트·이미지 제작과 로컬 게임 적용을 진행하고 있습니다. **v2 한글 출력은 사용자 화면으로 확인했으며, 최신 변경의 게임 화면 확인은 사용자 대기 중입니다.**

## 현재 진도 · 2026-10-24

| 항목 | 검증된 설치 상태 |
| --- | --- |
| 언어 사전 원문 | 34,208개 위치 · 중복 제외 30,822개 원문 |
| 번역 | 31,239개 고유 문구 · **34,208/34,208개 위치 (100.0%)** |
| 남은 사전 위치 | 0개 |
| 메인 이벤트 | **1~976번** 대사·선택지·모든 결과 연결 확인 |
| JSON 작업 | 43묶음 중 43묶음 설치·검증 |
| 한글 폰트 | 한글 11,172자 포함 · NGUI UIFont 8개 동적 폰트 연결 |
| 코드·게임 진행 데이터 | 메인 이벤트·퀴즈의 다른 언어와 게임 진행 필드 보존 확인 |
| 원본 백업 | 최초 원본 및 수정 단계별 로컬 백업 유지 |
| 배포 패키지 | 미완료 · 이 저장소는 완성 패치 배포본이 아닙니다 |

진도는 실제 게임에 적용한 번역 목록의 스냅샷을 기준으로 계산합니다. 작업자가 새 JSON을 저장해도 설치·검증 전에는 설치 진도에 합산하지 않습니다. UI 표와 씬 라벨은 중복이 많아 위 진도에 더하지 않습니다.

[최신 진도](reports/progress.json) · [번역 검사](reports/translation_catalog_validation.json) · [게임 파일 재조회](reports/translation_state.json) · [작업 묶음](reports/translation_queue.json)

## 이미지와 화면

로고·메뉴·학기·인원·학교 장소·능력치·상점·모드 도구에 이어 소품, 컨트롤러 안내, 회상 편지, 홍보, 도서관 포커/비트코인/크라우드펀딩/광고 메일, 엔딩 사진·문구, 학교·도시 배경 글씨를 한글화했습니다. 내장 이미지 생성 도구로 제작한 뒤 지정 영역만 원래 텍스처에 배치합니다. 생성 이미지와 적용 좌표·프롬프트를 함께 보관합니다. 추가로 검토한 잔여 후보 42개 중 커플 사진 캡션 32개와 갤러리·소품 9개, 총 41개를 적용했습니다. 장식용 네온 간판 1개는 사용자 요청으로 원문을 유지했습니다. 이번 재개 이후 추가한 이미지 텍스처는 중복 제외 96개입니다. 배경 간판·책/게임 제목·작가 서명 등 장식 문구는 원문을 유지합니다. [잔여 후보 검수 결과](reports/remaining_images_review.json)

제공받은 태국어 모드는 로컬에서 구조와 번역 대상만 참고합니다. 한국어 텍스트와 이미지는 영어 원본에서 제작하며 태국어 모드 파일을 덮어쓰지 않습니다. [참고 기록](docs/THAI_REFERENCE.md) · [이미지 제작 기록](artwork/ui/generation-notes.md) · [태국어 참고 대조](reports/thai_image_reference_audit.json)

음성 설정 창의 문구를 축약하고 명시적 개행과 글자 크기를 조정했습니다. 모든 화면의 자동 줄바꿈을 일괄 변경한 상태는 아닙니다. [폭 검사](reports/voice_popup_layout.json)

![한글 로고](artwork/logo/monster_prom_logo_ko_v1.png)

## 작업 구조

- 원본 추출: `inspect_assets.py`, `extract_catalog.py`, `extract_managed_strings.py`
- 중복 제거·문맥 포함 JSON 작업: `translation_batches.py` · [작업 안내](docs/JSON_WORKFLOW.md)
- 번역 사전: `translations/*_ko.json` · [용어·번역 지침](docs/TRANSLATION_GUIDE.md)
- 변수·서식·개행·능력치 검사: `validate_translation_catalog.py`
- 주입·설치 목록 고정: `apply_translation_batch.py`, `translation_snapshot.py`
- 설치 후 재조회·진도: `verify_translation_state.py`, `report_progress.py`
- 이미지 영역 교체·검증: `apply_atlas_regions.py`, `verify_image_regions.py`, `artwork/ui/*json`
- 백업·적용·복원: `manage_test_patch.py`, `patch_revision.py`

이름·게임 변수·숫자·서식 태그는 보존합니다. 한국어에 불필요한 영어 성별·동사 활용 태그의 생략은 `translations/grammar_adaptations.json`에 원문별 종류·개수·이유를 명시하고 검사합니다. 의미 검수 기록은 [별도 보고서](reports/translation_semantic_review.json)에 있으며 모든 문장의 독립 검수를 완료했다는 뜻은 아닙니다.

## 로컬 사용

본인 설치본과 Windows/Python이 필요합니다. 게임 원본, 전체 추출 원문, 태국어 모드, 추출 폰트, 백업, 패치 바이너리는 Git에 포함하지 않습니다. 이미 수정한 설치본에서 원문을 다시 추출하지 마세요. 초기 재현 순서는 [상세 기록](docs/STATUS.md)을 참고합니다.

기존 개발 폴더의 최종 패치 적용·상태·복원:

```powershell
python manage_test_patch.py apply
python manage_test_patch.py status
python manage_test_patch.py restore
```

새 번역은 문법 예외 통합과 사전 검사를 마친 뒤 **미사용** `--batch translation_batchNN` 번호로 적용합니다. 기존 백업을 덮어쓰지 않습니다.

```powershell
python validate_translation_catalog.py
python apply_translation_batch.py --batch translation_batchNN
python verify_translation_state.py
python report_progress.py
```

`report_progress.py --include-ready`는 아직 설치하지 않은 완료 JSON까지 포함한 별도 `reports/progress_ready.json`을 작성합니다.

게임 언어를 **ENGLISH**로 설정합니다. 한국어 번역은 영어 슬롯을 사용합니다. 실행 파일은 `C:\Games\Steam\steamapps\common\Monster Prom\MonsterProm.exe`이며, 실행과 화면 확인은 사용자가 진행합니다.
