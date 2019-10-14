# ДОБАВЛЕНИЕ ИНФОРМАЦИИ В СПИСОК ПРИ ПОИСКЕ И СОРТИРОВКА
def append_recording_id_date(lst, recordings_base, i, reverse=False):
    """
    Функция предназначена для добавления при выполнении цикла
    поиска иформации о записях из сформированного определенным
    образом pandas.DataFrame() в передаваемый ей список и последующей
    сортировки этого списка в том или ином порядке по ключу,
    который является датой записи.

    lst - передаваемый список
    recordings_base - передаваемый pandas.DataFrame()
    i - меняющееся в цикле значение строки recordings_base
    reverse - флаг указывающий на необходимость расположить записи
    в порядке убывания даты

    Каждый добавляемый таким образом в передаваемый список элемент
    являеся списком из трех строк. Назначения этих строк по индексам:
    [0] - Подстрока из информации о записи предназначенная для вывода
    в диалог с пользователем (для навигации по записям).
    [1] - id сообщения, в котором хранится аудиозапись на сервере
    [2] - Дата записи. Необходима для сортировки и является подстрокой,
    которая при выводе в диалог с пользователем строки с индексом [0]
    добавляется в ее конец.
    """
    recording = (
        f'{recordings_base["author"][i]} - '
        f'{recordings_base["title"][i]}\n'
        f'{recordings_base["length"][i]} мин - '
    )
    recording_id = (
        f'{recordings_base["recording_id"][i]}'
    )
    date = (
        f'{recordings_base["date"][i].split()[0]}'
    )
    lst.append(
        [
            recording,
            recording_id,
            date,
        ]
    )
    lst.sort(key=lambda el: el[2])
    if reverse:
        lst.reverse()

# $$$$$$$$$$$$$$$$$$$$$ ФУНКЦИИ ДЛЯ ПОИСКА ЗАПИСЕЙ $$$$$$$$$$$$$$$$$$$$$
# По вхождению подстроки в строку из ячейки стлобца
def sorted_by_strng_titles_list(
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
def sorted_by_length_titles_list(
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