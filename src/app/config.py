import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_PANEL_PATH = os.environ.get("ADMIN_PANEL_PATH", "/admin")
ROOT_PATH = os.environ.get("ROOT_PATH", "")
