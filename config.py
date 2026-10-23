"""Local installation configuration; no game files are included in this repo."""
from pathlib import Path
import os
GAME_DIR=Path(os.environ.get('MPKR_GAME_DIR',r'C:\Games\Steam\steamapps\common\Monster Prom'))
GAME_DATA=GAME_DIR/'MonsterProm_Data'
