import telebot
from telebot import apihelper
import server
import core

apihelper.proxy = {'https':'https://91.187.93.166:80'}

token = "649733112:AAEK-BgclHseZVIGPVKG6BEU05zxVHcZcVE"

bot = telebot.TeleBot(token)

main_server = server.serv(bot)

@bot.message_handler(commands=["start"])
def start(message):
    main_server.start(message)

@bot.message_handler(commands=["create"])
def create(message):
    main_server.create(message)

@bot.message_handler(commands=["join"])
def join(message):
    main_server.join(message)

@bot.message_handler(commands=["disconnect"])
def disconnect(message):
    main_server.disconnect(message)

@bot.message_handler(commands=["ready"])
def ready(message):
    main_server.ready(message)

@bot.message_handler(commands=["not_ready"])
def not_ready(message):
    main_server.not_ready(message)

@bot.message_handler(commands=["kick"])
def kick(message):        
    main_server.kick(message)

@bot.message_handler(content_types=["text"])
def on_text(message):
    main_server.on_text(message)

if __name__ == "__main__":
    bot.polling(none_stop=True)