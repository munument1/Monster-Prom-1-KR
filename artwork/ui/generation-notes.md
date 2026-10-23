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
