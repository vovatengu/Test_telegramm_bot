from telebot import TeleBot,types
from mydec import JsonFileConfigIO
BOT_TOKEN = open('.env.txt','r').read().replace("\n","")
bot = TeleBot(BOT_TOKEN)

# def analytics(func: callable):
#     total_messages = 0
#     users = set()
#     total_users = 0

#     def analytics_wrapper(message):
#         nonlocal total_messages, total_users
#         total_messages += 1

#         if message.chat.id not in users:
#             users.add(message.chat.id)
#             total_users += 1
        
#         print(
#             "New message:", message.text,
#             "Total message:", total_messages,
#             "Unique users" , total_users
#         )
#         return func (message)
    
#     return analytics_wrapper
users = set()
@bot.message_handler(commands=['start'])
# @analytics
def menu(message):    

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items1 = types.KeyboardButton('Кнопка Пустая')
    items2 = types.KeyboardButton('Кнопка Статистика')

    markup.add(items1,items2)

    bot.send_message (message.chat.id,"Привет".format(message.from_user),reply_markup=markup)
    
    if message.chat.id not in users:
        users.add(message.chat.id)
        key_ref= parser(message.text)
        print(key_ref) # ключ
        users_ref = JsonFileConfigIO('users.json')
        dict_ref = users_ref.read() #словарь
        print(dict_ref)
        print(list(dict_ref.keys()))
        if key_ref is not None and key_ref in list(dict_ref.keys()):
            dict_ref[key_ref] = dict_ref.get(key_ref) + 1
        else:
            dict_ref["tg"] = dict_ref["tg"] + 1
        print(dict_ref)
        users_ref.write(dict_ref)
        print(users)
        

@bot.message_handler(content_types=['text'])
# @analytics
def on_message(message):
    if message.text == 'Кнопка Статистика':
        bot.send_message(message.chat.id, 'Ваша статитика инвайтов:' + str(JsonFileConfigIO('users.json').read()))
    else:
        bot.send_message(message.chat.id, f"Вы написали: {message.text}")

def parser( arg:str):
    try:
        name = str(arg.split(" ")[1])
        return name
    except IndexError:
        print('Ссылка из тг')   

if __name__ == '__main__':
    bot.polling()