from telegram import Update
from telegram.ext import ContextTypes

HELP_TEXT = (
    "/ps [filter] - containers (-a)\n"
    "/inspect <name> - details\n"
    "/logs <name> [n] - recent logs\n"
    "/top <name> - processes\n"
    "/exec <name> <command> - run command\n"
    "/start_c <name> - start\n"
    "/stop <name> - stop\n"
    "/restart <name> - restart\n"
    "/rm <name> - remove (-f)\n"
    "/stats - resource usage\n"
    "/images - images\n"
    "/pull <image> - pull image\n"
    "/df - disk\n"
    "/compose <path> <action> - docker compose\n"
    "/protected - protected containers"
)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "Docker control bot.\nUse /help to see commands.\n\nCommands:\n"
        + HELP_TEXT
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(HELP_TEXT)


HANDLERS = [
    ("start", cmd_start),
    ("help", cmd_help),
]
