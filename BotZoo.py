import telebot
from config import TOKEN
from utilits import ZooQuiz
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def process_start_command(message: telebot.types.Message):
    bot.set_state(message.chat.id , state='start')
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
    text = 'Отлично давай по играем! \n'
    bot.send_message(message.from_user.id, text)
    user_state = bot.get_state(user_id=message.chat.id)
    if user_state == 'start':
        text = ' И так первый вопрос:'
        bot.send_message(message.from_user.id, text)
        bot.set_state(user_id=message.chat.id, state='question')
        display_question(message)
    elif user_state == 'question':
        display_question(message)

@bot.message_handler(content_types='text')
def display_question(message):
    if len(ZooQuiz.questions) != 0 and len(ZooQuiz.questions) > 0:
        question = ZooQuiz.questions[0]
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        answers_keys = list(question['answers'].keys())
        for j in answers_keys:
            btn = telebot.types.KeyboardButton(j)
            markup.add(btn)
        markup.add(telebot.types.KeyboardButton('Назад'))
        bot.send_message(message.from_user.id, question['questions'], reply_markup=markup)
        bot.set_state(user_id=message.chat.id, state='answer')
        check_answer(message)
    else:
        result(message)


def check_answer(message):
    question = ZooQuiz.questions[0]
    answer = message.text
    print(ZooQuiz.points, question['answers'].get(answer), answer)
    for i in list(question['answers'].keys()):
        if answer == i:
            ZooQuiz.points += question['answers'].get(answer)
            ZooQuiz.questions.pop(0)

def result(message):
    pass

bot.polling()