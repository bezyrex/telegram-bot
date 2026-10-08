from telegram.ext import CommandHandler, filters

from commands import basic, compose, containers, system
from config import ADMIN_IDS

HANDLERS = (
    basic.HANDLERS
    + containers.HANDLERS
    + system.HANDLERS
    + compose.HANDLERS
)

USER_FILTER = filters.User(user_id=ADMIN_IDS) if ADMIN_IDS else None


def register(application) -> None:
    for name, callback in HANDLERS:
        application.add_handler(CommandHandler(name, callback, filters=USER_FILTER))
