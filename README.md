# Телеграм & ВКонтакте quizz-bot

В репозитории находятся два бота для игры в викторину.

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
