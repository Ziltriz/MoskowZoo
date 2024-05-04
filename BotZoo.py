import telebot
from config import TOKEN
from utilits import ZooQuiz
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def process_start_command(message: telebot.types.Message):
    text = (f' Привет, {message.from_user.first_name}! \n '
            ' Я манул Тимофей из Московского зоопарка.\n'
            ' Я очень люблю играть в викторины и предлагаю тебе тоже попробовать! \n '
            ' Я кстати манул (как неожиданно 🙀🙀🙀🙀🙀🙀)! \n'
            ' Ну ладно скорее жми на /play \n'
            '\n'
            ' Если тебе нужна какая-либо помощь или дополнительная информация жми на /help ')
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    pass

@bot.message_handler(['play'])
def play(message: telebot.types.Message):
    text = 'Отлично давай по играем! \n'
    bot.send_message(message.from_user.id, text)
    zq = ZooQuiz()
    for i in zq.questions:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton(i['answers'][0])
        btn2 = telebot.types.KeyboardButton(i['answers'][1])
        btn3 = telebot.types.KeyboardButton(i['answers'][2])
        btn4 = telebot.types.KeyboardButton(i['answers'][3])
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, i['questions'], reply_markup=markup)



bot.polling()