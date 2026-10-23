# 제공된 태국어 모드 구조 참고

2026-10-23 사용자가 제공한 `Monster Prom Thai Mod v1.0.0-R17` ZIP을 로컬에서 읽고 비교했습니다. 제작자 표기는 동봉 README 기준 `มีเกมก็แปล By.Stamp Nattakit`입니다.

## 확인한 구조

- 게임 시작 시 `GeneralManager.ChangeLanguage(ELanguage.Chinese)`를 호출하도록 관리 어셈블리가 변경되어 있습니다.
- `UILabel.CheckLanguageFont`의 중국어 분기는 NGUI 비트맵 폰트를 비우고 `DefaultChineseFont`를 동적 폰트로 사용합니다.
- 폰트 3397의 이름은 `Kodchasan`으로 변경되어 있으며, 언어별 이미지 번들 `localization_ch_*`와 씬·에셋도 함께 제공됩니다. README에는 TPUA 방식이라고 설명되어 있습니다.
- 기본 화면은 공유 에셋의 이미지 아틀라스, 언어별 화면은 StreamingAssets 이미지 번들을 사용하는 구조를 다시 확인했습니다.

## 한국어 작업에 반영

한국어는 원본 영어를 기준으로 번역하고 영어 슬롯에 적용합니다. 미번역 문장이 중국어로 나타나는 일을 피하면서, 영어 화면이 참조하는 NGUI `UIFont` 8개를 한글 지원 동적 폰트에 연결하는 방식을 사용했습니다. 코드상 `UIFont.isDynamic`과 `UILabel.trueTypeFont` 경로가 연결되는 것을 확인했습니다.

기존 기본 로고뿐 아니라 Second Term 전용 로고와 메인 메뉴 버튼 이미지 6개를 추가로 교체했습니다. 나머지 이미지와 본문은 후속 번역 범위입니다.

태국어 모드의 DLL·폰트·텍스처·번역문은 한국어 패치에 복사하지 않았습니다. 제공 자료는 로컬 `reference/`에만 두고 Git에서 제외합니다. ZIP의 설치 프로그램이나 DLL을 실행하지 않았습니다.

이 분석은 구조에 관한 확인입니다. 한국어 v2의 실제 렌더링 성공 판정은 사용자 화면 확인 후에 기록해야 합니다.
