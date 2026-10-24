# 추가 이미지 v2

## v3 / v4 추가 산출물

내장 image_gen으로 아래 이미지를 생성했습니다. 원본 아틀라스를 참조했으며, 적용할 때는 번역할 글자가 들어 있는 지정 영역만 리샘플하여 가져옵니다. 생성 과정에서 다른 부분에 생긴 차이는 게임에 적용하지 않습니다.

- `generated/expansion_boards_ko_v3.png`: 학기 선택판 2개
- `generated/players234_ko_v3.png`: 인원 2~4명
- `generated/player1_ko_v3.png`: 인원 1명
- `generated/back_button_ko_v4.png`: 뒤로 버튼
- `generated/new_badge_ko_v4.png`: 신규 표시

### 학기 선택판 프롬프트

Use case text-localization. Edit this packed game texture atlas, keep tall 1024x2048 layout and ALL exact placement. Change the red chalkboard title SECOND TERM to exactly "두 번째 학기", and its white (DLC) subtitle to exactly "(추가 콘텐츠)". Change the purple chalkboard title FIRST TERM to exactly "첫 번째 학기", and its white (CLASSIC) subtitle to exactly "(기본 게임)". Keep title red and purple respectively, white subtitles, chalky irregular hand lettering with fully readable Hangul. Absolutely preserve both chalkboards, both cartoon characters and accessories, transparent background and full composition. No rearranging, no English, no added background or new objects. It is a packed game texture asset.

### 2~4명 프롬프트

Use case text-localization. This is a 2048x2048 packed game texture atlas: preserve its exact square canvas, exact placement and size of every shape. Change only these three labels: 2PLAYERS to exactly "2명", 3PLAYERS to exactly "3명", 4PLAYERS to exactly "4명". Black hand-drawn lettering, each in the SAME caption area beneath its existing character group. Preserve all cartoon people, faces, controllers, snakes, colored shapes, paper panels, line and transparency unchanged. Do not move or redraw illustrations or add lettering to unlabelled duplicates. Do not rearrange the atlas. No English or watermark.

### 1명 프롬프트

Use case text-localization. Edit this exact 2048x2048 square packed game texture atlas. Change ONLY the bottom caption "1PLAYER" beneath the lower red cartoon person to exactly "1명" in black playful hand-drawn lettering on the existing ivory paper card. Preserve its exact original position and scale. Keep all colored rectangles and duplicate figures, blank regions, outlines and transparency unchanged. No redesign, rearranging, new shapes, extra text or watermark. It is a sprite atlas with strict fixed coordinates.

### 뒤로 버튼 프롬프트

Use case text-localization. Edit the supplied square packed game sprite atlas, preserving its exact 2048x2048 canvas and all fixed positions. Change ONLY the word BACK on the hot pink left-pointing arrow button at the upper left into exactly "뒤로", using ivory hand-drawn lettering matching the original. Do not translate controller keys A/B/X/Y or Esc. Keep every border, arrow, colored rectangle, paper, blank patch, icon, transparency and all other pixels unchanged as closely as possible. No rearrangement, no additions. The new Hangul must fit cleanly within the same pink arrow.

### 신규 표시 프롬프트

Use case text-localization. Edit the supplied landscape 2048x1024 packed game texture atlas. Change ONLY the small black word NEW on the ivory paper badge near x=990 y=820 to exactly "신규" in matching compact hand-drawn black Hangul. Preserve its exact location and badge dimensions. Keep ALL large blank paper panels, black patterned backgrounds, bars, borders and transparency as close to pixel-identical to the reference as possible. No layout changes, no new text, no redesign. The two Hangul glyphs must be fully inside the original tiny badge.

기본 내장 image_gen 도구의 text-localization 방식으로 생성했습니다. 원본은 게임 설치본에서 로컬로 추출해 참조했으며 원본 파일은 Git에서 제외합니다.

