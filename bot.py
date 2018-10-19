#!/usr/bin/env python3

import os

from PIL import Image
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

from img_to_hearts import img_to_hearts

images_path = os.getenv("IMG_PATH")

count = 0


def start(bot, update):
    msg = "Я бот, который сделает из фото изображение из сердечек! Отошли мне изображение, чтобы попробовать!"
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg)


def img_to_heart(bot, update):
    global count
    file_id = update.message.photo[-1].file_id
    chat_id = update.message.chat_id
    print(file_id)
    bot.send_message(chat_id=chat_id, text="Класс! Картинка! Уже начинаю обработку..")
    # обработать
    new_file = bot.get_file(file_id)
    new_file.download(images_path + file_id + '.jpg')

    img = img_to_hearts(Image.open(images_path + file_id + '.jpg'))
    img.save(images_path + 'hearted_' + file_id + '.jpg')
    # залить и переслать
    bot.send_photo(chat_id=chat_id, photo=open(images_path + 'hearted_' + file_id + '.jpg', 'rb'))
    count += 1


def main():
    token = os.getenv("token")
    request_kwargs = {
        'proxy_url': 'socks5://localhost:9050',
    }
    updater = Updater(token=token, request_kwargs=request_kwargs)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    img_handler = MessageHandler(Filters.photo, img_to_heart)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(img_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
