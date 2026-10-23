# 추가 이미지 v2

기본 내장 image_gen 도구의 text-localization 방식으로 생성했습니다. 원본은 게임 설치본에서 로컬로 추출해 참조했으며 원본 파일은 Git에서 제외합니다.

- Second Term: `../logo/monster_prom_second_term_ko_v2.png`
- 메인 메뉴 생성 아틀라스: `generated/main_menu_ko_v2.png`
- 실제 적용 시 원본 텍스처 크기에 맞춰 리샘플하고 대상 버튼 영역만 교체합니다. 레이아웃과 스프라이트 영역은 게임 원본 기준입니다.

## Second Term 프롬프트

Use case text-localization. Edit this exact Monster Prom Second Term expansion logo. Keep its original gray shield, gray clasped skeletal hands, black outlines, purple ribbon with ivory border, flat angular comic artwork and full composition. Replace MONSTER with exactly "몬스터" in bold black angular Hangul, PROM with exactly "프롬" in hot pink angular Hangul. Replace the ribbon SECOND TERM with Korean "두 번째 학기": put exactly "두 번째" on the left ribbon and exactly "학기" on the right ribbon. All Korean must be clearly spelled and legible. Keep the logo square 1024x1024 with matching placement and safe transparent padding. The purple ribbon must have clean fully transparent outer background, no white or beige rectangular blocks. Preserve the ivory ribbon edging only. No English letters, extra ornaments, backdrop, or watermark. This is a localized game texture, not a mockup.

## 메인 메뉴 프롬프트

Use case text-localization. Edit the supplied game menu texture ATLAS. Output landscape 2048x1024 exactly with the SAME pixel placement, size, silhouettes and spacing of ALL arrow-shaped buttons and small decorations. It is a packed sprite atlas, not a newly arranged sheet: DO NOT move, scale, rotate or redesign any element. Change ONLY the lettering: SETTINGS -> "설정"; MODTOOL -> "모드 도구"; QUIT -> "종료"; PLAY -> "시작"; GALLERY -> "갤러리"; ONLINE -> "온라인". Match the original ivory hand-drawn narrow irregular lettering but with complete readable Hangul. Keep arrow plates black or hot pink exactly as reference, ivory thin borders, subtle geometric shading and original orientations. Keep every blank patch and small decoration exactly in its original location. True transparent background. No English letters or added captions. All lettering must remain strictly inside its original arrow button bounds.