- Second Term: `../logo/monster_prom_second_term_ko_v2.png`
- 메인 메뉴 생성 아틀라스: `generated/main_menu_ko_v2.png`
- 실제 적용 시 원본 텍스처 크기에 맞춰 리샘플하고 대상 버튼 영역만 교체합니다. 레이아웃과 스프라이트 영역은 게임 원본 기준입니다.

## 학교 장소 표지 v5 · 내장 image_gen

생성 원본: `generated/school_locations_ko_v5.png`. 적용용: `generated/school_locations_packed_ko_v5.png`. 생성 결과에서 화살표 13개를 잘라 원래 스프라이트 크기로 리샘플하고, `atlas_patches_v5.json`의 위치에 배치했습니다. 도서관 5색, 화장실 5색, 체육관 2색, 야외 파랑입니다. 해당 영역 밖의 픽셀과 다른 오브젝트는 보존했습니다. 생성 결과의 주차 카드는 이번 적용에서 제외했습니다. 나머지 색상·장소와 시간 표시는 미완료입니다. 원본의 타이트 메시가 유지되므로 게임 내 테두리와 글자 가장자리는 사용자 확인 대기입니다.

Use case: text-localization. Edit target: the supplied square 2048x2048 packed Monster Prom game sprite atlas. Preserve the EXACT layout, sizes, colors, arrow shapes, ivory borders, dark geometric backgrounds, blank panels and transparency. Change ONLY lettering in its existing location. All five LIBRARY arrows at the top must say exactly "도서관". All five BATHROOMS arrows (four across the second row and one red near bottom right) must say exactly "화장실". The blue OUTDOORS arrow near bottom right must say exactly "야외". Both GYM arrows at the bottom right must say exactly "체육관". The large Week card at bottom left must say exactly "주차", retaining its underline. Match original ivory irregular hand-drawn lettering, legible complete Hangul, fitting each original arrow. Do not move or redesign any sprite. Keep blank paper and panels unchanged. True transparent background, no extra words, no English.

## Second Term 프롬프트 (기존)

Use case text-localization. Edit this exact Monster Prom Second Term expansion logo. Keep its original gray shield, gray clasped skeletal hands, black outlines, purple ribbon with ivory border, flat angular comic artwork and full composition. Replace MONSTER with exactly "몬스터" in bold black angular Hangul, PROM with exactly "프롬" in hot pink angular Hangul. Replace the ribbon SECOND TERM with Korean "두 번째 학기": put exactly "두 번째" on the left ribbon and exactly "학기" on the right ribbon. All Korean must be clearly spelled and legible. Keep the logo square 1024x1024 with matching placement and safe transparent padding. The purple ribbon must have clean fully transparent outer background, no white or beige rectangular blocks. Preserve the ivory ribbon edging only. No English letters, extra ornaments, backdrop, or watermark. This is a localized game texture, not a mockup.

## 메인 메뉴 프롬프트

Use case text-localization. Edit the supplied game menu texture ATLAS. Output landscape 2048x1024 exactly with the SAME pixel placement, size, silhouettes and spacing of ALL arrow-shaped buttons and small decorations. It is a packed sprite atlas, not a newly arranged sheet: DO NOT move, scale, rotate or redesign any element. Change ONLY the lettering: SETTINGS -> "설정"; MODTOOL -> "모드 도구"; QUIT -> "종료"; PLAY -> "시작"; GALLERY -> "갤러리"; ONLINE -> "온라인". Match the original ivory hand-drawn narrow irregular lettering but with complete readable Hangul. Keep arrow plates black or hot pink exactly as reference, ivory thin borders, subtle geometric shading and original orientations. Keep every blank patch and small decoration exactly in its original location. True transparent background. No English letters or added captions. All lettering must remain strictly inside its original arrow button bounds.

## 학교·상점 v6·v7 최종 적용

내장 image_gen으로 생성했습니다. 최종 생성 파일과 정확한 프롬프트:

