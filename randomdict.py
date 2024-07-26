male_names = ['иван', 'андрей', 'олег', 'петр', 'алексей', 'александр',
              'федор', 'кирилл', 'леонид', 'максим', 'михаил', 'николай',
              'павел', 'роман', 'сергей', 'василий', 'владимир', 'борис']

male_surname = ['иванов', 'андреев', 'олегов', 'петров',
                'алексеев', 'александров', 'федоров', 'кириллов',
                'леонидов', 'максимов', 'михаилов', 'николаев',
                'павлов', 'романов', 'сергеев', 'василиев',
                'владимиров', 'борисов']

female_names = ['анна', 'александра', 'елена', 'ирина', 'мария', 'ольга',
                'татьяна', 'екатерина', 'наталья', 'виктория', 'ксения', 'светалана',
                'марина', 'дарья', 'олеся', 'инна', 'софия', 'вероника']

import random


def generate_new_dict(quantity: int):
    new_dict = {}
    for i in range(1, quantity + 1):
        key = i
        sex = random.randint(0, 1)
        if sex == 0:
            surname = male_surname[random.randint(0, len(male_surname) - 1)].upper()
            name = male_names[random.randint(0, len(male_names) - 1)].upper()
            secondname = male_surname[random.randint(0, len(male_surname) - 1)].upper() + 'ИЧ'
        else:
            surname = male_surname[random.randint(0, len(male_surname) - 1)].upper() + 'А'
            name = female_names[random.randint(0, len(female_names) - 1)].upper()
            secondname = male_surname[random.randint(0, len(male_surname) - 1)].upper() + 'НА'
        phone = str(random.randint(1000000, 10000000))
        print(i, surname, name, secondname, phone)
        new_dict.update({key: [surname, name, secondname, phone]})
    return new_dict
    # print(new_dict)

# generateNewDict(10)
