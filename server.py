import telebot
from telebot import apihelper
import server
from utility import *
from core import *


# Класс человека
class human:
    id = 0
    group_name = ""
    r = False
    t = ""
    name_pass_c = False
    name_pass_j = False
    kick_tag = False
    def __init__(self, x, y):
        self.t = y
        self.id = x


# Класс игрового стола
class table:
    leader = 0
    game_core = None
    game = False
    password = ""
    tags = set()
    people = set()
    r = set()
    def __init__(self, x, y):
        self.password = x
        self.leader = y


# Класс сервера
class serv:
    users = dict()
    tables = dict()
    marks = dict()
    tag = 0
    bot = None
     
    # Задаём все возможные дл использования клавиатуры
    keyboard1 = telebot.types.ReplyKeyboardMarkup(False, True)
    keyboard1.row('/create', '/join')

    keyboard2 = telebot.types.ReplyKeyboardMarkup(False, True)
    keyboard2.row('/disconnect', '/ready' , '/kick')

    keyboard3 = telebot.types.ReplyKeyboardMarkup(False, True)
    keyboard3.row('/disconnect', '/not_ready', '/kick')

    keyboard4 = telebot.types.ReplyKeyboardMarkup(False, True)
    keyboard4.row('left', 'up', 'down', 'right')

    keyboard5 = telebot.types.ReplyKeyboardMarkup(False, True)
    keyboard5.row('shoot', 'walk')

    def __init__(self, bot):
        self.bot = bot
        self.tag = 1

    # Тут тела всех команд бота
    def start(self, message):
        # Регистраци в боте
        cur_id = message.chat.id
        self.users[cur_id] = human(cur_id, "#" + ("%04d" % self.tag))
        self.marks["#" + ("%04d" % self.tag)] = cur_id #moe yvojenie
        self.tag += 1
        sent_message(self.bot, -1, [cur_id], "You are in!", serv.keyboard1) 

    def create(self, message):
        # Создать игровой стол
        cur_id = message.chat.id
        if self.users[cur_id].group_name != "":
            self.bot.send_message(cur_id, "Sorry, you are already in table.")
            return
        else:
            self.bot.send_message(cur_id, "Well! Let's choose a name and password for your table.")
            self.users[cur_id].name_pass_c = True

    def join(self, message):
        # Вступить в игровой стол
        cur_id = message.chat.id
        if self.users[cur_id].group_name != "":
            self.bot.send_message(cur_id, "Sorry, you are already in table.")
            return
        else:
            self.bot.send_message(cur_id, "Good! Enter name and password to join the table.")
            self.users[cur_id].name_pass_j = True

    def disconnect(self, message):
        # Отключиться от стола
        cur_id = message.chat.id
        if self.users[cur_id].group_name != "":
            cur_user = self.users[cur_id]
            cur_table = self.tables[cur_user.group_name]
            sent_message(self.bot, cur_id, cur_table.people, message.chat.first_name + cur_user.t + ' leaved table "' + cur_user.group_name + '".')
            cur_table.people.discard(cur_id)
            cur_table.tags.discard(cur_user.t)
            cur_user.group_name = ""
            self.bot.send_message(cur_id, "Fine! You leaved this table.", reply_markup=serv.keyboard1)
        else:
            self.bot.send_message(cur_id, "Sorry, you are already not in table.")

    def ready(self, message):
        # Готов к игре
        cur_id = message.chat.id
        cur_user = self.users[cur_id]
        if cur_user.group_name == "" :
            self.bot.send_message(cur_id, 'Sorry, you are not in table.')
            return
        elif cur_user.r:
            self.bot.send_message(cur_id, 'You are ready.')
            return
        else:
            cur_table = self.tables[cur_user.group_name]
            sent_message(self.bot, cur_id, cur_table.people, message.chat.first_name + cur_user.t + ' is ready to play.')
            self.bot.send_message(cur_id, 'Great! You are ready to play.', reply_markup=serv.keyboard3)
            cur_user.r = True
            cur_table.r.add(message.chat.id)
            if len(cur_table.r) == len(cur_table.people):

                def CB():
                    for i in cur_table.people:
                        self.users[i].r = False
                    cur_table.game = False
                    cur_table.r = set()

                sent_message(self.bot, -1, cur_table.r, "Ready! Set! GO!", serv.keyboard5)
                cur_table.game = True                
                cur_table.game_core = core(self.bot, len(cur_table.r), cur_table.people, CB)

    def not_ready(self, message):
        # Отменить готовность к игре
        cur_id = message.chat.id
        cur_user = self.users[cur_id]
        if cur_user.group_name == "" :
            self.bot.send_message(cur_id, 'Sorry, you are not in table.')
            return
        elif cur_user.r:
            cur_table = self.tables[cur_user.group_name]
            sent_message(self.bot, cur_id, cur_table.people, message.chat.first_name + cur_user.t + "isn't ready to play.")
            self.bot.send_message(message.chat.id, 'Exellent! You are not ready to play.', reply_markup=serv.keyboard2)
            cur_user.r = False
            cur_table.r.discard(cur_id)
        else:
            self.bot.send_message(cur_id, 'You are not ready.')
            return

    def kick(self, message):
        # Выкинуть из-за стола игрока (может только создатель)
        cur_id = message.chat.id
        cur_user = self.users[cur_id]
        if cur_user.group_name == "":
            self.bot.send_message(cur_id, "Sorry, you are not in table.")
            return
        elif cur_id == self.tables[cur_user.group_name].leader:
            self.bot.send_message(cur_id, 'Well! Please, write players tag to kick him from your table. For example "#' + cur_user.t + '"')
            cur_user.kick_tag = True
        else:
            self.bot.send_message(cur_id, "Sorry, you are not leader of this table.")
        
    
    def rules(self, message):
        # Вывести правила игры
        cur_id = message.chat.id
        self.bot.send_message(cur_id, """THE RULES OF MAZE
        You are in maze 6x6, but cant see it, so write 'up', 'down', 'right' or 'left' to move. You can move succsessful or meet the wall.
        Also there is a key and the door, you need to find the key and open the door to win.
        You can walk into portal to teleport to another one. There are 3 portals and each one teleport to the next. (0->1->2->0->...)
        You can shoot. The bullet fly through walls and kill everybody on its way. You have only 3 bullets.
        If you meet a bullet with your face, then you will go to the hospital. Its the constant place in the maze.""")


    def on_text(self, message):
        cur_id = message.chat.id
        cur_user = self.users[cur_id]
        if cur_user.name_pass_c:
            # Создание стола
            np = message.text.split()
            if len(np) != 2:
                self.bot.send_message(cur_id, "Sorry, this is an incorrect input form. Try again.")
                return
            elif np[0] in self.tables:
                self.bot.send_message(cur_id, "Sorry, this name is already taken. Try again.")
                return
            else:
                self.tables[np[0]] = table(np[1], cur_id)
                cur_user.group_name = np[0]
                self.tables[np[0]].people.add(cur_id)
                self.tables[np[0]].tags.add(cur_user.t)
                self.bot.send_message(cur_id, 'My respect! You managed to create a table "' + np[0] + '".', reply_markup=serv.keyboard2)
                cur_user.name_pass_c = False
        elif self.users[message.chat.id].name_pass_j:
            # Вступление в игру
            np = message.text.split()
            if len(np) != 2:
                self.bot.send_message(cur_id, "Sorry, this is an incorrect input form. Try again.")
                return
            elif np[0] not in self.tables or self.tables[np[0]].password != np[1]:
                self.bot.send_message(cur_id, "Sorry, there is incorrect name or password.")
                cur_user.name_pass_j = False
                return
            else:
                cur_user.group_name = np[0]
                self.tables[np[0]].people.add(cur_id)
                self.tables[np[0]].tags.add(cur_user.t)
                self.bot.send_message(cur_id, 'Congratulations! You joined a table "' + np[0] + '".', reply_markup=serv.keyboard2)
                sent_message(self.bot, cur_id, self.tables[cur_user.group_name].people, message.chat.first_name + ' joined chat "' + np[0] + '".')
                self.users[cur_id].name_pass_j = False
        elif self.users[cur_id].kick_tag:
            # Исключение игрока
            kt = message
            cur_table = self.tables[cur_user.group_name]
            if kt in cur_table.tags:
                cur_table.people.discard(self.marks[kt])
                cur_table.tags.discard(kt)
                sent_message(self.bot, cur_id, cur_table.people, kt + 'was kiked.')
            else:
                self.bot.send_message(cur_id, "Sorry, there are no players with this tag.")
        elif cur_user.group_name != '' and self.tables[cur_user.group_name].game:
            # Процесс хода в игре
            self.tables[cur_user.group_name].game_core.walk(message)
        else:
            # Написать сообщение
            if cur_user.group_name == "":
                self.bot.send_message(cur_id, "Write /create to make your own table. \nWrite /join to connect to table. \nWrite /disconnect to leave the table.")
            else:
                sent_message(self.bot, cur_id, self.tables[cur_user.group_name].people, message.chat.first_name + ' said "' + message.text + '"')
