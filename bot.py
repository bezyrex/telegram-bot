import asyncio
import time

from telegram import Bot, Update
from telegram.error import InvalidToken, NetworkError, TimedOut
from telegram.ext import Application, ApplicationBuilder

import commands
import events
from config import TOKEN

CONNECT_TIMEOUT = 20.0
READ_TIMEOUT = 30.0
LONG_POLL_TIMEOUT = 25
BOOTSTRAP_RETRIES = 10
BACKOFF_START = 5
BACKOFF_MAX = 60

NETWORK_ERRORS = (TimedOut, NetworkError, OSError)

PROXY_HINT = (
    "If you use a VPN/proxy, set HTTPS_PROXY=http://host:port in .env ("
    "host.docker.internal:port also works if the proxy runs on Windows)."
)


def backoff(attempt: int) -> int:
    return min(BACKOFF_START * attempt, BACKOFF_MAX)


def build_application() -> Application:
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .connect_timeout(CONNECT_TIMEOUT)
        .read_timeout(READ_TIMEOUT)
        .pool_timeout(10.0)
        .get_updates_connect_timeout(CONNECT_TIMEOUT)
        .get_updates_read_timeout(READ_TIMEOUT + LONG_POLL_TIMEOUT)
        .get_updates_pool_timeout(10.0)
        .build()
    )
    commands.register(app)
    events.register(app)
    return app


async def check_token() -> str:
    bot = Bot(TOKEN)
    async with bot:
        me = await bot.get_me()
    return me.username


def validate_token() -> None:
    attempt = 0
    while True:
        attempt += 1
        try:
            username = asyncio.run(check_token())
            print(f"Connected to Telegram as @{username}.", flush=True)
            return
        except InvalidToken:
            raise SystemExit("Invalid token. Check @BotFather and .env")
        except NETWORK_ERRORS as exc:
            delay = backoff(attempt)
            extra = f" {PROXY_HINT}" if attempt == 1 else ""
            print(
                f"No connection to Telegram ({type(exc).__name__}). "
                f"Retrying in {delay}s (attempt {attempt}).{extra}",
                flush=True,
            )
            time.sleep(delay)


def run() -> None:
    attempt = 0
    while True:
        app = build_application()
        try:
            app.run_polling(
                allowed_updates=Update.ALL_TYPES,
                bootstrap_retries=BOOTSTRAP_RETRIES,
                timeout=LONG_POLL_TIMEOUT,
                poll_interval=0.5,
            )
            return
        except NETWORK_ERRORS as exc:
            attempt += 1
            delay = backoff(attempt)
            print(
                f"Network error ({type(exc).__name__}: {exc}). "
                f"Reconnecting in {delay}s (attempt {attempt}).",
                flush=True,
            )
            time.sleep(delay)


def main() -> None:
    if not TOKEN:
        raise SystemExit(
            "TELEGRAM_BOT_TOKEN missing. Create a bot with @BotFather and put the token in .env"
        )
    validate_token()
    print("Bot started.", flush=True)
    run()


if __name__ == "__main__":
    main()
