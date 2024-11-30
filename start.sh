#!/bin/bash

if [ "$1" == "tg_bot" ]; then
  exec python tg_bot.py
elif [ "$1" == "vk_bot" ]; then
  exec python vk_bot.py
else
  echo "Неизвестный параметр: $1. Используйте 'web' или 'bot'."
  exit 1
fi
