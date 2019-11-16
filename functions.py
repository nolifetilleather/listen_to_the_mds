import datetime

# $$$$$$$$$$$$$$$$$$$$$ ФУНКЦИИ ДЛЯ ПОИСКА ЗАПИСЕЙ $$$$$$$$$$$$$$$$$$$$$
# По вхождению подстроки в строку из ячейки стлобца
def sorted_by_strng_in_column_recordings_list(
    recordings_base,
    column,
    strng,
    reverse=False
):
    lst = []

    for i in range(len(recordings_base)):
        if strng.lower() in recordings_base[column][i].lower():
            lst.append(i)

    lst.sort(
        key=lambda j: datetime.date(
            int(recordings_base['date'][j][6:]), #  год
            int(recordings_base['date'][j][3:5]), #  месяц
            int(recordings_base['date'][j][0:2]), #  день
        )
    )

    if reverse:
        lst.reverse()

    return lst

# По соответствию передаваемым границам значению длины записи
def sorted_by_length_recordings_list(
    recordings_base,
    strng,
    reverse=False
):
    import re

    lst = []
    limits = re.findall(r'\d+', strng)

    if len(limits) == 2:
        limits = list(map(int, limits))
        for i in range(len(recordings_base)):
            length = int(recordings_base['length'][i])
            if limits[0] < length < limits[-1]:
                lst.append(i)

        lst.sort(
            key=lambda j: datetime.date(
                int(recordings_base['date'][j][6:]),  # год
                int(recordings_base['date'][j][3:5]),  # месяц
                int(recordings_base['date'][j][0:2]),  # день
            )
        )

        if reverse:
            lst.reverse()

    return lst

# ФОРМИРОВАНИЕ СЛОВАРЯ СТРАНИЦ
def dict_of_navigation_pages(sorted_list):
    pages = len(sorted_list) // 10  # количество страниц
    result_dict = {}
    for i in range(pages + 1):
        page = i + 1  # номер страницы
        if i != pages:
            result_dict[page] = sorted_list[i*10:i*10+10]
        else:
            result_dict[page] = sorted_list[i*10:]

    return result_dict

# СТРАНИЦА НАВИГАЦИИ
def navigation_page(dct, user_state, recordings_base):

    page = ''
    rec_num = 1

    for i in dct[user_state.page]:
        author = recordings_base['author'][i]
        title = recordings_base['title'][i]
        length = recordings_base['length'][i]
        date = recordings_base['date'][i]
        page += (
            f'{rec_num}. {author} - {title}\n'
            f'{length} мин - {date}\n\n'
        )
        rec_num += 1

    page += (
        f'Текущая страница: {user_state.page}\n'
        f'Всего страниц: {len(dct)}'
    )

    return page

def msg_log_text(msg):
    return (
        f'msg_id: {msg.message_id}\n'
        f'user_id: {msg.from_user.id}\n'
        f'user_name: {msg.from_user.username}\n'
        f'first_name: {msg.from_user.first_name}\n'
        f'last_name: {msg.from_user.last_name}\n'
        f'text: {msg.text}'
    )

def log_write(module_name, msg):
    import datetime
    today = datetime.datetime.today()
    with open('./log/log.txt', 'a') as log:
        log.write(
            f'{module_name}:\n'
            f'{today.strftime("%d/%m/%Y %H:%M:%S")}\n'
            f'{msg}\n\n'
        )
