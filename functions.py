
import csv
import re


file_csv = 'phonebook_raw.csv'

def anti_chaos(file):
    with open(file, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)  #
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
    # Берем отдельно контакт
    for contact in nested_list:
        full_name = contact[0][0]
        names = full_name.split()  # колонка фамилия
        full_firstname = contact[1][0]
        firstnames = full_firstname.split()  # колонка имя

        # Обновляем информацию о контакте в колонке фамилия
        if len(names) == 3:  # Фамилия, имя и отчество присутствуют.
            contact[0] = [names[0]]  # lastname
            contact[1] = [names[1]]  # firstname
            contact[2] = [names[2]]  # surname
        elif len(names) == 2:  # присутствуют только фамилия и имя
            contact[0] = [names[0]]  # lastname
            contact[1] = [names[1]]  # firstname
            contact[2] = ['']  # surname отсутствует
        elif len(names) == 1:  # еасть только фамилия
            contact[0] = [names[0]]  # lastname
            contact[1] = [''] if not contact[1] else contact[1]
            contact[2] = [''] if not contact[2] else contact[2]

        # Обновляем информацию о контакте в колонке имя
        if len(firstnames) == 2:  # имя и отчество присутствуют.
            contact[1] = [firstnames[0]]  # firstname
            contact[2] = [firstnames[1]]  # surname

    # исправляем телефонные номера
    for contact in nested_list:
        try:
            contact[5] = re.sub(
                r'(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб.)?[\s]*(\d+)*[\)]*',
                r'+7(\2)-\3-\4-\5 \6\7',
                str(contact[5])
            )
        except TypeError:
            # Обрабатывать случаи, когда contact[5] не является строковым или байтовым объектом.
            contact[5] = ''

    # УБИРАЕМ ДУБЛИ
    dict_contacts = {}  # создаем пустой словарь
    for contact in nested_list[0:]:
        key = (contact[0][0], contact[1][0])  # вкладываем в ключ фамилию и имя
        if key not in dict_contacts:  # если имя фамилия нет в словаре
            value = (contact[2][0], contact[3][0], contact[4][0], contact[5][2:-2], contact[6][
                0])  # то добавляем в значение оставшиеся данные контакта заодно избавляемся от не нужных скобок
            dict_contacts[key] = value  # и добавляем в словарь
        elif key in dict_contacts.keys():  # если имя фамилия есть в словаре
            value = (contact[2][0], contact[3][0], contact[4][0], contact[5][2:-2], contact[6][0])
            new_value = []
            for q, w in zip(dict_contacts[key], value):
                if q == w:
                    new_value.append(q)
                elif q == '' and w != '':
                    new_value.append(w)
                elif q != '' and w == '':
                    new_value.append(q)
                else:
                    new_value.append('')
            dict_contacts[key] = tuple(new_value)

    # ОБРАТНО В СПИСОК
    final_list = []
    for key, value in dict_contacts.items():
        contact_list = list(key) + list(value)
        final_list.append(contact_list)

    with open("phonebook.csv", "w", encoding="utf-8") as f:  # записываем результат в csv файл
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(final_list)
