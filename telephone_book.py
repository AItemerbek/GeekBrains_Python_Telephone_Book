# Создать телефонный справочник с
# возможностью импорта и экспорта данных в
# формате .txt. Фамилия, имя, отчество, номер
# телефона - данные, которые должны находиться
# в файле.
# 1. Программа должна выводить данные
# 2. Программа должна сохранять данные в
# текстовом файле
# 3. Пользователь может ввести одну из
# характеристик для поиска определенной
# записи(Например имя или фамилию
# человека)
# 4. Использование функций. Ваша программа
# не должна быть линейной

import os
import json
import randomdict
import platform
import shutil


def clear():
    system = platform.system()
    if system == 'Windows':
        os.system('cls')
    else:
        term = os.getenv('TERM')
        if term is None:
            os.environ['TERM'] = 'xterm-256color'  # Установить значение по умолчанию
        os.system('clear')


# создать файл
def create_file():
    filename = '.'.join([input("Введите имя файла : "), 'json'])
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({}, f)
    return filename


# вывод всех справочников в папке
def print_files():
    print()
    flag = False
    for foldername, subfolders, filenames in os.walk("."):
        for filename in filenames:
            if filename.endswith('json'):
                print(os.path.join(foldername, filename))
                flag = True
    if not flag:
        print('Файлов не найдено ')
    print()
    createF = input('Хотите создать новый справочник? Введите - \"Y\": ')
    if createF.upper() == 'Y':
        create_file()


# ввод записи
def put_new_line():
    record = []
    flag = True
    record.append(input('Введите фамилию: ').upper())
    record.append(input('Введите имя: ').upper())
    record.append(input('Введите отчество: ').upper())
    while flag:
        telephone = input('Введите номер телефона состоящий из семи цифр: ').upper()
        if len(list(filter(lambda x: x in '0123456789', list(telephone)))) == 7:
            record.append(telephone)
            flag = False
        else:
            print('Ошибка ввода, повторите еще раз!')
    return record


# Проверка существования файла
def if_file_exist(filename: str):
    if os.path.isfile(filename):
        return True
    else:
        print('Справочник пуст или не существует. Введите хотя бы одну запись для начала работы')
        return False


# чтение справочника в формате словаря
def read_dict_form_file(filename: str):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


# добавление записи в файл
def input_data_file(filename: str, data_input):
    if not if_file_exist(filename):
        print(f'Файла {filename} не существует! Сохраните новый справочник')
        filename = create_file()
    data = read_dict_form_file(filename)
    data[str(count_nonempty_lines(filename) + 1)] = data_input
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f'Запись {data_input} успешно добавлена')
    return filename


# считаем список строк, чтобы присвоить номер записи
def count_nonempty_lines(filename: str):
    if not if_file_exist(filename):
        return 0
    data = read_dict_form_file(filename)
    return len(data)


# печать обновленного словаря в файл
def print_dict_to_file(filename: str, new_data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, ensure_ascii=False, indent=4)
    print()


# проверяем есть ключ в словаре
def if_key_in_dict(key: str, data, filename: str):
    if key in data:
        return True
    else:
        print()
        print(f'Записи с номером {key} не существует в справочнике {filename}')
        return False


# генерируем случайный справочник
def random_book():
    print()
    size = int(input('Введите размер справочника: '))
    data = randomdict.generate_new_dict(size)
    filename = '.'.join([input("Сохранить справочник как : "), 'json'])
    print_dict_to_file(filename, data)
    print(f'Справочник из {size} элементов успешно сгенерирован и сохранен в файл {filename}')
    print()
    return filename


# удаление записи из файла
def delete_data_file(filename: str):
    if not if_file_exist(filename):
        return
    deleteKey = input('Введите номер записи для удаления: ')
    data = read_dict_form_file(filename)
    if not if_key_in_dict(deleteKey, data, filename):
        return
    show_record = data[deleteKey]
    print(*show_record)
    change_you_mind = input('Вы точно хотите удалить запись, если да введите \"Y\": ')
    if change_you_mind.upper() != 'Y':
        print()
        print('ОТМЕНА УДАЛЕНИЯ ЗАПИСИ!')
        return
    new_data = {k: v for k, v in data.items() if v != data[deleteKey]}
    new_data = {str(k): v for k, v in enumerate(new_data.values(), start=1)}
    print_dict_to_file(filename, new_data)
    print(f'Запись № {deleteKey} успешно удалена')


