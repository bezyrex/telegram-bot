import asyncio
import subprocess
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from helpers import reply, usage
from protection import compose_conflict

ALLOWED_ACTIONS = {"up", "down", "ps", "logs", "restart", "pull", "build"}
CLOSING_ACTIONS = {"up", "down", "restart"}


async def cmd_compose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await usage(
            update,
            "Usage: /compose <project_path> <"
            + "|".join(sorted(ALLOWED_ACTIONS))
            + ">",
        )
        return

    path = Path(context.args[0]).expanduser()
    action = context.args[1]

    if action not in ALLOWED_ACTIONS:
        await usage(
            update, f"Allowed actions: {', '.join(sorted(ALLOWED_ACTIONS))}"
        )
        return
    if not path.exists():
        await usage(update, f"Not found: {path}")
        return

    if action in CLOSING_ACTIONS:
        conflict = await compose_conflict(path)
        if conflict:
            await update.effective_message.reply_text(
                f"Blocked: {path} includes the bot container ({conflict}). "
                "docker compose cannot stop it from Telegram."
            )
            return

    extra = ["-d"] if action == "up" else []
    try:
        proc = await asyncio.to_thread(
            subprocess.run,
            ["docker", "compose", action, *extra],
            cwd=str(path),
            capture_output=True,
            text=True,
            check=False,
            timeout=300,
        )
    except (OSError, subprocess.TimeoutExpired):
        await update.effective_message.reply_text("Timeout or error running docker compose")
        return

    out = ((proc.stdout or "") + (proc.stderr or "")).strip()
    await reply(update, out or f"docker compose {action} -> code {proc.returncode}")


HANDLERS = [
    ("compose", cmd_compose),
]