- `generated/school_cards_rgb_ko_v6.png` · [카드·표지 프롬프트](school_cards_rgb_ko_v6_prompt.md)
- `generated/school_stats_rgb_ko_v6.png` · [능력치·표지·카드 프롬프트](school_stats_rgb_ko_v6_prompt.md)
- `generated/school_buttons_ko_v6.png` · [선택 버튼 프롬프트](school_buttons_ko_v6_prompt.md)
- `generated/shop_labels_rgb_ko_v7.png` · [상점 프롬프트](shop_labels_rgb_ko_v7_prompt.md)

`atlas_patches_v6.json`과 `atlas_patches_v7.json`에 생성 이미지의 잘라낼 좌표와 게임의 배치 좌표를 기록했습니다. 카드·표지는 스프라이트 크기로 리샘플하고 능력치 문구는 원래 각 줄에 맞춥니다. RGB 중간 이미지를 사용해 투명 경계의 색 번짐을 피하고 최종 아틀라스에는 원래 알파를 유지합니다. 주차 대형 카드와 상점 검정 소지금 문구는 글자·밑줄 영역만 적용합니다. 밝은 나가기 버튼은 실제 이미지 문구 위치를 사용합니다. 원본 아틀라스와 적용 바이너리는 로컬에만 보관합니다. 게임 화면 확인은 사용자 대기입니다.


## v8・v9 추가 이미지

모드 도구 로고·버튼 3종과 이벤트 소품 8종을 내장 image_gen으로 생성했습니다. 정확한 프롬프트는 `modtool_buttons_v8_prompt.md`, `modtool_logo_v8_prompt.md`, `items_a_v9_prompt.md`, `items_b_v9_prompt.md`에 있습니다. 생성 원본은 `generated/`, 재현 좌표는 `modtool_v8.json`과 `items_v9.json`에 보관했습니다. RGB 검정 배경 중간 이미지를 잘라 원래 크기로 맞추고 최초 게임 텍스처의 알파 채널을 복원했습니다. 소품은 태국어 모드의 번역 대상과 대응 영어 원본을 대조해 선정했습니다. 게임 화면 확인은 사용자 대기입니다.


## v10~v12 추가 이미지

최종 컨트롤러 안내는 `controller_labels_ko_v10b_prompt.md`와 `generated/controller_labels_ko_v10b.png`, `controllers_v10c.json`을 사용합니다. 최초 합성 시 주변 컨트롤러 조각과 잘린 글자가 보여 독립 글자만 다시 생성했습니다. 기존 캡션 사각형을 지우고 새 알파 글자를 배치했으며 그 밖의 픽셀은 원본과 같습니다. 중간 실험 산출물은 로컬 참고 폴더에 보관합니다.

회상 주차 표시는 `weeks_ko_v11_prompt.md`, 편지는 `ending_letter_ko_v11_prompt.md`, 적용 좌표는 `story_images_v11.json`에 있습니다. 홍보 배너 3종과 안내 그림 2종은 `promos_ko_v12_prompt.md` 및 `promos_v12.json`을 사용합니다. 외곽은 최초 원본 알파를 유지하고 다른 이미지/오브젝트를 보존했습니다. 최종 게임 화면은 사용자 확인 대기입니다.

홍보 이미지 최종본은 `promos_v12b.json`과 `generated/promo_*_ko_v12b.png`입니다. 생성물 외곽의 색 잡음을 줄이기 위해 원본 알파를 다시 사용하고 경계의 원래 RGB 픽셀을 복원했습니다(작은 배너 3px, 큰 안내 그림 12px 경계 띠).

## v13~v18: 도서관·엔딩·배경 글씨

포커 4색, 비트코인 작은 캡션 4색, 노트, 크라우드펀딩 4색, 엔딩 사진 2종, 칠판 2종, 광고 메일 4색, 엔딩 문구/프롬 킹 띠/가족 그림 4종, 급식실·화장실·도시·프롤로그 배경 5종을 추가했습니다. 중복 수정 제외 30개 텍스처입니다. 각각 생성 파일명에 대응하는 `*_prompt.md`에 정확한 프롬프트가 있습니다.

