import telebot
from telebot import apihelper
import server

apihelper.proxy = {'https':'socks5://94.130.211.41:1080', 'http':'socks5://94.130.211.41:1080'}

token = "649733112:AAEK-BgclHseZVIGPVKG6BEU05zxVHcZcVE"

bot = telebot.TeleBot(token)

tag = 0

class human:
    id = 0
    group_name = ""
    r = False
    t = ""
    name_pass_c = False
    name_pass_j = False
    kick_name = False
    def __init__(self, x, y):
        self.t = y
        self.id = x

class table:
    leader = 0
    password = ""
    people = set()
    r = set()
    def __init__(self, x, y):
        self.password = x
        self.leader = y

users = dict()
tables = dict()

@bot.message_handler(commands=["start"])
def start(message):
    server.start(message)

@bot.message_handler(commands=["create"])
def create(message)
    server.create(message)

@bot.message_handler(commands=["join"])
def join(message):
    server.join(message)

@bot.message_handler(commands=["disconnect"])
def disconnect(message):
    server.disconnect(message)

@bot.message_handler(commands=["ready"])
def ready(message):
    server.ready(message)

@bot.message_handler(commands=["not_ready"])
def not_ready(message):
    server.not_ready(message)

@bot.message_handler(commands=["kick"])
def kick(message):        
    server.kick(message)

@bot.message_handler(content_types=["text"])
def on_text(message):
    server.on_text(message)

if __name__ == "__main__":
    bot.polling(none_stop=True)