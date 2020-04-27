# Штука дл рассылкисообщения (и клавиатуры) группе пользователей
def sent_message(bot, who, lst, mes, keyboard=False):
    for i in lst:
        if i != who:
            if keyboard:
                bot.send_message(i, mes, reply_markup=keyboard)
            else:
                bot.send_message(i, mes)