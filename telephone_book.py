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

clear = lambda: os.system('cls')

# создать файл
def createFile():
    filename = '.'.join([input("Введите имя файла : "),'json'])
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({}, f)
    return filename

# вывод всех справочников в папке
def printFiles():
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
       createFile()

# ввод записи
def putNewLine():
    record = []
    flag = True
    record.append(input('Введите фамилию: ').upper())
    record.append(input('Введите имя: ').upper())
    record.append(input('Введите отчество: ').upper())
    while flag:
        telephone = input('Введите номер телефона состоящий из семи цифр: ').upper()
        if len(list(filter(lambda x:x in '0123456789' , list(telephone)))) == 7 :
           record.append(telephone)
           flag = False
        else:   print('Ошибка ввода, повторите еще раз!')
    return record

# Проверка существования файла
def ifFileExist(filename: str):
    if os.path.isfile(filename):
        return True
    else:
        print('Справочник пуст или не существует. Введите хотя бы одну запись для начала работы')
        return False

    # чтение справочника в формате словаря
def readDictFormFile(filename: str):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# добавление записи в файл
def inputDataFile(filename: str,dataInput):
    if not ifFileExist(filename):
        print(f'Файла {filename} не существует! Сохраните новый справочник')
        filename = createFile()
    data = readDictFormFile(filename)
    data[str(countNonemptyLines(filename) + 1)] = dataInput
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print()
    return filename

# считаем список строк, чтобы присвоить номер записи
def countNonemptyLines(filename: str):
    if not ifFileExist(filename):
        return 0
    data = readDictFormFile(filename)
    return len(data)

# печать обновленного словаря в файл
def printDictToFile(filename: str, newData):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(newData, file, ensure_ascii=False, indent=4)
    print()

# генерируем случайный справочник
def randomBook():
    print()
    size = int(input('Введите размер справочника: '))
    data = randomdict.generateNewDict(size)
    filename = '.'.join([input("Сохранить справочник как : "), 'json'])
    printDictToFile(filename,data)
    print(f'Справочник из {size} элементов успешно сгенерирован и сохранен в файл {filename}')
    print()
    return filename

# удаление записи из файла
def deleteDataFile(filename: str):
    if not ifFileExist(filename):
        return
    deleteKey = input('Введите номер записи для удаления: ')
    changeYouMind = input('Вы точно хотите удалить запись, если да введите \"Y\": ')
    if changeYouMind.upper() != 'Y':
        print()
        print('ОТМЕНА УДАЛЕНИЯ ЗАПИСИ!')
        return
    data = readDictFormFile(filename)
    showRecord = data[deleteKey]
    print(*showRecord)
    newData = {k: v for k,v in data.items() if v != data[deleteKey]}
    newData = {str(k): v for k, v in enumerate(newData.values(), start=1)}
    printDictToFile(filename, newData)
    print(f'Запись № {deleteKey} успешно удалена')

# изменение записи
def changeDataFile(filename: str):
    if not ifFileExist(filename):
        return
    changeKey = input('Введите номер записи для изменения: ')
    data = readDictFormFile(filename)
    showRecord = data[changeKey]
    print(*showRecord)
    print('Для изменения нажмите: 0 - запись целиком, 1 - фамилия, 2 - имя, 3 - отчество, 4 - номер телефона , 5 - отмена')
    changeRecord = input('Введите ваш выбор: ')
    if changeRecord == '0':
        temp = putNewLine()
        data[changeKey] = temp
    elif changeRecord == '1' or changeRecord == '2' or changeRecord == '3' or changeRecord == '4':
        val = int(changeRecord) - 1
        temp = data[changeKey]
        if changeRecord == '1': temp[val] = input(f'Фамилия {temp[val]} будет изменена на: ').upper()
        if changeRecord == '2': temp[val] = input(f'Имя {temp[val]} будет изменено на: ').upper()
        if changeRecord == '3': temp[val] = input(f'Отчество {temp[val]} будет изменено на: ').upper()
        if changeRecord == '4':
            flag = True
            while flag:
                temp[val] = input(f'Телефон {temp[val]} будет изменено на: ')
                if len(list(filter(lambda x: x in '0123456789', list(temp[val])))) == 7:
                    flag = False
                else:
                    print('ОШИБКА ВВОДА! Повторите еще раз')
        data[changeKey] = temp
    else:
        print('ОТМЕНА ИЗМЕНЕНИЙ')
        return
    newData = data
    printDictToFile(filename, newData)
    print(f'Запись № {changeKey} успешно изменена')

