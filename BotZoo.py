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

@bot.message_handler(commands=['play'])
def play(message):
    text = ('Отлично давай по играем! \n'
            'Жми на кнопку начнем для начала!')
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(telebot.types.KeyboardButton('Начнем!'))
    msg = bot.send_message(message.from_user.id, text=text, reply_markup=markup)
    bot.register_next_step_handler(msg, display_question)
def display_question(message):
    points = ZooQuiz.points
    if message.text == 'Начнем!':
        text = ' И так первый вопрос:'
        bot.send_message(message.from_user.id, text)
    if len(ZooQuiz.questions) != 0 and len(ZooQuiz.questions) > 0:
        question = ZooQuiz.questions[0]
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        answers_keys = list(question['answers'].keys())
        for j in answers_keys:
            btn = telebot.types.KeyboardButton(j)
            markup.add(btn)
        markup.add(telebot.types.KeyboardButton('Назад'))
        msg = bot.send_message(message.from_user.id, question['questions'], reply_markup=markup)
        bot.register_next_step_handler(msg, check_answer)
    else:
        result(message, points)
    

def check_answer(message):
    question = ZooQuiz.questions[0]
    answer = message.text
    if len(ZooQuiz.questions) != 0:
        for i in list(question['answers'].keys()):
            print(message.text, i)
            if answer == i:
                ZooQuiz.points += question['answers'].get(answer)
                ZooQuiz.questions.pop(0)
                display_question(message)
                break


def result(message, points):
    if points > 10:
        points = 10
    animals = ZooQuiz.animals
    for keys, value in animals.items():
        if value == points:
            bot.send_message(message.chat.id, f'Поздравляю твое тотемное животное это - {keys}')



bot.polling()