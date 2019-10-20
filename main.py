import telebot
import pandas as pd
import auth
from classes import *
import functions as fnc

users_states_dict = {}
recordings_base = pd.read_excel('recordings_base.xlsx', dtype=str)

listen_to_the_mds_bot = telebot.TeleBot(auth.token)

recording_choice_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
recording_choice_keyboard.row('1', '2', '3', '4', '5')
recording_choice_keyboard.row('6', '7', '8', '9', '10')
recording_choice_keyboard.row('<<', '<', '>', '>>')

length_choice_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
length_choice_keyboard.row('0..15', '15..30', '30..60')
length_choice_keyboard.row('60..90', '90..180', '180..999')

# @@@@@@@@@@@@@@@@@@@@@@@@@@ СТАРТ/СБРОС @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@listen_to_the_mds_bot.message_handler(commands=['start'])
def start(message):

    user_id = message.from_user.id

    # создание cоcтояния пользователя
    if user_id not in users_states_dict:

        user_state = UserState()
        user_state.search_type_selection_expected = True
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

# @@@@@@@@@@@@@@@@@@@@@@@ ВЫБОР ПОИСКА ПО АВТОРУ @@@@@@@@@@@@@@@@@@@@@@@
@listen_to_the_mds_bot.message_handler(commands=['search_by_author'])
def set_search_by_author(message):

    user_id = message.from_user.id

    # создание cоcтояния пользователя
    if user_id not in users_states_dict:
        user_state = UserState()
        user_state.author_selection_expected = True
        users_states_dict[user_id] = user_state

    # сброс и установка состояния пользователя
    elif user_id in users_states_dict:
        user_state = users_states_dict[user_id]
        user_state.reset()
        user_state.author_selection_expected = True

    # это сообщение выводится в любом случае
    listen_to_the_mds_bot.send_message(
        user_id,
        'Введите имя автора',
    )

# @@@@@@@@@@@@@@@@@@@@@@@ ВЫБОР ПОИСКА ПО ДЛИНЕ @@@@@@@@@@@@@@@@@@@@@@@@
@listen_to_the_mds_bot.message_handler(commands=['search_by_length'])
def set_search_by_length(message):

    user_id = message.from_user.id

    # создание cоcтояния пользователя
    if user_id not in users_states_dict:
        user_state = UserState()
        user_state.length_selection_expected = True
        users_states_dict[user_id] = user_state

    # сброс и установка состояния пользователя
    elif user_id in users_states_dict:
        user_state = users_states_dict[user_id]
        user_state.reset()
        user_state.length_selection_expected = True

    # это сообщение выводится в любом случае
    listen_to_the_mds_bot.send_message(
        user_id,
        'Введите диапазон поиска в минутах',
        reply_markup=length_choice_keyboard,
    )

# @@@@@@@@@@@@@@@@ ПОИСК, НАВИГАЦИЯ, АДМИНИСТРИРОВАНИЕ @@@@@@@@@@@@@@@@@
# используем в навигаци и выборе записи для уменьшения повторов кода
def return_pages_dict(state):
    if state.column is not None:
        pgs_dict = fnc.dict_of_navigation_pages(
            fnc.sorted_by_strng_in_column_recordings_list(
                recordings_base=recordings_base,
                column=state.column,
                strng=state.strng,
                reverse=state.reversed_by_date_search_result,
            )
        )
    else:
        pgs_dict = fnc.dict_of_navigation_pages(
            fnc.sorted_by_length_recordings_list(
                recordings_base=recordings_base,
                strng=state.strng,
                reverse=state.reversed_by_date_search_result,
            )
        )
    return pgs_dict

