from telegram.ext import Application

from events import errors


def register(application: Application) -> None:
    application.add_error_handler(errors.on_error)
