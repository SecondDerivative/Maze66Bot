def sent_message(bot, who, lst, mes):
    for i in lst:
        if i != who:
            bot.send_message(i, mes)