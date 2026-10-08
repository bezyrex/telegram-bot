from telegram import Update
from telegram.ext import ContextTypes

from docker_cli import docker
from helpers import reply, usage


async def _run(update: Update, label: str, *args: str) -> None:
    code, out = await docker(*args)
    await reply(update, out or f"docker {label} failed (code {code})")


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _run(
        update,
        "stats",
        "stats",
        "--no-stream",
        "--format",
        "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}",
    )


async def cmd_images(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _run(
        update,
        "images",
        "images",
        "--format",
        "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}",
    )


async def cmd_pull(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await usage(update, "Usage: /pull <image[:tag]>")
        return
    await _run(update, "pull", "pull", context.args[0])


async def cmd_df(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _run(update, "system df", "system", "df")


HANDLERS = [
    ("stats", cmd_stats),
    ("images", cmd_images),
    ("pull", cmd_pull),
    ("df", cmd_df),
]
