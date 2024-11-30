import random

import redis
import vk_api as vk
from environs import Env
from get_questions import get_answer_and_questions
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkEventType, VkLongPoll


def new_questions(event, vk_api, redis_connect, answer_and_questions, keyboard):
    vk_chat_id = event.user_id
    random_questions = random.choice(list(answer_and_questions.keys()))
    redis_connect.set(vk_chat_id, random_questions)
    vk_api.messages.send(
        user_id=event.user_id,
        message=random_questions,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard(),
    )


def get_answer(event, vk_api, redis_connect, answer_and_questions, keyboard):
    vk_chat_id = event.user_id
    question = redis_connect.get(vk_chat_id)
    answer = answer_and_questions.get(question)
    vk_api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard(),
    )
    new_questions(event, vk_api, redis_connect, answer_and_questions, keyboard)


def check_question(event, vk_api, redis_connect, answer_and_questions, keyboard):
    user_answer = event.text
    tg_chat_id = event.user_id

    question = redis_connect.get(tg_chat_id)
    answer = answer_and_questions.get(question)
    answer = answer.split(":")
    answer = answer[1].strip()

    if "." in answer:
        answer = answer.split(".")[0]
    elif "(" in answer:
        answer = answer.split("(")[0]

    if answer.lower() == user_answer.lower():
        vk_api.messages.send(
            user_id=event.user_id,
            message="Все верно!",
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard(),
        )
        new_questions(event, vk_api, redis_connect, answer_and_questions, keyboard)
    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message="Неверно! Попробуйте еще",
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard(),
        )


if __name__ == "__main__":
    env = Env()
    env.read_env()

    redis_address = env.str("REDIS_ADDRESS")
    redis_port = env.str("REDIS_PORT")
    redis_password = env.str("REDIS_PASSWORD")
    redis_connect = redis.Redis(
        host=redis_address,
        port=redis_port,
        password=redis_password,
        decode_responses=True,
    )

    answer_and_questions = get_answer_and_questions("1vs1200.txt", "KOI8-R")
    vk_bot_token = env.str("VK_BOT_TOKEN")
    vk_session = vk.VkApi(token=vk_bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button("Новый вопрос")
    keyboard.add_button("Сдаться")
    keyboard.add_line()
    keyboard.add_button("Мои очки")

    for event in longpoll.listen():
        if not (event.type == VkEventType.MESSAGE_NEW and event.to_me):
            continue
        if event.text == "/start":
            vk_api.messages.send(
                user_id=event.user_id,
                random_id=random.randint(1, 1000),
                keyboard=keyboard.get_keyboard(),
                message="Выберете действие",
            )
        if event.text == "Новый вопрос":
            new_questions(event, vk_api, redis_connect, answer_and_questions, keyboard)
        elif event.text == "Сдаться":
            get_answer(event, vk_api, redis_connect, answer_and_questions, keyboard)
        else:
            check_question(event, vk_api, redis_connect, answer_and_questions, keyboard)
