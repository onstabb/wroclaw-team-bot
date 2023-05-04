import os
from pathlib import Path

from dotenv import load_dotenv
from pytz import timezone

load_dotenv()

BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
MONGODB_URI: str = os.environ.get("MONGODB_URI", "")
DB_NAME: str = "WroclawTeamDB"

PROXY_URL: str = os.environ.get("PROXY_URL", "")
I18N_DOMAIN: str = 'WroclawTeamBot'
BASE_DIR: Path = Path(__file__).parent.parent
LOCALE_DIR: Path = BASE_DIR / 'locales'
DEFAULT_LANGUAGE: str = "pl"
MAIN_TIMEZONE = timezone("Europe/Warsaw")


