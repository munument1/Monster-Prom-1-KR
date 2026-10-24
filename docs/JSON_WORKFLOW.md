# JSON 번역 작업

원문은 이미 `extracted/dialogue_and_localized_text.jsonl`에 추출되어 있습니다. 2026-10-24부터 중복 문구를 한 번만 번역하는 편집용 JSON 묶음을 추가했습니다. 전체 추출 원문과 작업용 JSON은 로컬에 보관하며 Git에는 번역 결과와 수량 보고서만 올립니다.

```powershell
python translation_batches.py prepare --first-event 261 --last-event 976 --words 9000
```

이번 준비 결과는 `extracted/work_json_261_976/`의 43개 묶음, 미번역 고유 원문 24,833개입니다. 준비 시점의 수량이며 이후 완료 여부는 `reports/translation_queue.json`의 완료 목록으로 확인합니다. 각 항목에는 영어, 한국어 빈칸, 원본 ID, 이벤트, 화자, 선택지 여부가 있습니다. 같은 원문이 먼 이벤트에서도 쓰이면 해당 위치를 함께 묶으므로 묶음의 마지막 이벤트 번호가 연속 진행률을 뜻하지 않습니다.

작업자는 `korean`만 채우고 나머지 필드는 유지합니다. 기존 번역과 같은 영어는 기존 한국어를 그대로 사용합니다.

```powershell
python translation_batches.py import extracted/work_json_261_976/story_261_976_001.json
python validate_translation_catalog.py
```

가져오기는 추출본 해시, 원문 ID, 빈 번역, 기존 번역 충돌을 검사하고 기존 결과 파일 덮어쓰기를 거부합니다. 변수·서식·개행·능력치 검사와 문법 생략 예외 통합은 공통 검증기에서 수행합니다. 검증 후에만 게임에 적용합니다.

중복 제거, 완료 문구 제외, 빈칸 거부, 원문 ID 불일치 거부, 덮어쓰기 방지와 정상 가져오기를 임시 자료로 확인했습니다. 퍼센트 수치와 실제 변수 토큰을 구분하며 아포스트로피가 들어간 동사 변수도 보존합니다.

JSON은 추출·분배·병합 시간을 줄입니다. 문맥과 말장난을 읽고 옮기는 작업, 이미지 생성과 검토는 별도로 필요합니다.

작업은 세 번역 에이전트가 서로 다른 묶음을 맡아 이어갑니다. 적용된 완료 목록은 `reports/translation_queue.json`, 실제 설치 진도는 `reports/progress.json`에서 확인합니다. 결과 JSON은 임시 파일에 쓴 뒤 원자적으로 교체합니다.

주입을 마치면 `translation_snapshot.py`가 실제 검사·적용한 사전을 `test_patch/installed_translations.json`과 해당 배치 폴더에 고정합니다. 설치 재조회와 기본 진도 집계는 이 목록을 사용합니다. 번역 에이전트가 다음 파일을 저장하는 동안에도 검증 대상이 달라지지 않습니다. 아직 적용하지 않은 완료 JSON까지 보고 싶으면 `python report_progress.py --include-ready`를 사용합니다. 별도 `reports/progress_ready.json`에 기록합니다.

2026-10-24 재개 중 새 JSON이 주입 직후 도착해 최신 사전과 설치 상태의 검증 범위가 어긋난 사례가 있었습니다. 설치 목록을 고정한 후 배치 11·12·13의 재조회가 통과했으며, 임시 자료로 새 파일 추가가 기존 설치 목록을 바꾸지 않는 것도 확인했습니다.
