from utility import *
from gen import *

class player:
    id = 0
    x = 0
    y = 0
    bullets = 1 
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
    maze = walls(gen.hor, gen.ver)
    
    def __init__(self, x, y, users):
        self.bot = x
        self.cnt = y
        for i in users:
            self.players.append(player(i))

    def walk(self, message):
        p = self.players[self.step]
        cur_id = message.chat.id
        txt = message.text
        if txt == "Up": dx, dy = 0, -1
        elif txt == "Down": dx, dy = 0, 1
        elif txt == "Right": dx, dy = 1, 0
        elif txt == "Left": dx, dy = -1, 0
        else: self.bot.send_message(cur_id, "Sorry, this is an incorrect input form. Try again.")
        if ((p.x + dx < 6 and p.y + dy < 6 and p.x + dx >= 0 and p.y + dy >= 0) and
        ((dx == 0 and self.maze.hor[p.x][(p.y * 2 + dy) // 2]) or (dy == 0 and self.maze.ver[p.y][(p.x * 2 + dx) // 2]))):
            self.bot.send_message(cur_id, "Well done!")
            sent_message(self.bot, cur_id, self.players, message.chat.first_name + " went " + txt + "!")
            p.x += dx
            p.y += dy
        else:
            self.bot.send_message(cur_id, "There is a wall!")
            sent_message(self.bot, cur_id, self.players, message.chat.first_name + " went " + txt + "! But there is a wall.")
        self.step = (self.step + 1) % self.cnt

# (p.y * 2 + dy) // 2 - нахождение стены (типа если dy == -1, то лажа иначе (возьми (1;1) и (6;6) клетки и рассмотри другие формулы, если не веришь))
# True - ты пройдёшь, False - ТЫ НЕ ПРОЙДЁШЬ!!!!!