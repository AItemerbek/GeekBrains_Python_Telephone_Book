maleNames = ['иван', 'андрей', 'олег', 'петр', 'алексей', 'александр',
             'федор', 'кирилл', 'леонид', 'максим', 'михаил', 'николай',
             'павел', 'роман', 'сергей', 'василий', 'владимир', 'борис']

maleSurname = ['иванов', 'андреев', 'олегов', 'петров',
               'алексеев', 'александров', 'федоров', 'кириллов',
               'леонидов', 'максимов', 'михаилов', 'николаев',
               'павлов', 'романов', 'сергеев', 'василиев',
                'владимиров', 'борисов']

femaleNames = ['анна', 'александра', 'елена', 'ирина', 'мария', 'ольга',
             'татьяна', 'екатерина', 'наталья', 'виктория', 'ксения', 'светалана',
             'марина', 'дарья', 'олеся', 'инна', 'софия', 'вероника']



import random
def generateNewDict(quantity: int):
    newDict = {}
    for i in range(1,quantity + 1):
        key = i
        sex = random.randint(0,1)
        if sex == 0:
            surname = maleSurname[random.randint(0,len(maleSurname)-1)].upper()
            name = maleNames[random.randint(0,len(maleNames)-1)].upper()
            secondname = maleSurname[random.randint(0,len(maleSurname)-1)].upper() + 'ИЧ'
        else:
            surname = maleSurname[random.randint(0, len(maleSurname) - 1)].upper() + 'А'
            name = femaleNames[random.randint(0, len(femaleNames) - 1)].upper()
            secondname = maleSurname[random.randint(0, len(maleSurname) - 1)].upper() + 'НА'
        phone = str(random.randint(1000000,10000000))
        print(i,surname,name,secondname,phone)
        newDict.update({key:[surname,name,secondname,phone]})
    return newDict
    # print(newDict)

# generateNewDict(10)