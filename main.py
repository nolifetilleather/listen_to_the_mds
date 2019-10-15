import telebot
import pandas as pd
import auth
from classes import *
import functions as fnc

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

    user_id = message.from_user.id

    # создание cоcтояния пользователя
    if user_id not in users_states_dict:

        user_state = UserState()
        user_state.sort_type_selection_expected = True
        users_states_dict[user_id] = user_state

        listen_to_the_mds_bot.send_message(
            user_id,
            (
                'Бот предназначен для удобной навигации по '
                'записям радиопередачи "Модель для сборки".\n'
                'Осуществите выбор способа поиска записей:'
            ),
        )

    # сброс состояния пользователя
    else:
        users_states_dict[user_id].reset()

    # это сообщение выводится в любом случае
    listen_to_the_mds_bot.send_message(
        user_id,
        (
            '/search_by_author\nПоиск по имени автора\n\n'
            '/search_by_title\nПоиск по названию\n\n'
            '/search_by_length\nПоиск по длине записи\n\n'
            '/reverse_sort_by_date\nРеверсировать порядок результата поиска'
        ),
    )

# состояние поиска по автору "вкл"
@listen_to_the_mds_bot.message_handler(commands=['search_by_author'])
def search_by_author_set(message):

    user_id = message.from_user.id

    # создание cоcтояния пользователя
    if user_id not in users_states_dict:
        user_state = UserState()
        user_state.author_selection_expected = True
        users_states_dict[user_id] = user_state

    # сброс и установка состояния пользователя
    elif user_id in users_states_dict:
        user = users_states_dict[user_id]
        user.reset()
        user.author_selection_expected = True

    # это сообщение выводится в любом случае
    listen_to_the_mds_bot.send_message(
        user_id,
        'Введите имя автора',
    )

@listen_to_the_mds_bot.message_handler(content_types=['text'])
def search_by_strng(message):

    user_id = message.from_user.id

    if (
            user_id in users_states_dict
            and
            (users_states_dict[user_id].author_selection_expected
             or
             users_states_dict[user_id].title_selection_expected)
    ):

        user_state = users_states_dict[user_id]

        column_dict = {
            True: 'author',
            False: 'title',
        }

        pages_dict = fnc.dict_with_pages_for_navigation(
            fnc.sorted_by_strng_recordings_list(
                recordings_base=recordings_base,
                column=column_dict[user_state.author_selection_expected],
                strng=message.text,
                reverse=users_states_dict[user_id]
                .reversed_by_date_search_result,
            )
        )

        if len(pages_dict[1]) == 0:
            listen_to_the_mds_bot.send_message(
                user_id,
                'По вашему запросу ничего не найдено.\n'
                'Повторите ввод или измените способ поиска /start',
            )
        else:
            # сохраняем в атрибут название столбца для поиска
            user_state.column = \
                column_dict[user_state.author_selection_expected]

            # сохраняем запрос пользователя
            user_state.strng = message.text

            # перестаем ожидать ввод подстроки для поиска
            if user_state.author_selection_expected:
                user_state.author_selection_expected = False
            elif user_state.title_selection_expected:
                user_state.title_selection_expected = False

            # устанавливаем значение запрашиваемой страницы == 0
            user_state.page = 0

            # начинаем ожидать изменения страницы для навигации
            user_state.page_selection_expected = True

            # начинаем ожидать выбора записи
            user_state.recording_selection_expected = True

def send_page_for_recording_selection(user_state):
    


listen_to_the_mds_bot.polling(none_stop=True, interval=0)
