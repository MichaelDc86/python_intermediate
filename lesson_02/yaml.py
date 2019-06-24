import yaml
import random


def fill_the_inn_dict():
    inn_dict = {}
    rand_val = random.randint(129, 500)
    for i in range(129, random.randrange(129, 150)):
        inn_dict[chr(random.randint(129, 500))] = str(random.randint(129, 500)) + chr(rand_val)
    # print(inn_dict)
    return inn_dict


tmp_dict = {
    'first': [i for i in range(0, 100) if i % 7 == 0],
    'second': 7,
    'third': fill_the_inn_dict(),
}


def get_data_to_yaml():
    print(tmp_dict)
    with open('file.yaml', 'w') as file:
        yaml.dump(tmp_dict, file, Dumper=yaml.Dumper)


if __name__ == '__main__':
    get_data_to_yaml()
