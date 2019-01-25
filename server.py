import telebot
from telebot import apihelper
import server
from utility import *
from core import *

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

class serv:
    users = dict()
    tables = dict()
    marks = dict()
    tag = 0
    bot = None

    def __init__(self, bot):
        self.bot = bot
        self.tag = 1

    def start(self, message):
        cur_id = message.chat.id
        self.users[cur_id] = human(cur_id, "#" + ("%04d" % self.tag))
        self.marks["#" + ("%04d" % self.tag)] = cur_id #moe yvojenie
        self.tag += 1
        sent_message(self.bot, -1, [cur_id], "You are in!") 

    def create(self, message):
        cur_id = message.chat.id
        if self.users[cur_id].group_name != "":
            self.bot.send_message(cur_id, "Sorry, you are already in table.")
            return
        else:
            self.bot.send_message(cur_id, "Well! Let's choose a name and password for your table.")
            self.users[cur_id].name_pass_c = True

    def join(self, message):
        cur_id = message.chat.id
        if self.users[cur_id].group_name != "":
            self.bot.send_message(cur_id, "Sorry, you are already in table.")
            return
        else:
            self.bot.send_message(cur_id, "Good! Enter name and password to join the table.")
            self.users[cur_id].name_pass_j = True

    def disconnect(self, message):
        cur_id = message.chat.id
        if self.users[cur_id].group_name != "":
            cur_user = self.users[cur_id]
            cur_table = self.tables[cur_user.group_name]
            sent_message(self.bot, cur_id, cur_table.people, message.chat.first_name + cur_user.t + ' leaved table "' + cur_user.group_name + '".')
            cur_table[cur_user.group_name].people.discard(cur_id)
            cur_table.tags.discard(cur_user.t)
            cur_user.group_name = ""
            self.bot.send_message(cur_id, "Fine! You leaved this table.")
        else:
            self.bot.send_message(cur_id, "Sorry, you are already not in table.")

    def ready(self, message):
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
            self.bot.send_message(cur_id, 'Great! You are ready to play.')
            cur_user.r = True
            cur_table.r.add(message.chat.id)
            if len(cur_table.r) == len(cur_table.people):
                sent_message(self.bot, -1, cur_table.r, "Ready! Set! GO!")
                cur_table.game = True                
                cur_table.game_core = core(self.bot, len(cur_table.r), cur_table.people)

    def not_ready(self, message):
        cur_id = message.chat.id
        cur_user = self.users[cur_id]
        if cur_user.group_name == "" :
            self.bot.send_message(cur_id, 'Sorry, you are not in table.')
            return
        elif cur_user.r:
            cur_table = self.tables[cur_user.group_name]
            sent_message(self.bot, cur_id, cur_table.people, message.chat.first_name + cur_user.t + ' is ready to play.')
            self.bot.send_message(message.chat.id, 'Exellent! You are not ready to play.')
            cur_user.r = False
            cur_table.r.discard(cur_id)
        else:
            self.bot.send_message(cur_id, 'You are not ready.')
            return

    def kick(self, message):
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

    def on_text(self, message):
        cur_id = message.chat.id
        cur_user = self.users[cur_id]
        if cur_user.name_pass_c:
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
                self.bot.send_message(cur_id, 'My respect! You managed to create a table "' + np[0] + '".')
                cur_user.name_pass_c = False
        elif self.users[message.chat.id].name_pass_j:
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
                self.bot.send_message(cur_id, 'Congratulations! You joined a table "' + np[0] + '".')
                sent_message(self.bot, cur_id, self.tables[cur_user.group_name].people, message.chat.first_name + ' joined chat "' + np[0] + '".')
                self.users[cur_id].name_pass_j = False
        elif self.users[cur_id].kick_tag:
            kt = message
            cur_table = self.tables[cur_user.group_name]
            if kt in cur_table.tags:
                cur_table.people.discard(self.marks[kt])
                cur_table.tags.discard(kt)
                sent_message(self.bot, cur_id, cur_table.people, kt + 'was kiked.')
            else:
                self.bot.send_message(cur_id, "Sorry, there are no players with this tag.")
        elif self.tables[cur_user.group_name].game:
            self.tables[cur_user.group_name].game_core.walk(message)
        else:
            if cur_user.group_name == "":
                self.bot.send_message(cur_id, "Write /create to make your own table. \nWrite /join to connect to table. \nWrite /disconnect to leave the table.")
            else:
                sent_message(self.bot, cur_id, self.tables[cur_user.group_name].people, message.chat.first_name + ' said "' + message.text + '"')
