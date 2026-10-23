# 번역·검수 방식

## 병렬 작업

사용자 요청으로 2026-10-24부터 번역을 서브 에이전트 3명에게 겹치지 않는 이벤트 구간으로 나누어 맡깁니다. 주 에이전트는 이미지 작업과 합치기·교차 검수·게임 적용·업로드를 담당합니다. 작업자는 자기 구간의 번역 JSON과 문법 예외 JSON만 작성합니다. 게임 파일과 Git은 주 에이전트가 검증 후 변경합니다.

원본 추출 위치에 있는 모든 비어 있지 않은 영어 문구를 번역합니다. 선택지뿐 아니라 각 성공·실패 결과도 포함합니다. 같은 영어 키가 기존 사전에 있으면 기존 번역을 재사용하고, 서로 다른 구간에서 충돌하면 문맥을 검토해 하나로 통일합니다.

## 표현과 용어

JSON 작업 묶음의 준비·가져오기 방식은 [JSON 작업 안내](JSON_WORKFLOW.md)를 따릅니다. `story_` 번역 파일도 이벤트 파일과 같은 능력치 검사를 받습니다.

- SMARTS 지능 / BOLDNESS 대담함 / CREATIVITY 창의력 / CHARM 매력 / FUN 재미 / MONEY 돈
- Liam 리암 / Damien 데미안 / Scott 스콧 / Polly 폴리 / Polina 폴리나 / Miranda 미란다 / Vera 베라
- Interdimensional Prince 차원 왕자 / Coven 코번 / Univertica 유니버티카 / Rabbaroo 래버루
- Momentgram 모먼트그램 / Horny Dating App(tm) 발정난 데이팅 앱(tm) / CrowdSerfs 크라우드서프
- Slayer는 괴물 사냥꾼. 밴드명 Slayer는 슬레이어.
- Crazy Martin the Were-Bear Janitor는 곰인간 관리인 미치광이 마틴.

캐릭터별 말투와 원문의 욕설·말장난을 살립니다. 이름 치환자와 게임 변수, 서식 태그를 보존합니다. 능력치 결과는 `지능 +2, 재미 -1`처럼 부호와 수치를 명시합니다. 고유명사를 바꿀 때는 연결된 조사도 확인합니다.

영어 문법 대명사·활용동사는 성별 중립 한국어 지시어와 서술어로 자연화할 수 있습니다. 생략은 원문별 토큰과 정확한 개수를 `grammar_adaptations.json`에 명시한 경우에만 허용합니다. 작업자의 별도 예외 파일은 합친 뒤 중앙 파일로 검증합니다. 이름 변수는 이 예외에 포함하지 않습니다.

## 적용과 검증

1. `python validate_translation_catalog.py`: 중복 키 번역 일치, 변수·서식·개행, 영어 문법 예외, 새 이벤트의 능력치 부호·수치 검사.
2. 선택지·각 결과 마지막 문장과 의미가 의심되는 부분을 다른 작업자가 교차 검수. 자동 검사만으로 번역 정확성을 보장하지 않습니다.
3. `python apply_translation_batch.py --batch translation_batch09`처럼 미사용 번호로 적용. 최초 원본과 단계별 백업 유지.
4. `python verify_translation_state.py`: 설치 문자열 재조회 및 영어 문자열 외 이벤트·퀴즈 데이터 원본 비교.
5. `python report_progress.py --first-event 146 --last-event 215`처럼 완료한 구간으로 진도 재집계. 새 구간 작업에서는 인수를 갱신합니다.
6. 최신 패치를 복원·재적용해 전체 파일 해시 확인. 게임은 실행하지 않으며 화면 검증은 사용자가 담당합니다.

진도는 34,208개 언어 사전 위치를 분모로 합니다. 원문 중복과 공통 문구 재사용 때문에 이벤트 위치 수, 고유 번역 수, 설치 위치 증가량은 서로 다릅니다. 이벤트 수만으로 전체 번역률을 계산하지 않습니다.

동사 활용 토큰과 성별 표현 토큰은 최초 추출에서 실제 발견한 값만 `translations/grammar_verb_tokens.json`, `translations/grammar_gender_tokens.json`에 명시했습니다. 이 목록은 생략 자체를 자동 승인하지 않으며, 여전히 각 원문의 정확한 개수·자연화 이유를 별도 예외에 기록해야 합니다. 이름·COUNT·WEEKS 같은 값 변수는 생략 대상이 아닙니다.
