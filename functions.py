# ДОБАВЛЕНИЕ ИНФОРМАЦИИ В СПИСОК ПРИ ПОИСКЕ И СОРТИРОВКА
def append_recording_id_date(lst, recordings_base, i, reverse=False):
    """
    Функция предназначена для добавления при выполнении цикла
    поиска иформации о записях из сформированного определенным
    образом pandas.DataFrame() в передаваемый ей список и последующей
    сортировки этого списка в том или ином порядке по ключу,
    который является датой записи.

    lst: передаваемый список
    recordings_base: передаваемый pandas.DataFrame()
    i: меняющееся в цикле значение строки recordings_base
    reverse: флаг указывающий на необходимость расположить записи
    в порядке убывания даты

    Каждый добавляемый таким образом в передаваемый список элемент
    являеся списком из пяти строк. Индексы строк:
    [0] - Имя автора
    [1] - Название произведения
    [2] - Длина аудиозаписи в минутах
    [3] - id сообщения с аудиозаписью
    [4] - Дата записи
    """
    author = f'{recordings_base["author"][i]}'
    title = f'{recordings_base["title"][i]}'
    length = f'{recordings_base["length"][i]}'
    recording_id = f'{recordings_base["recording_id"][i]}'
    date = f'{recordings_base["date"][i].split()[0]}'  # .split нужен
    # чтобы убрать время из представления даты вида YYYY-MM-DD HH:MM:SS
    lst.append(
        [
            author,
            title,
            length,
            date,
            recording_id,
        ]
    )
    lst.sort(key=lambda el: el[-2])
    if reverse:
        lst.reverse()

# $$$$$$$$$$$$$$$$$$$$$ ФУНКЦИИ ДЛЯ ПОИСКА ЗАПИСЕЙ $$$$$$$$$$$$$$$$$$$$$
# По вхождению подстроки в строку из ячейки стлобца
def sorted_by_strng_in_column_recordings_list(
    recordings_base,
    column,
    strng,
    reverse=False
):
    sorted_list = []
    for i in range(len(recordings_base)):
        if strng.lower() in recordings_base[column][i].lower():
            append_recording_id_date(
                sorted_list,
                recordings_base,
                i,
                reverse
            )
    return sorted_list

# По соответствию передаваемым границам значению длины записи
def sorted_by_length_recordings_list(
    recordings_base,
    strng,
    reverse=False
):
    import re

    limits = re.findall(r'\d+', strng)
    limits = list(map(int, limits))
    sorted_list = []

    for i in range(len(recordings_base)):
        length = int(recordings_base["length"][i])
        if limits[0] <= length <= limits[-1]:
            append_recording_id_date(
                sorted_list,
                recordings_base,
                i,
                reverse
            )

    return sorted_list

# ФОРМИРОВАНИЕ СЛОВАРЯ СТРАНИЦ
def dict_with_pages_for_navigation(sorted_list):
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
def navigation_page(dct, user_state):

    page = ''
    rec_num = 1

    for rec_info in dct[user_state.page]:
        author = rec_info[0]
        title = rec_info[1]
        length = rec_info[2]
        date = rec_info[3]
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