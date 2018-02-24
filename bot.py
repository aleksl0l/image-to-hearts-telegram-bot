#!/usr/bin/env python3

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import os
from img_to_hearts import img_to_hearts
from PIL import Image
from daemon import runner

token_path = '/home/alex/git/image_to_hearts/token'
images_path = '/home/alex/images/'


count = 0
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Я бот, который сделает из фото сердечное фото! Отошли мне изображение, чтобы попробовать!")

def img_to_heart(bot, update):
    global count
    file_id = update.message.photo[-1].file_id
    chat_id = update.message.chat_id
    print(file_id)
    bot.send_message(chat_id=chat_id, text="Класс! Ты прислал картинку!")
    #обработать
    newFile = bot.get_file(file_id)
    newFile.download(images_path + str(count) + '.jpg')

    img = img_to_hearts(Image.open(images_path + str(count) + '.jpg'))
    img.save(images_path + 'hearted_'+str(count)+'.jpg')
    # 
    # data = None
    # with io.BytesIO() as output:
    #     img.save(output, 'PNG')
    #     data = output.getvalue()
    # 
    # imgByteArr = io.BytesIO()
    # img.save(imgByteArr, format='PNG')
    # imgByteArr = imgByteArr.getvalue()
    # os.system('python3 /home/alexlol/img_to_hearts.py ' + '/home/alexlol/images/'+str(count)+'.jpg')

    #залить и переслать
    bot.send_photo(chat_id=chat_id, photo=open(images_path + 'hearted_'+str(count)+'.jpg', 'rb'))
    # bot.send_photo(chat_id=chat_id, photo=img.getdata())
    count += 1
    # bot.send_photo(chat_id=chat_id, photo=file_id)



class Main():
    def run(self):
        with open(token_path, 'r') as myfile:
                token = myfile.read()
        token = token[:-1]
        updater = Updater(token=token)
        
        dispatcher = updater.dispatcher
        
        # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        
        start_handler = CommandHandler('start', start)
        img_handler = MessageHandler(Filters.photo, img_to_heart)
        
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(img_handler)
        updater.start_polling()
        

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/bot.pid'
        self.pidfile_timeout = 5
            
    def run(self):
        service = Main()
        service.run()
        
app = App()
# logger = logging.getLogger("DaemonLog")
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# handler = logging.FileHandler("/var/log/testdaemon/testdaemon.log")
# handler.setFormatter(formatter)
# logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
# daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
        
        




