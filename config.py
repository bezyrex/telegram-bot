import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


def _load_env() -> None:
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env()

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ADMIN_IDS = {
    int(x)
    for x in os.environ.get("TELEGRAM_ADMIN_IDS", "").replace(" ", "").split(",")
    if x
}
PROTECTED_CONTAINERS = frozenset(
    name.strip()
    for name in os.environ.get("PROTECTED_CONTAINERS", "").split(",")
    if name.strip()
)


def is_authorized(user_id: int | None) -> bool:
    if not ADMIN_IDS:
        return True
    return user_id in ADMIN_IDS
