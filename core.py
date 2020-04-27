from utility import *
from gen import *
import random, sqlite3
import telebot

class player:
    # Класс игрока
    id = 0
    x = 0
    y = 0
    key = False
    def __init__(self, ID, xpos, ypos):
        self.id = ID
        self.x = xpos
        self.y = ypos
        self.key = False
        self.bullets = 3

class walls:
    # Класс стен
    ver = []
    hor = []
    def __init__(self, x, y):
        self.hor = x
        self.ver = y
        
class core:
    # Игровое ядро
    bot = None
    players = []
    cnt = 0
    step = 0
    users = set()
    key = [0, 0]
    door = [0, 0]
    maze = None

    # Необходимые клавиатуры
    keyboard2 = telebot.types.ReplyKeyboardMarkup(False, True)
    keyboard2.row('/disconnect', '/ready' , '/kick')

    keyboard4 = telebot.types.ReplyKeyboardMarkup(False, True)
    keyboard4.row('left', 'up', 'down', 'right')

    keyboard5 = telebot.types.ReplyKeyboardMarkup(False, True)
    keyboard5.row('shoot', 'walk')

    def __init__(self, x, y, users, CB):
        self.bot = x
        self.cnt = y
        self.end_CB = CB
        self.users = users
        # Госпиталь
        self.hospital = [random.randint(1, 4), random.randint(1, 4)]
        # Порталы
        self.portals = [[0, 0], [0, 0], [0, 0]]
        for i in range(3):
            self.portals[i] = [random.randint(0, 5), random.randint(0, 5)]
        # Дверь
        if random.randint(0, 1):
            if random.randint(0, 1):
                self.door = [0, random.randint(0,5)]
            else:
                self.door = [5, random.randint(0,5)]
        else:
            if random.randint(0, 1):
                self.door = [random.randint(0, 5), 0]
            else:
                self.door = [random.randint(0, 5), 5]
        # Ключ
        self.key = [random.randint(0, 5), random.randint(0, 5)]
        while self.key == self.door or self.key == self.hospital or self.key in self.portals:
            self.key = [random.randint(0, 5), random.randint(0, 5)]
        # Стены
        hor = [[False] * 5 for _ in range(6)]
        ver = [[False] * 5 for _ in range(6)]
        # Если не получается взять стены из бд, то генерируем их сами
        try:
            name_db = 'data.db'
            con = sqlite3.connect(name_db)
            cur = con.cursor()
            L = len(cur.execute("Select id FROM data WHERE id > 0").fetchall())
            num = random.randint(0, L)
            hor = cur.execute("Select hor FROM data WHERE id = ?",(num,)).fetchone()
            ver = cur.execute("Select ver FROM data WHERE id = ?",(num,)).fetchone()
            self.maze = walls(hor, ver)
        except Exception:
            generate(hor, ver, 6, 6)
            self.maze = walls(hor, ver)
        # Раскидываем игроков по полю, чтобы они не попали в ключ
        posx = list(filter(lambda i: i != self.key[0], [0, 1, 2, 3, 4, 5]))
        posy = list(filter(lambda i: i != self.key[1], [0, 1, 2, 3, 4, 5]))
        for i in users:
            self.players.append(player(i, random.choice(posx), random.choice(posy)))
    
    def walk(self, message):
        # Функци хода
        p = self.players[self.step]
        cur_id = message.chat.id
        txt = message.text.lower()
        if cur_id != p.id:
            # Проверем ход ли это пишущего игрока
            self.bot.send_message(cur_id, "Oi, it's not your turn.")
            return
        elif txt in ['walk', 'shoot']:
            # Даём выбор ходить или стрелть и сохранем действие
            if txt == 'shoot' and p.bullets == 0:
                 self.bot.send_message(cur_id, "You have no bullets")
                 return
            self.action = txt
            self.bot.send_message(cur_id, "You chose to " + txt, reply_markup=core.keyboard4)
            return
        elif self.action == 'walk':
            # Если действие хода, то читаем направление и ходим, обработка всех объектов, которые можно встретить, сбрасываем флаг действия
            sent_message(self.bot, -1, self.users, message.chat.first_name + " is walking now.")
            if txt == "up": dx, dy = 0, -1
            elif txt == "down": dx, dy = 0, 1
            elif txt == "right": dx, dy = 1, 0
            elif txt == "left": dx, dy = -1, 0
            else: 
                self.bot.send_message(cur_id, "Sorry, this is an incorrect input form. Try again.")
                return
            if ((p.x + dx < 6 and p.y + dy < 6 and p.x + dx >= 0 and p.y + dy >= 0) and
            ((dx == 0 and self.maze.hor[p.x][(p.y * 2 + dy) // 2]) or (dy == 0 and self.maze.ver[p.y][(p.x * 2 + dx) // 2]))):
                self.bot.send_message(cur_id, "Well done!", reply_markup=core.keyboard5)
                sent_message(self.bot, cur_id, self.users, message.chat.first_name + " went " + txt + "!")
                p.x += dx
                p.y += dy
                if p.x == self.key[0] and p.y == self.key[1]:
                    p.key = True
                    self.bot.send_message(cur_id, "WoW! You have got a key!", reply_markup=core.keyboard5)
                    sent_message(self.bot, cur_id, self.users, message.chat.first_name + " went " + txt + " and got the key!")
                elif p.x == self.door[0] and p.y == self.door[1] and p.key:
                    self.bot.send_message(cur_id, "Congratulations! You are the winner!")
                    sent_message(self.bot, cur_id, self.users, message.chat.first_name + " went " + txt + " and won the game!")
                    self.end_CB()
                    sent_message(self.bot, -1, self.users, "Game has been ended. Oi-oi! Everybody aren't ready.", keyboard=core.keyboard2)
                    return
                elif [p.x, p.y] in self.portals:
                    p.x, p.y = self.portals[(self.portals.index([p.x, p.y]) + 1) % 3]
                    self.bot.send_message(cur_id, "Wsooh! You used the portal.", reply_markup=core.keyboard5)
                    sent_message(self.bot, cur_id, self.users, message.chat.first_name + " went " + txt + " and walk into the portal!")
            else:
                self.bot.send_message(cur_id, "There is a wall!", reply_markup=core.keyboard5)
                sent_message(self.bot, cur_id, self.users, message.chat.first_name + " went " + txt + "! But there is a wall.")
            self.step = (self.step + 1) % self.cnt
            self.action = False
        elif self.action == 'shoot':
            # Если есть пули - выбираем направление и делаем выстрел, отправлем всех убитых в госпиталь, сбрасываем флаг действия
            p.bullets -= 1
            sent_message(self.bot, -1, self.users, message.chat.first_name + " is shooting now.")
            if txt == "up":
                kill_streak = 0
                for i in self.players:
                    if i.x == p.x and i.y < p.y:
                        self.bot.send_message(i.id, "You caught the bullet. You are in the hospital now.")
                        i.x, i.y = self.hospital
                        kill_streak += 1
                self.bot.send_message(cur_id, "You have killed " + str(kill_streak) + " people.", reply_markup=core.keyboard5)
            elif txt == "down":
                kill_streak = 0
                for i in self.players:
                    if i.x == p.x and i.y > p.y:
                        self.bot.send_message(i.id, "You caught the bullet. You are in the hospital now.")
                        i.x, i.y = self.hospital
                        kill_streak += 1
                self.bot.send_message(cur_id, "You have killed " + kill_streak + " people.", reply_markup=core.keyboard5)
            elif txt == "right":
                kill_streak = 0
                for i in self.players:
                    if i.x > p.x and i.y == p.y:
                        self.bot.send_message(i.id, "You caught the bullet. You are in the hospital now.")
                        i.x, i.y = self.hospital
                        kill_streak += 1
                self.bot.send_message(cur_id, "You have killed " + kill_streak + " people.", reply_markup=core.keyboard5)
            elif txt == "left":
                kill_streak = 0
                for i in self.players:
                    if i.x < p.x and i.y == p.y:
                        self.bot.send_message(i.id, "You caught the bullet. You are in the hospital now.")
                        i.x, i.y = self.hospital
                        kill_streak += 1
                self.bot.send_message(cur_id, "You have killed " + kill_streak + " people.", reply_markup=core.keyboard5)
            else: 
                self.bot.send_message(cur_id, "Sorry, this is an incorrect input form. Try again.")
                return
            self.step = (self.step + 1) % self.cnt
            self.action = False
        else:
            # Если сообщение непонято, то просим ввести ещё раз
            self.bot.send_message(cur_id, "Sorry, this is an incorrect input form. Try again.")
            return