import os
import telebot

import re

def parse (message):
    
    parsed = parser.findall(message)
    
    orders = []
    params = numbers, titles, quanitities, prices, addresses, phone_numbers, names, statuses = tuple(list() for i in range(8))
    paramNames = "Номер заказа", "Наименование продукта", "Кол-во", "Цена", "Адрес", "Тел. номер", "ФИО заказчика", "Статус заказа"
    
    errors = []
    
    for order in parsed:
        if len(order) == 8:
            orders.append(dict(zip(paramNames, order)))
            for i in range(8):
                params[i].append(order[i])
        else:
            errors.append(order[0])
        
    return orders, errors, params

bot = telebot.TeleBot("Orders Parser")

parser = re.compile("(\d+)(?:\s*?[^\.\s]*?[\.\s]+)?((?:\S+\s)+?)(\d+(?:ta|та|dona|дона|nafar|нафар)?)?\s?\n?((?:(?:\d+|\s)+)(?:ming|минг|млн|mln|K|k|К/к)?)(?:\.\s?\n?|\s?\n?)((?:.|\n)+?)(\+[\d ]+)\s?\n?([^\n✅❌]+)(✅|❌)")

@bot.message_handler(commands = ["parse"])
def parse_reply (input):
    orders, errors, params = parse(message[6:])
    bot.reply_to(input, "Результат парсинга:")
    for order in orders:
        bot.send_message(input, "Заказ №" + order[0])
        for i in range(1, 8) in order:
            bot.send_message(input, + order[i])
        bot.send_message(input, "____________________")




test_string = """vodiy zakaz:
15-zakaz 5⃣litr 10ta 180ming
Farg‘ona viloyati kirgili tabasum 31dom 
Muhabbat opa
+998931265766
😍❌

17-заказ.5⃣литр 10та 162 000.Фаргона вилояти.Киргили.Хувайдо махалла.Кадирдон 98.Шохиста.
+99893 3719676
+99898 2767877
Насиба🌺✅

18-заказ.5⃣литр 10та 162 000.Андидон шахар.Ху́жаобод тумани.Зиёкор м/ф/й.Бахрин ку́часи 90-уй.Зулхумор опа.
+99891 6017225
+99890 0606205
Насиба🌺❗️10литлидан бу́са оламан 5литрли у́рнига дидила.✅

20-заказ.5⃣литр 10та 162 000.Андижон вилояти.Андижон тумани.Телевизионний ку́ча.Лолапа.ар:2-поликлиника.
+99890 2176339
+99890 2172015
Насиба🌺✅

21-заказ.5⃣литр 10та 162 000.Andijon viloyati.Qorgontepa tumani. 
+99899 7215313
Насиба🌺✅"""