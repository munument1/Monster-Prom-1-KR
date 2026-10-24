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
