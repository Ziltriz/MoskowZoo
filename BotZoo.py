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
def help(message):
    quiz_result = 'Квиз не пройден'
    contact_staff(message, quiz_result)

@bot.message_handler(commands=['play'])
def play(message):
    text = ('Отлично давай по играем! \n'
            'Жми на кнопку начнем для начала!')
    questions = ZooQuiz.questions.copy()
    ZooQuiz.points = 0
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(telebot.types.KeyboardButton('Начнем!'))
    msg = bot.send_message(message.from_user.id, text=text, reply_markup=markup)

    bot.register_next_step_handler(msg, display_question, questions)
def display_question(message, questions):

    if message.text == 'Начнем!':
        text = ' И так первый вопрос:'
        bot.send_message(message.from_user.id, text)
    if len(questions) != 0 and len(questions) > 0:
        question = questions[0]
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        answers_keys = list(question['answers'].keys())
        for j in answers_keys:
            btn = telebot.types.KeyboardButton(j)
            markup.add(btn)
        msg = bot.send_message(message.from_user.id, question['questions'], reply_markup=markup)
        bot.register_next_step_handler(msg, check_answer, questions)
    else:
        points = ZooQuiz.points
        result(message, points)


def check_answer(message, questions):
    question = questions[0]
    answer = message.text
    if len(questions) != 0:
        for i in list(question['answers'].keys()):
            if answer == i:
                ZooQuiz.points += question['answers'].get(answer)
                questions.pop(0)
                display_question(message, questions)
                break


def result(message, points):
    if points > 9:
        points = 9
    animals = ZooQuiz.animals
    for keys, value in animals.items():
        if value[0] == points:
            photo_url = open(value[1], 'rb')
            text = f'Ого! Твое тотемное животное это - {keys}'
            bot.send_photo(message.chat.id, photo=photo_url, caption=text)
            feed(message, keys)
    text = ('Знаешь, этот чудо зверь в нашем зоопарке очень ждет своего опекуна!\n'
            'Опекать – значит помогать любимым животным. Можно взять под крыло любого обитателя Московского зоопарка,\n'
            'в том числе и того, кто живет за городом – в Центре воспроизводства редких видов животных под Волоколамском.\n'
            'Более подробно ты можешь узнать о программе на сайте https://moscowzoo.ru/about/guardianship')
    bot.send_message(message.chat.id, text=text)
    markup = telebot.types.ReplyKeyboardMarkup()
    btn = telebot.types.KeyboardButton('Пройти квиз еще раз!')
    markup.add(btn)
    msg = bot.send_message(message.chat.id, text='Пройдем квиз еще разок?', reply_markup=markup)
    bot.register_next_step_handler(msg, play)

def feed(message, keys):
    text = (f'Ты посмотри! Мое тотемное животное это - {keys}! \n'
            f'Переходи по ссылке и тоже проходи викторину! \n'
            f'https://t.me/SfZoo_bot')
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton(text='Поделиться', url=f"https://t.me/share/url?url={text}")
    markup.add(btn)
    bot.send_message(message.chat.id, text='Круто! Скорее делись своим результатом!', reply_markup=markup)
    contact_staff(message, keys)

def contact_staff(message, quiz_result):
    staff_message = f"Результаты викторины от пользователя {message.chat.id}:\n\n{quiz_result}"
    text = ("Если тебе нужна какая-либо помощь, напишите работнику зоопарка.\n"
            "Он с радостью ответит на все твои вопросы")
    share_message = f"Привет!"
    chat_id = 694958032
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("Помощь", url=f"https://t.me/Ziltriz?url={share_message}")
    markup.add(btn)
    bot.send_message(chat_id=chat_id, text=staff_message)
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


bot.polling()