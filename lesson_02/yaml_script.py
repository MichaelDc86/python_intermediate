import random
import yaml
from pprint import pprint
import pickle


def fill_the_inn_dict():
    inn_dict = {}
    # rand_val = random.randint(129, 500)
    for i in range(129, random.randrange(129, 150)):
        inn_dict[chr(random.randint(129, 500))] = str(random.randint(129, 500)) + chr(random.randint(129, 500))
    # print(inn_dict)
    return inn_dict


def get_data_to_yaml():
    data = {
        'first': [i for i in range(0, 100) if i % 7 == 0],
        'second': random.randint(0, 1000),
        'third': fill_the_inn_dict(),
    }
    print(data)
    with open('file.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(data, file, Dumper=yaml.Dumper, default_flow_style=False, allow_unicode=True)


def read_from_yaml():
    with open('file.yaml', 'r', encoding='utf-8') as file:
        pprint(yaml.load(file, Loader=yaml.Loader))


if __name__ == '__main__':
    get_data_to_yaml()
    read_from_yaml()