# изменение записи
def change_data_file(filename: str):
    if not if_file_exist(filename):
        return
    change_key = input('Введите номер записи для изменения: ')
    data = read_dict_form_file(filename)
    if not if_key_in_dict(change_key, data, filename):
        return
    show_record = data[change_key]
    print(*show_record)
    print(
        'Для изменения нажмите: 0 - запись целиком, 1 - фамилия, 2 - имя, 3 - отчество, 4 - номер телефона , 5 - отмена')
    change_record = input('Введите ваш выбор: ')
    if change_record == '0':
        temp = put_new_line()
        data[change_key] = temp
    elif change_record == '1' or change_record == '2' or change_record == '3' or change_record == '4':
        val = int(change_record) - 1
        temp = data[change_key]
        if change_record == '1': temp[val] = input(f'Фамилия {temp[val]} будет изменена на: ').upper()
        if change_record == '2': temp[val] = input(f'Имя {temp[val]} будет изменено на: ').upper()
        if change_record == '3': temp[val] = input(f'Отчество {temp[val]} будет изменено на: ').upper()
        if change_record == '4':
            flag = True
            while flag:
                temp[val] = input(f'Телефон {temp[val]} будет изменено на: ')
                if len(list(filter(lambda x: x in '0123456789', list(temp[val])))) == 7:
                    flag = False
                else:
                    print('ОШИБКА ВВОДА! Повторите еще раз')
        data[change_key] = temp
    else:
        print('ОТМЕНА ИЗМЕНЕНИЙ')
        return
    new_data = data
    print_dict_to_file(filename, new_data)
    print(f'Запись № {change_key} успешно изменена')


# запрос на изменение
def change_request(filename: str, answer: str):
    if answer.upper() == 'Y':
        print('Введите \"del\" для удаления записи')
        print('Введите \"change\" для изменения записи')
        need_action = input('Введите любое значение для выхода из поиска: ')
        if need_action.upper() == 'DEL':
            return delete_data_file(filename)
        elif need_action.upper() == 'CHANGE':
            return change_data_file(filename)
        else:
            return
    else:
        return


# вывести файл на печать
def output_data_file(filename: str):
    file_re_open = input(f'Текущий файл {filename}. Для смены файла нажмите \"Y\": ')
    print()
    if file_re_open.upper() == 'Y':
        filename = '.'.join([input("Введите имя файла : "), 'json'])
    if not if_file_exist(filename):
        return filename
    data = read_dict_form_file(filename)
    print('╒════════════════╤════════════════╤════════════════╤════════════════╤════════════════╕')
    print('│ № записи       │ Фамилия        │ Имя            │ Отчество       │ Телефон        │')
    for k, v in data.items():
        print('├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤')
        print('│', end='')
        print("{0:>16}".format(k), end='│')
        for value in v:
            print("{0:>16}".format(value), end='│')
        print()
    print('╘════════════════╧════════════════╧════════════════╧════════════════╧════════════════╛')
    print()
    return filename


# поиск записи в справочнике
def find_record(filename: str):
    if not if_file_exist(filename):
        return
    record = input('Введите запись для поиска: ')
    incomplete_match = input('Для точного поиска - введите 1, для приближенного поиска - введите любой знак: ')
    temp = 0
    print()
    data = read_dict_form_file(filename)
    if incomplete_match == '1':
        for k, v in data.items():
            if record.upper() in v:
                print(f"{k}: {v}")
                temp += 1
        if temp == 0:
            print('Такой записи нет в справочнике!')
        else:
            print()
            answer = input('Хотите изменить или удалить запись? Введите: Y - да. N - нет. ')
            change_request(filename, answer)
    else:
        keylist = []
        for k, v in data.items():
            for symbols in v:
                if record.upper() in symbols and k not in keylist:
                    keylist.append(k)
                    print(f"{k}: {v}")
                    temp += 1
        if temp == 0:
            print('Не найдено ни одного соответствия')
        else:
            answer = input('Хотите изменить или удалить запись? Введите: Y - да. N - нет. ')
            change_request(filename, answer)
    print()


