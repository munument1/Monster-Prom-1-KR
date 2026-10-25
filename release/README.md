# 릴리즈 재현

기존 개발 폴더의 최초 백업과 최종 설치 스테이징이 필요합니다. 게임 바이너리와 생성된 배포 ZIP은 Git에 커밋하지 않고 릴리즈 첨부 파일로 배포합니다.

```powershell
python -m pip install -r release/requirements-build.txt
python release/build_release.py payload
python -m PyInstaller --noconfirm --clean --onefile --windowed --name MonsterPromKR-Patcher --distpath release_build/installer --workpath release_build/pyinstaller --specpath release_build release/patcher.py
python release/build_release.py archive
```

`build_release.py payload`는 원본·수정본 해시를 확인하고 파일별 bsdiff를 만듭니다. 각 변경분으로 원본을 재구성한 결과가 최종 수정본 해시와 같은지 검사합니다. 원본 전체 파일은 ZIP에 넣지 않습니다.

Windows 설치 패처 소스는 `patcher.py`입니다. 개발·자동 검증용으로 `--action install|restore|verify --game-dir <폴더> --package <패키지 폴더> --result <결과 JSON>`을 지원합니다. 일반 사용자는 인자 없이 실행해 GUI를 사용합니다.

## 파일 덮어쓰기판

```powershell
python release/build_overwrite.py
python release/test_overwrite_package.py
```

기존 v0.1 패키지 목록과 최종 수정본 해시가 일치할 때만 25개 수정 파일을 `MonsterProm_Data/` 경로로 ZIP에 담습니다. 기존 Windows 설치형 ZIP을 변경하지 않고 수동 설치 ZIP을 추가하며, SHA256SUMS.txt에 두 배포본을 함께 기록합니다. Steam Deck은 Windows판+Proton을 대상으로 안내합니다. 실기 실행은 별도 확인이 필요합니다.
