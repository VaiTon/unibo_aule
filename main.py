from datetime import datetime
import os
import sys

import tzlocal
import dateutil.parser
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, Updater
from dotenv import load_dotenv

import aule

load_dotenv()  # Load .env file

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    print("BOT_TOKEN not set")
    exit(-1)


def aule_libere(update: Update, context: CallbackContext):
    time = datetime.now(tzlocal.get_localzone())

    aule_libere, impegni_map = aule.aule_libere(time)

    aule_txt = []

    for id in aule_libere:
        aule_txt.append(f"- {aule_libere[id]['descrizione']}\n")

        if impegni_map[id]:
            aule_txt.append(
                f" -> Prossima lezione alle {dateutil.parser.parse(impegni_map[id]['startTime']).strftime('%H:%M')}\n"
            )

    orario = time.strftime("%H:%M")

    text = f"<b>Trovate {len(aule_libere)} aule libere alle ore {orario}:</b>\n\n{''.join(aule_txt)}"

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML
    )


updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("aulelibere", aule_libere))

updater.start_polling()