최종 적용 순서: `library_images_v13.json` → `library_images_v13b.json` → `crowdfunding_v14.json` → `ending_images_v15.json` → `chalk_images_v15b.json` → `scam_images_v16.json` → `ending_details_v17.json` → `promking_v17c.json` → `backgrounds_v18.json`.

포커·캡션은 첫 결과의 색과 여백을 고친 v13b를 사용합니다. 칠판 상단 영문 끝조각은 v15b에서 범위를 넓혀 제거했습니다. `baseline`은 지정한 로컬 단계 백업에서 해당 텍스처만 복원한 뒤 최종 생성 영역을 가져오는 옵션입니다. 다른 최신 텍스처나 대사를 되돌리지 않습니다.

광고 메일은 생성한 본문 패널과 공통 메일 로고·받는 이 라벨만 조립했습니다. 원본의 가상 URL은 유지합니다. `scam_*_composite16.png`가 적용용 파일입니다. 프롬 킹 띠는 실험 마스크에서 영문 흔적이 남아 최종 v17c의 생성 영역으로 복구했습니다. 마스크 실험은 로컬 참고 폴더에만 보관합니다.

`verify_image_regions.py`로 실제 설치본을 다시 읽어 치수, 원본 알파, 지정 영역 밖 픽셀이 동일한지 검사했습니다. 검증 결과는 `reports/images_v13_v15.json`, `reports/images_v16_v18.json`에 있습니다. 글씨 주변을 포함한 사각형 안에는 생성 과정의 질감·색 차이가 있을 수 있으며 게임 화면은 사용자 확인 대기입니다.

## v19~v27: 추가 UI·갤러리·커플 사진

v19~v23은 엔딩/앨범·선거 8개, 온라인 아바타 1개, 영업/DLC/해설자/가족 그림 7개, 홍보 7개, 상점/옵션 아틀라스 2개, 총 25개 텍스처입니다. 앞선 v13~v18 30개와 합쳐 55개입니다.

v24~v27에서 갤러리·소품 9개, 커플 사진 하단 캡션 32개를 추가했습니다. 검토 후보 42개 중 654 네온 간판은 사용자의 장식 간판 유지 요청에 따라 적용하지 않았습니다. 생성 단계에서 함께 바뀐 배경 간판/책/게임 제목도 합성에 사용하지 않고 원본을 유지했습니다. 작가 서명·브랜드·숫자 역시 유지합니다.

내장 image_gen으로 생성한 원본 결과는 `generated/`, 각 입력 프롬프트는 `*_prompt.md`입니다. 최종 적용은 `gallery_v24_v25.json`, `captions_v26.json`, `photos_v27.json`입니다. 커플 사진 중 14개는 사진 안으로 걸친 기존 캡션 제거 또는 손글씨 수정을 위해 전체 참고 이미지에서 수정본을 생성한 뒤 글자 영역만 합성했습니다. 그 밖의 18개는 검수한 2열4행 캡션 시트에서 정확한 셀 경계로 잘라 배치했습니다. 원본 알파와 대상 밖 픽셀은 보존했습니다.

이번 재개 이후 중복 제외 96개 텍스처 추가 적용. 게임 화면 확인은 사용자 대기입니다. 텍스트 영역 검증 보고서는 `reports/images_v19_v20.json`, `reports/images_v21_v23.json`, `reports/images_v24_v25.json`, `reports/images_v26.json`, `reports/images_v27.json`에 있습니다.

## v28: 시작 잡지 가로 폭 수정

기존 v9 한글 잡지 표지가 원본보다 좁게 들어갔다는 사용자 피드백을 반영했습니다. 사용자의 가로 늘리기 요청에 따라 기존 설치 이미지의 x=0~490 영역을 원본 644×836 크기로 가로 방향만 리샘플하고 최초 원본 알파를 복원했습니다. 새 이미지 생성 결과는 사용하지 않았습니다. 최종 파일은 `generated/magazine_width_fix_v28.png`, 적용은 `magazine_width_fix_v28.json`, 검사 결과는 `reports/magazine_width_fix_v28.json`입니다. 다른 텍스처와 오브젝트는 보존했습니다.
