import requests
import os
import time
import json

# Вставьте сюда свой токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN") or "7695628682:AAHr6xFTBfYLAXd78_7NXUAXljlTf77uA2g"

# Ссылка на канал
CHANNEL_LINK = "https://t.me/+DZbUdjgiK61kNWQy"

# URL для доступа к API Telegram
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# Функция для получения обновлений
def get_updates(offset=None):
    response = requests.get(URL + "getUpdates", params={'offset': offset})
    return response.json()

# Функция для отправки сообщения
def send_message(chat_id, text, reply_markup=None):
    data = {'chat_id': chat_id, 'text': text}
    if reply_markup:
        data['reply_markup'] = reply_markup
    response = requests.post(URL + "sendMessage", data=data)
    return response.json()

# Функция для отправки приветственного сообщения с кнопкой снизу
def send_welcome(chat_id):
    # Обычная кнопка снизу сообщения
    keyboard = {
        "keyboard": [
            [{"text": "✅ Я не робот"}]
        ],
        "resize_keyboard": True,  # Автоматически подогнать размер
        "one_time_keyboard": True  # Скрыть клавиатуру после нажатия
    }
    send_message(chat_id, "Привет! Чтобы перейти в закрытый канал, подтвердите, что вы не робот.", json.dumps(keyboard))

# Функция для обработки обновлений сообщений
def process_update(update):
    message = update['message']
    chat_id = message['chat']['id']
    text = message.get('text', '')

    # Если команда /start
    if text == "/start":
        send_welcome(chat_id)
    # Если пользователь нажал кнопку "Я не робот"
    elif text == "✅ Я не робот":
        send_message(chat_id, f"✅ Спасибо за подтверждение! Вот ссылка: {CHANNEL_LINK}")

# Основная функция, которая будет постоянно проверять обновления
def main():
    offset = None
    while True:
        updates = get_updates(offset)

        if "result" in updates:
            for update in updates['result']:
                if 'message' in update:
                    process_update(update)

                offset = update['update_id'] + 1  # Обновляем offset

        # Задержка между запросами обновлений
        time.sleep(1)

if __name__ == "__main__":
    main()
