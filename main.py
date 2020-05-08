import telebot
from telebot import apihelper
import server
import core


# Прописываем прокси и токен
apihelper.proxy = {'https':'https://149.28.154.226:8080'}
token = "649733112:AAEK-BgclHseZVIGPVKG6BEU05zxVHcZcVE"

# Заводим объект класса telebot.TeleBot
bot = telebot.TeleBot(token)

# Создаём сервер для бота
main_server = server.serv(bot)

# Прописываем все команды и ссылки на их ответы в сервере
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


@bot.message_handler(commands=["rules"])
def rules(message):        
    main_server.rules(message)


@bot.message_handler(content_types=["text"])
def on_text(message):
    main_server.on_text(message)


# Чтобы бот работал без остановки с самого запуска нужно прописать это
if __name__ == "__main__":
    bot.polling(none_stop=True)