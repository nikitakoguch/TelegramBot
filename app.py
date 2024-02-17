import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    welcome = f"Привет,{message.chat.username}😊\nЧтобы начать работу введите команду в формате:\n<имя валюты>\n\
<в какую валюту перевести>\
<количество переводимой валюты>\n\nВажно: все значения вводятся через пробел и валюты с маленькой буквы!\n\n\
Посмотреть список доступных валют: /values\nP.S. Если ты забудешь как пользоваться ботом, ты всегда сможешь\n\
прочитать инструкцию с помощью команды: /help"
    bot.reply_to(message, welcome) 
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в формате:\n<имя валюты>\n\
<в какую валюту перевести>\n\
<количество переводимой валюты>\nПосмотреть список доступных валют: /values\n\n\nВажно: все значения вводятся через пробел и валюты с маленькой буквы!\n'
    bot.reply_to(message, text)
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Должно быть 3 параметра!\nОзнакомьтесь с инструкцией ещё раз с помощью команды /help')
        quote, base, amount = values
        result = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}') 
       
    else:
        text = f'Цена {amount} {quote} в {base} - {result}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)