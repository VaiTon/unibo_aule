from datetime import datetime
import os
import sys

import tzlocal
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, Updater

import aula

BOT_TOKEN = os.environ["BOT_TOKEN"]


def aule_libere(update: Update, context: CallbackContext):
    time = datetime.now(tzlocal.get_localzone())
    aule_libere = aula.aule_libere(time)

    aule = [f"- {aula['descrizione']}\n" for aula in aule_libere]

    text = f"<b>Trovate {len(aule_libere)} aule libere:</b>\n\n{''.join(aule)}"

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML
    )


updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("aulelibere", aule_libere))

updater.start_polling()
