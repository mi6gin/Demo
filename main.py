import telebot
import wikipedia, re
from soviet_union import communism
# Создаем экземпляр бота

bot = telebot.TeleBot("token=communism")

wikipedia.set_lang("ru")

# Функция, обрабатывающая команду /start

@bot.message_handler(commands=["start"])

def starting(message):

    photo = open('/home/mi6gun/bot/files/start.png', 'rb')

    bot.send_photo(message.chat.id, photo, 'Здравствуйте мистер Романов ✌️, меня зовут Нихао, я ваш ассистент!')

    bot.send_message(message.chat.id, 'Если вам что-нибудь понадобится, то просто воспользуйтесь командой /help, и я сразу же прийду к вам на помощь!')

# Функция, обрабатывающая команду /help
@bot.message_handler(commands=["help"])

def helping(message):

    sticker = open('/home/mi6gun/bot/files/help.webp', 'rb')

    bot.send_sticker(message.chat.id, sticker)

    bot.send_message(message.chat.id, 'Пока что из доступных функций я могу предложить вам лишь вызов списка(для его вызова используйте команду /list) и поиск на Википедии(для этого используйте команду /wiki).')

# Функция, обрабатывающая команду /list
@bot.message_handler(commands=["list"])

def listing(message):
    bot.send_message(
        message.chat.id, 'Ваш список: 1)Остальгия; 2)Microsoft word for windows(10). Для того чтобы получить доступ к файлам вышлите мне их номер в списке.')
    bot.register_next_step_handler(message, list_files)

def list_files(message):
    dict = {
        '1': 'Остальгия: берлинская стена - https://drive.google.com/drive/folders/1-kagrWnuxGG5ZAu4OW3R_WO0nISELn6m?usp=sharing',
        '2': 'Оффис для винды - https://drive.google.com/drive/folders/127lldOpiGAYAhgRD7kff6Pv_cmn6VO39?usp=sharing',
    }
    if message.text in dict:
        bot.send_message(message.chat.id, dict[message.text])
        if message.text == '1' or '2': bot.register_next_step_handler(message, list_files)
    elif message.text == '/wiki' or '/help' or '/start':bot.send_message(message.chat.id, 'Простите мистер Романов, я совсем забыла вам сказать, что в режиме "списка" команды плохо работают... Отправте ещё раз пожалуйста.')
    else:bot.send_message(message.chat.id, 'Мне кажется, вы что-то не то написали мистер Романов') and bot.register_next_step_handler(message, list_files)


@bot.message_handler(commands=["wiki"])
def wiki(message):
    bot.send_message(
        message.chat.id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')
    if message.text:
        bot.register_next_step_handler(message, handle_text)

def handle_text(message):
    bot.send_message(message.chat.id, wikiliks(message.text))

# Подфункция википедии
def wikiliks(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'



# Запускаем бота

bot.polling(none_stop=True, interval=0)
