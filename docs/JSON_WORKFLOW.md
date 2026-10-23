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
