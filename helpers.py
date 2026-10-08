import html

from telegram import Update
from telegram.constants import ParseMode

from protection import is_protected

TELEGRAM_LIMIT = 4000
MAX_CHUNKS = 20

PROTECTED_MSG = (
    "Blocked: {name} is the bot container. "
    "I cannot stop it from Telegram."
)


async def reply(update: Update, text: str, silent: bool = False) -> None:
    text = text.strip() or "(no output)"
    chunks = [text[i : i + TELEGRAM_LIMIT] for i in range(0, len(text), TELEGRAM_LIMIT)]
    for chunk in chunks[:MAX_CHUNKS]:
        await update.effective_message.reply_text(
            f"<pre>{html.escape(chunk)}</pre>",
            parse_mode=ParseMode.HTML,
            disable_notification=silent,
        )
    if len(chunks) > MAX_CHUNKS:
        await update.effective_message.reply_text(
            f"... ({len(chunks) - MAX_CHUNKS} more chunks omitted)"
        )


async def usage(update: Update, text: str) -> None:
    await update.effective_message.reply_text(text)


async def refuse_protected(update: Update, name: str) -> bool:
    if not await is_protected(name):
        return False
    await update.effective_message.reply_text(PROTECTED_MSG.format(name=name))
    return True
