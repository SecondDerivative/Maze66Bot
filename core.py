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
        p = self.players[step]
        if message.txt == "Up": dx, dy = 0, -1
        elif message.txt == "Down": dx, dy = 0, 1
        elif message.txt == "Right": dx, dy = 1, 0
        elif message.txt == "Left": dx, dy = -1, 0
        else: self.bot.send_message(message.chat.id, "Sorry, this is an incorrect input form. Try again.")
        if p.x + dx < 6 and p.y + dy < 6 and p.x + dx >= 0 and p.y + dy >= 0:
            self.bot.send_message(message.chat.id, "Well done!")
            sent_message(self.bot, message.chat.id, players, message.chat.first_name + " went " + message.txt + "!")
            p.x += dx
            p.y += dy
        else:
            self.bot.send_message(message.chat.id, "There is a wall!")
            sent_message(self.bot, message.chat.id, players, message.chat.first_name + " went " + message.txt + "! But there is a wall.")
        step = (step + 1) % cnt
