import telebot
import matplotlib.pyplot as plt
import numpy as np
import datetime
import math
import numexpr as ne

bot = telebot.TeleBot('TOKEN')

def graph(func):

    try:
        x = []
        y = []

        for i in range(1000):
            r = ne.evaluate(func.replace("x", str(i / 100)))
            x.append(i / 100)
            y.append(r)
        # print(result)
        plt.figure(figsize=(10, 5))
        plt.grid(True)
        plt.plot(x, y, label=r'f(x)='+func)
        plt.xlabel(r'$x$', fontsize=14)
        plt.ylabel(r'$f(x)$', fontsize=14)
        plt.grid(True)
        plt.legend(loc='best', fontsize=12)
        plt.savefig('foo.png') #генерирует картинку
    # Обрабатываем исключение, которое мог вернуть модуль graph при запросе
    except Exception as e:
        return 'Неверный формат'


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Введите функцию: y=')

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def graph_message(*messages):
    for m in messages:
        chat_id = m.chat.id
        if m.content_type == 'text':
            text = m.text
            msgid = m.message_id
            graph(m.text)
            bot.send_chat_action(chat_id, 'upload_photo')
            img = open('foo.png', 'rb')
            bot.send_photo(chat_id, img, reply_to_message_id=msgid)
            img.close()
            bot.send_message(m.chat.id, 'Введите функцию: y=')


bot.polling(none_stop=True, interval=0)