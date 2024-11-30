from random import choice

import redis
from environs import Env
from get_questions import get_answer_and_questions
from logging_config import start_logger
from telegram import Bot, ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, Filters, MessageHandler, Updater


CHOOSINGS = 1


def start(update: Update, context: CallbackContext) -> None:
    tg_chat_id = update.message.chat_id
    custom_keyboard = [["Новый вопрос"], ["Сдаться"]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(
        chat_id=tg_chat_id,
        text="Добро пожаловть в quiz бота",
        reply_markup=reply_markup,
    )
    return CHOOSINGS


def new_questions(update: Update, context: CallbackContext) -> None:
    tg_chat_id = update.message.chat_id
    db_connection = context.bot_data["redis_connect"]
    random_questions = choice(list(context.bot_data["answer_and_questions"].keys()))
    db_connection.set(tg_chat_id, random_questions)
    context.bot.send_message(chat_id=tg_chat_id, text=random_questions)
    return CHOOSINGS


def get_answer(update: Update, context: CallbackContext) -> None:
    tg_chat_id = update.message.chat_id
    db_connection = context.bot_data["redis_connect"]
    question = db_connection.get(tg_chat_id)
    answer = context.bot_data["answer_and_questions"].get(question)
    context.bot.send_message(chat_id=tg_chat_id, text=answer)
    new_questions(update, context)


def check_question(update: Update, context: CallbackContext) -> None:
    user_answer = update.effective_message.text
    tg_chat_id = update.message.chat_id
    db_connection = context.bot_data["redis_connect"]

    question = db_connection.get(tg_chat_id)
    answer = context.bot_data["answer_and_questions"].get(question)
    answer = answer.split(":")
    answer = answer[1].strip()

    if "." in answer:
        answer = answer.split(".")[0]
    elif "(" in answer:
        answer = answer.split("(")[0]

    if answer.lower() == user_answer.lower():
        context.bot.send_message(chat_id=tg_chat_id, text="Верно!!!")
        new_questions(update, context)
    else:
        context.bot.send_message(
            chat_id=tg_chat_id, text="Неверно, попробуйте ещё или нажмите 'Cдаться'"
        )


def main() -> None:
    env = Env()
    env.read_env()
    tg_chat_id = env.str("TG_CHAT_ID")
    tg_bot_token = env.str("TG_BOT_TOKEN")
    redis_address = env.str("REDIS_ADDRESS")
    redis_port = env.str("REDIS_PORT")
    redis_password = env.str("REDIS_PASSWORD")
    try:
        redis_connect = redis.Redis(
            host=redis_address,
            port=redis_port,
            password=redis_password,
            decode_responses=True,
        )
        bot = Bot(tg_bot_token)
        updater = Updater(tg_bot_token)
        dispatcher = updater.dispatcher
        logger = start_logger(bot, tg_chat_id)
        logger.info("Бот телеграм запущен")

        answer_and_questions = get_answer_and_questions("1vs1200.txt", "KOI8-R")
        dispatcher.bot_data["redis_connect"] = redis_connect
        dispatcher.bot_data["answer_and_questions"] = answer_and_questions

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                CHOOSINGS: [
                    MessageHandler(Filters.regex("Новый вопрос"), new_questions),
                    MessageHandler(Filters.regex("Сдаться"), get_answer),
                    MessageHandler(Filters.text, check_question),
                ],
            },
            fallbacks=[CommandHandler("start", start)],
        )
        dispatcher.add_handler(conv_handler)
        updater.start_polling()
        updater.idle()
    except ConnectionError as e:
        logger.error("Ошибка:", e)


if __name__ == "__main__":
    main()
