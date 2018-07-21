class serv:
    def start(message):
        users[message.chat.id] = human(message.chat.id)
        

    def create(message):
        if users[message.chat.id].group_name != "":
            bot.send_message(message.chat.id, "Sorry, you are already in table.")
            return
        else:
            bot.send_message(message.chat.id, "Well! Let's choose a name and password for your table.")
            users[message.chat.id].name_pass_c = True

    def join(message):
        if users[message.chat.id].group_name != "":
            bot.send_message(message.chat.id, "Sorry, you are already in table.")
            return
        else:
            bot.send_message(message.chat.id, "Good! Enter name and password to join the table.")
            users[message.chat.id].name_pass_j = True

    def disconnect(message):
        if users[message.chat.id].group_name != "":
            for i in tables[users[message.chat.id].group_name].people:
                    if i != message.chat.id:
                        bot.send_message(i, message.chat.first_name + ' leaved table "' + users[message.chat.id].group_name + '".')
            tables[users[message.chat.id].group_name].people.discard(message.chat.id)
            users[message.chat.id].group_name = ""
            bot.send_message(message.chat.id, "Fine! You leaved this table.")
        else:
            bot.send_message(message.chat.id, "Sorry, you are already not in table.")

    def ready(message):
        if users[message.chat.id].group_name == "" :
            bot.send_message(message.chat.id, 'Sorry, you are not in table.')
            return
        elif users[message.chat.id].r:
            bot.send_message(message.chat.id, 'You are ready.')
            return
        else:
            for i in tables[users[message.chat.id].group_name].people:
                    if i != message.chat.id:
                        bot.send_message(i, message.chat.first_name + ' is ready to play.')
            bot.send_message(message.chat.id, 'Great! You are ready to play.')
            users[message.chat.id].r = True
            tables[np[0]].r.add(message.chat.id)

    def not_ready(message):
        if users[message.chat.id].group_name == "" :
            bot.send_message(message.chat.id, 'Sorry, you are not in table.')
            return
        elif users[message.chat.id].r:
            for i in tables[users[message.chat.id].group_name].people:
                    if i != message.chat.id:
                        bot.send_message(i, message.chat.first_name + ' is ready to play.')
            bot.send_message(message.chat.id, 'Exellent! You are not ready to play.')
            users[message.chat.id].r = False
            tables[users[message.chat.id].group_name].r.discard(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'You are not ready.')
            return

    def kick(message):        
        if message.text.id == tables[users[message.chat.id].group_name].leader:
            bot.send_message(message.chat.id, "Well! Please, write players tag to kick him from your table.")
            users[message.chat.id].kick_name = True
        else:
            bot.send_message(message.chat.id, "Sorry, you are not leader of this table.")
    
    def tag_list(message):
        for 

    def on_text(message):
        if users[message.chat.id].name_pass_c:
            np = message.text.split()
            if len(np) != 2:
                bot.send_message(message.chat.id, "Sorry, this is an incorrect input form. Try again.")
                return
            elif np[0] in tables:
                bot.send_message(message.chat.id, "Sorry, this name is already taken. Try again.")
                return
            else:
                tables[np[0]] = table(np[1], message.chat.id)
                users[message.chat.id].group_name = np[0]
                tables[np[0]].people.add(message.chat.id)
                bot.send_message(message.chat.id, 'My respect! You managed to create a table "' + users[message.chat.id].group_name + '".')
                users[message.chat.id].name_pass_c = False
        elif users[message.chat.id].name_pass_j:
            np = message.text.split()
            if len(np) != 2:
                bot.send_message(message.chat.id, "Sorry, this is an incorrect input form. Try again.")
                return
            elif np[0] not in tables or tables[np[0]].password != np[1]:
                bot.send_message(message.chat.id, "Sorry, there is incorrect name or password.")
                users[message.chat.id].name_pass_j = False
                return
            else:
                users[message.chat.id].group_name = np[0]
                tables[np[0]].people.add(message.chat.id)
                bot.send_message(message.chat.id, 'Congratulations! You joined a table "' + users[message.chat.id].group_name + '".')
                for i in tables[users[message.chat.id].group_name].people:
                    if i != message.chat.id:
                        bot.send_message(i, message.chat.first_name + ' joined chat "' + users[message.chat.id].group_name + '".')
                users[message.chat.id].name_pass_j = False
        elif users[message.chat.id].kick_name:
            
        else:
            if users[message.chat.id].group_name == "":
                bot.send_message(message.chat.id, "Write /create to make your own table. \nWrite /join to connect to table. \nWrite /disconnect to leave the table.")
            else:
                for i in tables[users[message.chat.id].group_name].people:
                    if i != message.chat.id:
                        bot.send_message(i, message.chat.first_name + ' said "' + message.text + '"')