# объединение справочников
def merger_files(filename: str):
    if not if_file_exist(filename):
        return
    print()
    print(f'Текущий файл {filename}')
    new_name = '.'.join([input(f'Введите имя файла для объединения с файлом {filename}: '), 'json'])
    if not if_file_exist(new_name):
        return
    answer = input(
        'Введите: 1 - добавление одной записи. 2 - Добавления среза записей. 3 - для полного слияния. 0 - отмена: ')
    if answer == '1':
        new_data = read_dict_form_file(new_name)
        key = input(f'Введите номер записи из словаря {new_name}: ')
        if not if_key_in_dict(key, new_data, new_name):
            return
        new_data = {key: new_data[key]}
    elif answer == '2':
        new_data = read_dict_form_file(new_name)
        startkey = input(f'Введите номер записи с которой начнется слияние из словаря {new_name}: ')
        if not if_key_in_dict(startkey, new_data, new_name):
            return
        stopkey = input(f'Введите номер записи на которой закончится слияние из словаря {new_name}: ')
        if not if_key_in_dict(stopkey, new_data, new_name):
            return
        if int(startkey) > int(stopkey):
            startkey, stopkey = stopkey, startkey
        keys = [str(i) for i in range(int(startkey), int(stopkey) + 1)]
        new_data = {k: v for k, v in new_data.items() if k in keys}
    elif answer == '3':
        new_data = read_dict_form_file(new_name)
    else:
        return
    for k in new_data:
        input_data_file(filename, new_data[k])
    print()
    print('Слияние справочников успешно завершено!')


# удаление дубликатов
def delete_dublicates(filename: str):
    if not if_file_exist(filename):
        return
    data = read_dict_form_file(filename)
    new_data = {}
    [new_data.update({k: v}) for k, v in data.items() if v not in new_data.values()]
    print('Вот перечень всех дубликатов:')
    for k, v in data.items():
        if k not in new_data:
            print(f'{k} : {data[k]}')
    answer = input('Хотите удалить дублирующие записи ? Введите - \'Y\': ')
    new_data = {str(k): v for k, v in enumerate(new_data.values(), start=1)}
    if answer.upper() == 'Y':
        print_dict_to_file(filename, new_data)
        print(f'Удалено {len(data) - len(new_data)} дубликатов')


def main():
    print('Вот список справочников, которые доступны для работы: ')
    print_files()
    file_name = '.'.join([input("Введите имя файла : "), 'json'])
    while True:
        clear()
        print('══════════════════════════════════════════════════════════════════')
        print(f'Работа со справочником {file_name}. Для смены справочника выберете пункт 1 в меню')
        print(' ══════════════════════════════════════════════════════════════════')
        print('Введите: 1 - просмотр справочника. 2 - добавить запись. 3 - найти пользователя')
        print('Введите: 4 - удалить запись. 5 - изменить запись. 6 - объединить справочники')
        print('Введите: 7 - удалить дубликаты с словаре. 8 - сгенерировать справочник. 0 - доступные справочники')
        print('Введите: \"Exit\" для выхода из программы')
        func_num = input('Сделайте Ваш выбор: ')
        if func_num == '1':
            file_name = output_data_file(file_name)
        elif func_num == '2':
            file_name = input_data_file(file_name, put_new_line())
        elif func_num == '3':
            find_record(file_name)
        elif func_num == '4':
            delete_data_file(file_name)
        elif func_num == '5':
            change_data_file(file_name)
        elif func_num == '6':
            merger_files(file_name)
        elif func_num == '7':
            delete_dublicates(file_name)
        elif func_num == '8':
            file_name = random_book()
        elif func_num == '0':
            print_files()
        elif func_num.upper() == 'EXIT':
            break
        else:
            continue


if __name__ == '__main__':
    main()
