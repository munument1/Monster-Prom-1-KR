# 한글 로고 시안 v1

- 도구: 기본 내장 image_gen, imagegen 스킬의 text-localization 방식
- 원본: 게임 resources.assets의 Texture2D path ID 224, 이름 logo, 1024×1024
- 시안: monster_prom_logo_ko_v1.png
- 게임의 기본 로고 및 축소 버전 3개에 적용 완료. 원본 텍스처 크기에 맞추고 투명 영역을 유지했으며, 스프라이트 메시를 조정함. 적용 기록: patch_v1/verification.json. 화면 검증은 사용자 진행 예정.

## 사용 프롬프트

Use case: text-localization. Edit target: the supplied original Monster Prom 1 game logo. Produce a Korean localized logo asset on a genuinely transparent background, square 1024x1024 composition matching the original. Replace ONLY the two English lettering lines: top MONSTER becomes exactly "몬스터" (three Hangul syllables 몬 스 터), bottom PROM becomes exactly "프롬" (two Hangul syllables 프 롬). The top Korean line must have tall black angular hand-drawn display lettering, the bottom Korean line vivid hot pink lettering with the original dark magenta dimensional shadow. Fit each Korean line naturally within the original plaque with bold readable complete Hangul glyphs. Preserve the original gray shield/plaque silhouette, its border, chips and geometric shading, the two small bat wings, and the prominent clasped gray skeletal/monster hands and forearms across the bottom. Preserve the original flat comic graphic style, strong black outlines, original color palette and overall arrangement. No English lettering, extra text, background scene or watermark. All non-text visual elements should remain as close to the reference as possible. This is an actual game logo localization asset, not a presentation or mockup.
