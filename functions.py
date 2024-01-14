import pandas as pd
import csv
import re

file_csv = 'phonebook_raw.csv'

# Для наглядности
def visualization(file):
    phonebook_raw_pd = pd.read_csv(file, sep=',', encoding='utf-8')
    return print(phonebook_raw_pd)
    # display(phonebook_raw_pd) # в pc не работает
    # return phonebook_raw_pd.head(3)


def anti_chaos(file):
    with open(file, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)  #
    # pp(contacts_list)
    nested_list = []

    # Создаем список удобный для дальнейшей работы.
    for contact in contacts_list:
        # Создаем временный список для хранения информации о контакте
        contact_info = []
        # Итерируемся по каждому элементу информации в контакте
        for info in contact:
            # Оборачиваем информацию в список и добавляем во временный список
            contact_info.append([info])
        # Добавляем временный список во внешний список
        nested_list.append(contact_info)

    # ИСПРАВЛЯЮ БОРДАК В ФИО
    # Берем отдельно каждый контакт...
    for contact in nested_list:
        full_name = contact[0][0]
        names = full_name.split()

        # Обновляем информацию о контакте
        if len(names) == 3:  # Фамилия, имя и отчество присутствуют.
            contact[0] = [names[0]]  # lastname
            contact[1] = [names[1]]  # firstname
            contact[2] = [names[2]]  # surname
        elif len(names) == 2:  # присутствуют только фамилия и имя
            contact[0] = [names[0]]  # lastname
            contact[1] = [names[1]]  # firstname
            contact[2] = ['']  # surname отсутствует
        elif len(names) == 1:  # есть только фамилия
            contact[0] = [names[0]]  # lastname
            contact[1] = [''] if not contact[1] else contact[1]
            contact[2] = [''] if not contact[2] else contact[2]

    # исправляем телефонные номера
    for contact in nested_list:
        try:
            contact[5] = re.sub(
                r'(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб.)?[\s]*(\d+)*[\)]*',
                r'+7(\2)-\3-\4-\5 \6\7',
                str(contact[5])
            )
        except TypeError:
            # На случай contact[5] не является строковым или байтовым объектом.
            contact[5] = ''

    # Приводим список к первоначальному виду для записи в csv файл.
    flattened_list = [[item[0] if isinstance(item, list) else item for item in sublist] for sublist in nested_list]

    # Записываем исправленные данные в новый файл.
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(flattened_list)