@listen_to_the_mds_bot.message_handler(content_types=['text'])
def search_navigation_administration(message):

    global recordings_base
    user_id = message.from_user.id

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$ ПОИСК ПО АВТОРУ ИЛИ НАЗВАНИЮ $$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
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

        pages_dict = fnc.dict_of_navigation_pages(
            fnc.sorted_by_strng_in_column_recordings_list(
                recordings_base=recordings_base,
                column=column_dict[user_state.author_selection_expected],
                strng=message.text,
                reverse=user_state.reversed_by_date_search_result,
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
            # устанавливаем значение запрашиваемой страницы == 1
            user_state.page = 1
            # отправляем пользователю страницу для навигации
            listen_to_the_mds_bot.send_message(
                user_id,
                fnc.navigation_page(pages_dict, user_state),
                reply_markup=recording_choice_keyboard,
            )
            # начинаем ожидать изменения страницы для навигации
            user_state.page_selection_expected = True
            # начинаем ожидать выбора записи
            user_state.recording_selection_expected = True

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$ ПОИСК ПО ДЛИНЕ АУДИО $$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    elif (
            user_id in users_states_dict
            and
            users_states_dict[user_id].length_selection_expected
    ):

        user_state = users_states_dict[user_id]

        pages_dict = fnc.dict_of_navigation_pages(
            fnc.sorted_by_length_recordings_list(
                recordings_base,
                message.text,
                user_state.reversed_by_date_search_result,
            )
        )

        if len(pages_dict[1]) == 0:
            listen_to_the_mds_bot.send_message(
                user_id,
                'По вашему запросу ничего не найдено.\n'
                'Повторите ввод или измените способ поиска /start',
                reply_markup=length_choice_keyboard,
            )

        else:
            # сохраняем запрос пользователя
            user_state.strng = message.text
            # перестаем ожидать ввод запроса с длиной
            user_state.length_selection_expected = False
            # устанавливаем значение запрашиваемой страницы == 1
            user_state.page = 1
            # отправляем пользователю страницу для навигации
            listen_to_the_mds_bot.send_message(
                user_id,
                fnc.navigation_page(pages_dict, user_state),
                reply_markup=recording_choice_keyboard,
            )
            # начинаем ожидать изменения страницы для навигации
            user_state.page_selection_expected = True
            # начинаем ожидать выбора записи
            user_state.recording_selection_expected = True

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$ НАВИГАЦИЯ И ОТПРАВКА ЗАПИСИ $$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    elif (
            user_id in users_states_dict
            and
            users_states_dict[user_id].page_selection_expected
            and
            users_states_dict[user_id].recording_selection_expected
            and
            (message.text in ('<<', '<', '>', '>>')
             or
             int(message.text) in range(1, 11))
    ):

        user_state = users_states_dict[user_id]
        pages_dict = return_pages_dict(user_state)

        # СМЕНА СТРАНИЦЫ
        if message.text in ('<<', '<', '>', '>>'):
            page_was_changed = True
            if message.text == '>' and user_state.page < len(pages_dict):
                user_state.page += 1
            elif message.text == '>>' and user_state.page < len(pages_dict):
                user_state.page = len(pages_dict)
            elif message.text == '<' and user_state.page > 1:
                user_state.page -= 1
            elif message.text == '<<' and user_state.page > 1:
                user_state.page = 1
            else:
                page_was_changed = False

            if page_was_changed:
                pages_dict = return_pages_dict(user_state)
                listen_to_the_mds_bot.send_message(
                    user_id,
                    fnc.navigation_page(pages_dict, user_state),
                    reply_markup=recording_choice_keyboard,
                )
            else:
                listen_to_the_mds_bot.send_message(
                    user_id,
                    'Недопустимое изменение страницы',
                    reply_markup=recording_choice_keyboard,
                )

        # ВЫБОР ЗАПИСИ
        elif (
                int(message.text) in range(1, 11)
                and
                len(pages_dict[user_state.page]) >= int(message.text)
        ):
            listen_to_the_mds_bot.forward_message(
                user_id,
                auth.bot_admin_id,
                pages_dict[user_state.page][int(message.text) - 1][4],
            )
        elif(
                int(message.text) in range(1, 11)
                and
                len(pages_dict[user_state.page]) < int(message.text)
        ):
            listen_to_the_mds_bot.send_message(
                user_id,
                'Недопустимый ввод',
                reply_markup=recording_choice_keyboard,
            )

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$ АДМИНИСТРИРОВАНИЕ $$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    # для обновления recordings_base через сообщение в тг
    elif (
            message.text == 'refreshdata'
            and
            user_id == auth.bot_admin_id
    ):
        try:
            listen_to_the_mds_bot.send_message(
                    user_id,
                    f'Число элементов в recordings_base до обновления: '
                    f'{len(recordings_base)}.\n'
                    'Пробую обновить...',
                )

            recordings_base = pd.read_excel('recordings_base.xlsx')

            listen_to_the_mds_bot.send_message(
                user_id,
                'Обновление прошло успешно!\n'
                'Число элементов в recordings_base после обновления: '
                f'{len(recordings_base)}',
            )
        except Exception as e:
            listen_to_the_mds_bot.send_message(
                user_id,
                f'Возникла ошибка: {e}',
            )

    # отправка собственного message_id администратору бота
    elif user_id == auth.bot_admin_id:
        listen_to_the_mds_bot.send_message(
            user_id,
            message.message_id,
        )

listen_to_the_mds_bot.polling(none_stop=True, interval=0)
