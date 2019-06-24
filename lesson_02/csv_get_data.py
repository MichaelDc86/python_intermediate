import os
import re
import csv

path = os.getcwd() + '\\data'
os_prod_list = []
os_name_list = []
os_code_list = []
os_type_list = []
words = {
    'word_1': 'Изготовитель системы:.+\s?',
    'word_2': 'Название ОС:.+\s?',
    'word_3': 'Код продукта:.+\s?',
    'word_4': 'Тип системы:.+\s?'
}
main_data = [[words['word_1'].split(':')[0],
              words['word_2'].split(':')[0],
              words['word_3'].split(':')[0],
              words['word_4'].split(':')[0]]]


def get_data():
    for file in os.listdir(path):
        file_name = path + '\\' + file
        with open(file_name, encoding='cp1251') as tmp:
            # print(tmp.encoding)
            content = tmp.read()
            for word in words:
                raw_gap = re.search(words[word], content).span()
                rez = content[raw_gap[0]:raw_gap[1]:]
                if word == 'word_1':
                    os_prod_list.append(rez.split('  ')[-1][:-1:])
                if word == 'word_2':
                    os_name_list.append(rez.split('  ')[-1][:-1:])
                if word == 'word_3':
                    os_code_list.append(rez.split('  ')[-1][:-1:])
                if word == 'word_4':
                    os_type_list.append(rez.split('  ')[-1][:-1:])
    list_of_lists = [os_prod_list, os_name_list, os_code_list, os_type_list]
    tmp_lst = []

    for j in range(len(words)-1):
        for i in list_of_lists:
            tmp_lst.append(i[j])
        main_data.append(tmp_lst)
        tmp_lst = []
    # print(main_data)

    return main_data


def write_to_csv():
    lst = get_data()
    with open('rez.csv', 'w') as tmp:
        writer = csv.writer(tmp, )
        for row in lst:
            writer.writerow(row)


if __name__ == '__main__':
    write_to_csv()
