import telebot
from telebot import apihelper
import server
from utility import *

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
        self.users[message.chat.id] = human(message.chat.id, "#" + ("%04d" % self.tag))
        self.marks["#" + ("%04d" % self.tag)] = message.chat.id
        self.tag += 1

    def create(self, message):
        if self.users[message.chat.id].group_name != "":
            self.bot.send_message(message.chat.id, "Sorry, you are already in table.")
            return
        else:
            self.bot.send_message(message.chat.id, "Well! Let's choose a name and password for your table.")
            self.users[message.chat.id].name_pass_c = True

    def join(self, message):
        if self.users[message.chat.id].group_name != "":
            self.bot.send_message(message.chat.id, "Sorry, you are already in table.")
            return
        else:
            self.bot.send_message(message.chat.id, "Good! Enter name and password to join the table.")
            self.users[message.chat.id].name_pass_j = True

    def disconnect(self, message):
        if self.users[message.chat.id].group_name != "":
            sent_message(self.bot, message.chat.id, self.tables[self.users[message.chat.id].group_name].people, message.chat.first_name + self.users[message.chat.id].t + ' leaved table "' + self.users[message.chat.id].group_name + '".')
            self.tables[self.users[message.chat.id].group_name].people.discard(message.chat.id)
            self.tables[self.users[message.chat.id].group_name].tags.discard(self.users[message.chat.id].t)
            self.users[message.chat.id].group_name = ""
            self.bot.send_message(message.chat.id, "Fine! You leaved this table.")
        else:
            self.bot.send_message(message.chat.id, "Sorry, you are already not in table.")

    def ready(self, message):
        if self.users[message.chat.id].group_name == "" :
            self.bot.send_message(message.chat.id, 'Sorry, you are not in table.')
            return
        elif self.users[message.chat.id].r:
            self.bot.send_message(message.chat.id, 'You are ready.')
            return
        else:
            sent_message(self.bot, message.chat.id, self.tables[self.users[message.chat.id].group_name].people, message.chat.first_name + self.users[message.chat.id].t + ' is ready to play.')
            self.bot.send_message(message.chat.id, 'Great! You are ready to play.')
            self.users[message.chat.id].r = True
            self.tables[self.users[message.chat.id].group_name].r.add(message.chat.id)

    def not_ready(self, message):
        if self.users[message.chat.id].group_name == "" :
            self.bot.send_message(message.chat.id, 'Sorry, you are not in table.')
            return
        elif self.users[message.chat.id].r:
            sent_message(self.bot, message.chat.id, self.tables[self.users[message.chat.id].group_name].people, message.chat.first_name + self.users[message.chat.id].t + ' is ready to play.')
            self.bot.send_message(message.chat.id, 'Exellent! You are not ready to play.')
            self.users[message.chat.id].r = False
            self.tables[self.users[message.chat.id].group_name].r.discard(message.chat.id)
        else:
            self.bot.send_message(message.chat.id, 'You are not ready.')
            return

    def kick(self, message):        
        if message.chat.id == self.tables[self.users[message.chat.id].group_name].leader:
            self.bot.send_message(message.chat.id, 'Well! Please, write players tag to kick him from your table. For example "#' + self.users[message.chat.id].t + '"')
            self.users[message.chat.id].kick_tag = True
        else:
            self.bot.send_message(message.chat.id, "Sorry, you are not leader of this table.")

    def on_text(self, message):
        if self.users[message.chat.id].name_pass_c:
            np = message.text.split()
            if len(np) != 2:
                self.bot.send_message(message.chat.id, "Sorry, this is an incorrect input form. Try again.")
                return
            elif np[0] in self.tables:
                self.bot.send_message(message.chat.id, "Sorry, this name is already taken. Try again.")
                return
            else:
                self.tables[np[0]] = table(np[1], message.chat.id)
                self.users[message.chat.id].group_name = np[0]
                self.tables[np[0]].people.add(message.chat.id)
                self.tables[np[0]].tags.add(self.users[message.chat.id].t)
                self.bot.send_message(message.chat.id, 'My respect! You managed to create a table "' + self.users[message.chat.id].group_name + '".')
                self.users[message.chat.id].name_pass_c = False
        elif self.users[message.chat.id].name_pass_j:
            np = message.text.split()
            if len(np) != 2:
                self.bot.send_message(message.chat.id, "Sorry, this is an incorrect input form. Try again.")
                return
            elif np[0] not in self.tables or self.tables[np[0]].password != np[1]:
                self.bot.send_message(message.chat.id, "Sorry, there is incorrect name or password.")
                self.users[message.chat.id].name_pass_j = False
                return
            else:
                self.users[message.chat.id].group_name = np[0]
                self.tables[np[0]].people.add(message.chat.id)
                self.tables[np[0]].tags.add(self.users[message.chat.id].t)
                self.bot.send_message(message.chat.id, 'Congratulations! You joined a table "' + self.users[message.chat.id].group_name + '".')
                sent_message(self.bot, message.chat.id, self.tables[self.users[message.chat.id].group_name].people, message.chat.first_name + ' joined chat "' + self.users[message.chat.id].group_name + '".')
                self.users[message.chat.id].name_pass_j = False
        elif self.users[message.chat.id].kick_tag:
            kt = message
            if kt in self.tables[self.users[message.chat.id].group_name].tags:
                self.tables[self.users[message.chat.id].group_name].people.discard(self.marks[kt])
                self.tables[self.users[message.chat.id].group_name].tags.discard(kt)
                sent_message(self.bot, message.chat.id, self.tables[self.users[message.chat.id].group_name].people, kt + 'was kiked.')
            else:
                self.bot.send_message(message.chat.id, "Sorry, there are no players with this tag.")
        else:
            if self.users[message.chat.id].group_name == "":
                self.bot.send_message(message.chat.id, "Write /create to make your own table. \nWrite /join to connect to table. \nWrite /disconnect to leave the table.")
            else:
                for i in self.tables[self.users[message.chat.id].group_name].people:
                    if i != message.chat.id:
                        self.bot.send_message(i, message.chat.first_name + ' said "' + message.text + '"')