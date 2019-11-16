import telebot
import pandas as pd
from classes import *
import auth
import functions as fnc
import re

module_name = 'main'

users_states_dict = {}
recordings_base = pd.read_excel('recordings_base.xlsx', dtype=str).fillna('')

rec_expected = False
date_and_station_expected = False

listen_to_the_mds_bot = telebot.TeleBot(auth.token)

recording_choice_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
recording_choice_keyboard.row('1', '2', '3', '4', '5')
recording_choice_keyboard.row('6', '7', '8', '9', '10')
recording_choice_keyboard.row('<<', '<', '>', '>>')

length_choice_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
length_choice_keyboard.row('0..15', '15..30', '30..60')
length_choice_keyboard.row('60..90', '90..180', '180..999')

fnc.log_write(
    module_name,
    'Главный модуль запущен.'
)

# @@@@@@@@@@@@@@@@@@@@@@@@@@ СТАРТ/СБРОС @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@listen_to_the_mds_bot.message_handler(commands=['start'])
def start(message):

    fnc.log_write(
        module_name,
        fnc.msg_log_text(message),
    )

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

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@ ИЗМЕНЕНИЕ ПОРЯДКА СОРТИРОВКИ @@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@listen_to_the_mds_bot.message_handler(commands=['reverse_sort_by_date'])
def reverse_sort_by_date(message):

    fnc.log_write(
        module_name,
        fnc.msg_log_text(message),
    )

    user_id = message.from_user.id

    if user_id not in users_states_dict:
        user_state = UserState()
        user_state.search_type_selection_expected = True
        users_states_dict[user_id] = user_state
    else:
        user_state = users_states_dict[user_id]
        user_state.reversed_by_date_search_result = \
        not user_state.reversed_by_date_search_result

    user_state.reset() # reset не сбрасывет значение
                       # .reversed_by_date_search_result

    # это сообщение выводится в любом случае
    listen_to_the_mds_bot.send_message(
        user_id,
        (
            'Порядок вывода записей изменен!\n\n'
            '/search_by_author\nПоиск по имени автора\n\n'
            '/search_by_title\nПоиск по названию\n\n'
            '/search_by_length\nПоиск по длине записи\n\n'
            '/reverse_sort_by_date\nРеверсировать порядок результата поиска'
        ),
    )

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@ ВЫБОР ПОИСКА ПО АВТОРУ @@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@listen_to_the_mds_bot.message_handler(commands=['search_by_author'])
def set_search_by_author(message):

    fnc.log_write(
        module_name,
        fnc.msg_log_text(message),
    )

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

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@ ВЫБОР ПОИСКА ПО НАЗВАНИЮ @@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@listen_to_the_mds_bot.message_handler(commands=['search_by_title'])
def set_search_by_title(message):

    fnc.log_write(
        module_name,
        fnc.msg_log_text(message),
    )

    user_id = message.from_user.id

    # создание cоcтояния пользователя
    if user_id not in users_states_dict:
        user_state = UserState()
        user_state.title_selection_expected = True
        users_states_dict[user_id] = user_state

    # сброс и установка состояния пользователя
    elif user_id in users_states_dict:
        user_state = users_states_dict[user_id]
        user_state.reset()
        user_state.title_selection_expected = True

    # это сообщение выводится в любом случае
    listen_to_the_mds_bot.send_message(
        user_id,
        'Введите название',
    )

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@ ВЫБОР ПОИСКА ПО ДЛИНЕ @@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@listen_to_the_mds_bot.message_handler(commands=['search_by_length'])
def set_search_by_length(message):

    fnc.log_write(
        module_name,
        fnc.msg_log_text(message),
    )

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

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@ ПОИСК, НАВИГАЦИЯ, АДМИНИСТРИРОВАНИЕ @@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# для уменьшения повторов кода
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
    global rec_expected
    global date_and_station_expected

    fnc.log_write(
        module_name,
        fnc.msg_log_text(message),
    )

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
                fnc.navigation_page(
                    pages_dict, user_state, recordings_base
                ),
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
                fnc.navigation_page(
                    pages_dict, user_state, recordings_base
                ),
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
             message.text in (str(i) for i in range(1, 11)))
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
                    fnc.navigation_page(
                        pages_dict, user_state, recordings_base
                    ),
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
            i = pages_dict[user_state.page][int(message.text) - 1]
            listen_to_the_mds_bot.forward_message(
                user_id,
                auth.bot_admin_id,
                recordings_base['recording_id'][i],
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
    # после добавления записи через excel таблицу
    elif (
            message.text == 'refreshdata'
            and
            user_id == auth.bot_admin_id
    ):

        fnc.log_write(
            module_name,
            fnc.msg_log_text(message),
        )

        try:
            msg = (
                f'Число элементов в recordings_base до обновления: '
                f'{len(recordings_base)}.\n'
                'Пробую обновить...'
            )
            listen_to_the_mds_bot.send_message(
                    user_id,
                    msg,
                )
            fnc.log_write(
                module_name,
                msg,
            )

            recordings_base = pd.read_excel(
                'recordings_base.xlsx', dtype=str
            ).fillna('')

            msg = (
                'Обновление прошло успешно!\n'
                'Число элементов в recordings_base после обновления: '
                f'{len(recordings_base)}'
            )
            listen_to_the_mds_bot.send_message(
                user_id,
                'Обновление прошло успешно!\n'
                'Число элементов в recordings_base после обновления: '
                f'{len(recordings_base)}',
            )
            fnc.log_write(
                module_name,
                msg,
            )
        except Exception as e:
            listen_to_the_mds_bot.send_message(
                user_id,
                f'Возникла ошибка: {e}',
            )

    # для добавления записи через диалог с ботом
    elif (
            message.text == 'addrec'
            and
            user_id == auth.bot_admin_id
    ):

        fnc.log_write(
            module_name,
            'Добавление записи в recordings_base через мессенджер',
        )

        rec_expected = True

        listen_to_the_mds_bot.send_message(
            user_id,
            'Ожидается аудиозапись',
        )

    elif (
            user_id == auth.bot_admin_id
            and
            date_and_station_expected
            and
            len(message.text.split()) > 1
    ):
        date, station = \
            re.split(r' ', message.text, maxsplit=1)[0], \
            re.split(r' ', message.text, maxsplit=1)[1]

        recordings_base['date'][len(recordings_base) - 1] = date
        recordings_base['station'][len(recordings_base) - 1] = station
        recordings_base.to_excel(
            'recordings_base.xlsx',
            index=False,
        )
        listen_to_the_mds_bot.send_message(
            user_id,
            'Информация о дате эфира и станции добавлена к последней записи.\n'
            f'Число строк в recordings_base: {len(recordings_base)}.\n'
            'Файл recordings_base.xlsx обновлен.',
        )
        date_and_station_expected = False

@listen_to_the_mds_bot.message_handler(content_types=['audio'])
def audio_id(message):

    global rec_expected
    global date_and_station_expected
    global recordings_base

    user_id = message.from_user.id
    audio = message.audio

    fnc.log_write(
        module_name,
        f'{fnc.msg_log_text(message)}\n\n{audio}',
    )

    # вернет id сообщения с записью, если режим добавления
    # через диалог не активен
    if user_id == auth.bot_admin_id and not rec_expected:
        listen_to_the_mds_bot.send_message(
            user_id,
            message.message_id,
        )

    elif user_id == auth.bot_admin_id and rec_expected:
        new_line = pd.DataFrame(
            index=[len(recordings_base)],
            columns=[
                'author',
                'title',
                'length',
                'date',
                'recording_id',
                'station',
            ]
        )
        ind = len(recordings_base)
        from math import ceil
        new_line['author'][ind] = audio.performer
        new_line['title'][ind] = audio.title
        new_line['length'][ind] = str(ceil(audio.duration/60))
        new_line['recording_id'][ind] = str(message.message_id)

        recordings_base = recordings_base.append(new_line)

        rec_expected = False
        date_and_station_expected =True

        listen_to_the_mds_bot.send_message(
            user_id,
            'В recordings_base добавлена новая строка. '
            'Ожидается ввод даты эфира и названия радиостанции в формате '
            '"dd.mm.yyyy station".',
        )

listen_to_the_mds_bot.polling(none_stop=True, interval=0)
