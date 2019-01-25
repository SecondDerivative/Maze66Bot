from utility import *
from gen import *
import random

class player:
    id = 0
    x = 0
    y = 0
    key = False
    def __init__(self, x):
        self.id = x

class walls:
    ver = []
    hor = []
    def __init__(self, x, y):
        self.hor = x
        self.ver = y
        
class core:
    bot = None
    players = []
    cnt = 0
    step = 0
    key = [0, 0]
    door = [0, 0]
    maze = None

    def __init__(self, x, y, users):
        self.bot = x
        self.cnt = y
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
        self.key = [random.randint(0, 5), random.randint(0, 5)]
        while self.key == self.door:
            self.key = [random.randint(0, 5), random.randint(0, 5)]
        hor = [[False] * 5 for _ in range(6)]
        ver = [[False] * 5 for _ in range(6)]
        generate(hor, ver, 6, 6)
        self.maze = walls(hor, ver)
        for i in users:
            self.players.append(player(i))

    def walk(self, message):
        p = self.players[self.step]
        sent_message(self.bot, -1, self.players, message.chat.first_name + " is walking now.")
        cur_id = message.chat.id
        txt = message.text.lower()
        if cur_id != p.id:
            self.bot.send_message(cur_id, "Ow, it's not your turn.")
        else:
            if txt == "up": dx, dy = 0, -1
            elif txt == "down": dx, dy = 0, 1
            elif txt == "right": dx, dy = 1, 0
            elif txt == "left": dx, dy = -1, 0
            else: 
                self.bot.send_message(cur_id, "Sorry, this is an incorrect input form. Try again.")
                return
            if ((p.x + dx < 6 and p.y + dy < 6 and p.x + dx >= 0 and p.y + dy >= 0) and
            ((dx == 0 and self.maze.hor[p.x][(p.y * 2 + dy) // 2]) or (dy == 0 and self.maze.ver[p.y][(p.x * 2 + dx) // 2]))):
                self.bot.send_message(cur_id, "Well done!")
                sent_message(self.bot, cur_id, self.players, message.chat.first_name + " went " + txt + "!")
                p.x += dx
                p.y += dy
                if p.x == self.key[0] and p.y == self.key[1]:
                    p.key = True
                    self.bot.send_message(cur_id, "WoW! You have got a key!")
                    sent_message(self.bot, cur_id, self.players, message.chat.first_name + " went " + txt + " and got a key!")
                elif p.x == self.door[0] and p.y == self.door[1] and p.key:
                    self.bot.send_message(cur_id, "Congratulations! You are the winner!")
                    sent_message(self.bot, cur_id, self.players, message.chat.first_name + " went " + txt + " and won the game!")
                    return
            else:
                self.bot.send_message(cur_id, "There is a wall!")
                sent_message(self.bot, cur_id, self.players, message.chat.first_name + " went " + txt + "! But there is a wall.")
            self.step = (self.step + 1) % self.cnt

# (p.y * 2 + dy) // 2 - нахождение стены (типа если dy == -1, то лажа иначе (возьми (1;1) и (6;6) клетки и рассмотри другие формулы, если не веришь))
# True - ты пройдёшь, False - ТЫ НЕ ПРОЙДЁШЬ!!!!!