import telebot
import pandas as pd
import auth
from classes import *
from functions import *

users_states_dict = {}
recordings_base = pd.read_excel('recordings_base.xlsx')

listen_to_the_mds_bot = telebot.TeleBot(auth.token)

choice_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
choice_keyboard.row('1', '2', '3', '4', '5')
choice_keyboard.row('6', '7', '8', '9', '10')
choice_keyboard.row('<<', '<', '>', '>>')

# СТАРТ/СБРОС
@listen_to_the_mds_bot.message_handler(commands=['start'])
def start(message):

    if message.from_user.id not in users_states_dict:
        listen_to_the_mds_bot.send_message(
            message.from_user.id,
            (
                'Бот предназначен для удобной навигации по '
                'записям радиопередачи "Модель для сборки".\n'
                'Осуществите выбор способа поиска записей:'
            ),
        )

    listen_to_the_mds_bot.send_message(
        message.from_user.id,
        (
            '/search_by_author\nПоиск по имени автора\n\n'
            '/search_by_title\nПоиск по названию\n\n'
            '/search_by_length\nПоиск по длине записи\n\n'
            '/reverse_sort_by_date\nРеверсировать порядок результата поиска'
        ),
    )

    if message.from_user.id not in users_states_dict:
        user = User(
            telegram_id=message.from_user.id
        )
        user.sort_type_selection_expected = True
        users_states_dict[message.from_user.id] = user

    # сброс состояния пользователя
    else:
        del users_states_dict[message.from_user.id]
        user = User(
            telegram_id=message.from_user.id
        )
        users_states_dict[message.from_user.id] = user
    print(users_states_dict)

# состояние поиска по автору вкл
@listen_to_the_mds_bot.message_handler(commands=['search_by_author'])
def search_by_author_set(message):

    if message.from_user.id not in users_states_dict:
        user = User(
            telegram_id=message.from_user.id
        )
        user.author_selection_expected = True
        users_states_dict[message.from_user.id] = user

    elif message.from_user.id in users_states_dict:
        del users_states_dict[message.from_user.id]
        user = User(
            telegram_id=message.from_user.id
        )
        user.author_selection_expected = True
        user.page = 0
        users_states_dict[message.from_user.id] = user

    listen_to_the_mds_bot.send_message(
        message.from_user.id,
        (
            'Введите имя автора'
        ),
    )

@listen_to_the_mds_bot.message_handler(content_types=['text'])
def search_by_strng(message):
    if (
            message.from_user.id in users_states_dict
            and
            (users_states_dict[message.from_user.id].author_selection_expected
             or
             users_states_dict[message.from_user.id].title_selection_expected)
    ):
        # сохраняем запрос пользователя
        users_states_dict[message.from_user.id].strng = message.text
        # "перестаем ожидать" вво

        pages_dict = dict_with_pages_for_navigation(
            sorted_by_strng_recordings_list(
                recordings_base=recordings_base,
                column='author',
                strng=message.text,
                reverse=users_states_dict[message.from_user.id]
                .reversed_by_date_search_result,
            )
        )

listen_to_the_mds_bot.polling(none_stop=True, interval=0)
