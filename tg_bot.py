import logging
from random import choice

import redis
from environs import Env
from get_questions import get_answer_and_questions
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


def main_handler(update: Update, context: CallbackContext) -> None:
    tg_chat_id = update.message.chat_id
    db_connection = context.bot_data["resid_connect"]
    random_questions = choice(list(context.bot_data["answer_and_questions"].keys()))
    db_connection.set(tg_chat_id, random_questions)

    user_message = update.message.text
    if user_message == "Новый вопрос":
        context.bot.send_message(chat_id=tg_chat_id, text=random_questions)


def main() -> None:
    env = Env()
    env.read_env()
    tg_bot_token = env.str("TG_BOT_TOKEN")
    redis_address = env.str("REDIS_ADDRESS")
    redis_port = env.str("REDIS_PORT")
    redis_password = env.str("REDIS_PASSWORD")
    redis_connect = redis.Redis(
        host=redis_address, port=redis_port, password=redis_password
    )

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    answer_and_questions = get_answer_and_questions("1vs1200.txt", "KOI8-R")
    dispatcher.bot_data["resid_connect"] = redis_connect
    dispatcher.bot_data["answer_and_questions"] = answer_and_questions

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, main_handler)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
