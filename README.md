# Телеграм & ВКонтакте quizz-bot

В репозитории находятся два бота для игры в викторину.


https://github.com/user-attachments/assets/246e91db-0542-44af-8583-f555764c180f

https://github.com/user-attachments/assets/704cd70a-5000-46b1-8f70-ec1487dbd537


Пример работы Telegram бота:

## Запуск

У вас уже должен быть установлен python3.

```
pip intsall -r requirements.txt
```

Создайте `.env` файл и поместите туда следующие строки:

```
TG_BOT_TOKEN=<Token бота телеграм>
TG_CHAT_ID=<Ваш id телеграм для отправки сообщений о логировании>
VK_BOT_TOKEN=<Token бота ВКонтакте>
REDIS_ADDRESS=<Адресс Redis>
REDIS_PORT=<порт Redis>
REDIS_PASSWORD=<Парот от Redis>

```

## Запуск prod версии

- Скопируйте репозиторий к себе на сервер
- Создайте файл `env`
- Выполните команду `docker-compose up -d`
