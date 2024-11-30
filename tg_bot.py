import logging

from environs import Env
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    tg_chat_id = update.message.chat_id
    custom_keyboard = [["Новый вопрос", "Сдаться"], ["Мой счет"]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(
        chat_id=tg_chat_id,
        text="Добро пожаловть в quiz бота",
        reply_markup=reply_markup,
    )


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main() -> None:
    env = Env()
    env.read_env()
    tg_bot_token = env.str("TG_BOT_TOKEN")

    updater = Updater(tg_bot_token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
