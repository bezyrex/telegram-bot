from telegram import Update
from telegram.ext import ContextTypes


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(f"Error: {context.error}")
    else:
        print(f"Error: {context.error}")