# запрос на изменение
def changeRequest(filename: str, answer: str):
    if answer.upper() == 'Y':
        print('Введите \"del\" для удаления записи')
        print('Введите \"change\" для изменения записи')
        needAction = input('Введите любое значение для выхода из поиска: ')
        if needAction.upper() == 'DEL':
           return deleteDataFile(filename)
        elif needAction.upper() == 'CHANGE':
           return changeDataFile(filename)
        else:   return
    else:   return

# вывести файл на печать
def outputDataFile(filename: str):
    fileReOpen = input(f'Текущий файл {filename}. Для смены файла нажмите \"Y\": ')
    print()
    if fileReOpen.upper() == 'Y':
        filename = '.'.join([input("Введите имя файла : "),'json'])
    if not ifFileExist(filename):
        return filename
    data = readDictFormFile(filename)
    print('╒════════════════╤════════════════╤════════════════╤════════════════╤════════════════╕')
    print('│ № записи       │ Фамилия        │ Имя            │ Отчество       │ Телефон        │')
    for k,v in data.items():
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
def findRecord(filename: str):
    if not ifFileExist(filename):
        return
    record = input('Введите запись для поиска: ')
    incompleteMatch = input('Для точного поиска - введите 1, для приближенного поиска - введите любой знак: ')
    temp = 0
    print()
    data = readDictFormFile(filename)
    if incompleteMatch == '1':
        for k,v in data.items():
            if record.upper() in v:
                print(f"{k}: {v}")
                temp += 1
        if temp == 0:
            print('Такой записи нет в справочнике!')
        else:
            print()
            answer = input('Хотите изменить или удалить запись? Введите: Y - да. N - нет. ')
            changeRequest(filename,answer)
    else:
        keylist = []
        for k,v in data.items():
            for symbols in v:
                if record.upper() in symbols and k not in keylist:
                    keylist.append(k)
                    print(f"{k}: {v}")
                    temp += 1
        if temp == 0:
            print('Не найдено ни одного соответствия')
        else:
            answer = input('Хотите изменить или удалить запись? Введите: Y - да. N - нет. ')
            changeRequest(filename, answer)
    print()

# объединение справочников
def mergerFiles(filename: str):
    if not ifFileExist(filename):
        return
    print()
    print(f'Текущий файл {filename}')
    newName = '.'.join([input(f'Введите имя файла для объединения с файлом {filename}: '), 'json'])
    if not ifFileExist(newName):
        return
    data = readDictFormFile(filename)
    newData = readDictFormFile(newName)
    newData = {str(int(k) + len(data)) : v for k,v in newData.items()}
    data.update(newData)
    printDictToFile(filename, data)
    print()
    print('Слияние справочников успешно завершено!')

# удаление дубликатов
def deleteDublicates(filename: str):
    if not ifFileExist(filename):
        return
    data = readDictFormFile(filename)
    newData = {}
    [newData.update({k: v}) for k, v in data.items() if v not in newData.values()]
    print('Вот перечень всех дубликатов:')
    for k, v in data.items():
        if  k not in newData:
            print(f'{k} : {data[k]}')
    answer = input('Хотите удалить дублирующие записи ? Введите - \'Y\': ')
    newData = {str(k): v for k, v in enumerate(newData.values(), start=1)}
    if answer.upper() == 'Y':
        printDictToFile(filename, newData)
        print(f'Удалено {len(data)- len(newData)} дубликатов')

def main():
    print('Вот список справочников, которые доступны для работы: ')
    printFiles()
    fileName = '.'.join([input("Введите имя файла : "),'json'])
    while True:
        clear()
        print('══════════════════════════════════════════════════════════════════')
        print(f'Работа со справочником {fileName}. Для смены справочника выберете пункт 1 в меню')
        print(' ══════════════════════════════════════════════════════════════════')
        print('Введите: 1 - просмотр справочника. 2 - добавить запись. 3 - найти пользователя')
        print('Введите: 4 - удалить запись. 5 - изменить запись. 6 - объединить справочники')
        print('Введите: 7 - удалить дубликаты с словаре. 8 - сгенерировать справочник. 0 - доступные справочники')
        print('Введите: \"Exit\" для выхода из программы')
        func_num = input('Сделайте Ваш выбор: ')
        if func_num == '1':
            fileName = outputDataFile(fileName)
        elif func_num == '2':
            fileName = inputDataFile(fileName, putNewLine())
        elif func_num == '3':
            findRecord(fileName)
        elif func_num == '4':
            deleteDataFile(fileName)
        elif func_num == '5':
            changeDataFile(fileName)
        elif func_num == '6':
            mergerFiles(fileName)
        elif func_num == '7':
            deleteDublicates(fileName)
        elif func_num == '8':
            fileName = randomBook()
        elif func_num == '0':
            printFiles()
        elif func_num.upper() == 'EXIT':
            break
        else: continue

if __name__ == '__main__':
    main()
