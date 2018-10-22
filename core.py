from utility import *

class player:
    id = 0
    x = 0
    y = 0
    bullets = 1 
    def __init__(self, x):
        self.id = x
        
class core:
    bot = None
    players = []
    cnt = 0
    step = 0
    
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
        if p.x + dx < 6 and p.y + dy < 6 and p.x + dx >= 0 and p.y + dy >= 0:
            self.bot.send_message(cur_id, "Well done!")
            sent_message(self.bot, cur_id, self.players, message.chat.first_name + " went " + txt + "!")
            p.x += dx
            p.y += dy
        else:
            self.bot.send_message(cur_id, "There is a wall!")
            sent_message(self.bot, cur_id, self.players, message.chat.first_name + " went " + txt + "! But there is a wall.")
        self.step = (self.step + 1) % self.cnt
