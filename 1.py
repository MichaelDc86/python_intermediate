# import requests
# from pythonping import ping
#
# ping('8.8.8.8', verbose=True)
# url_1 = 'https://www.youtube.com/'
# youtube = requests.get(url_1).text

word_1 = 'разработка'
word_2 = 'сокет'
word_3 = 'декоратор'

b_word_1 = word_1.encode()
b_word_2 = word_2.encode()
b_word_3 = word_3.encode()

str_word_1 = b_word_1.decode()
str_word_2 = b_word_2.decode()
str_word_3 = b_word_3.decode()

# c latin-1 сделал только дляодного слова. Может, как-то не так понял задание..
# --------------------------------------------------
try:
    bl_word_1 = word_1.encode('latin-1')
except UnicodeEncodeError:
    print('UnicodeEncodeError')
    bl_word_1 = word_1.encode('utf-8')

strl_word_1 = bl_word_1.decode('latin-1')
# --------------------------------------------------

print(bl_word_1)
print(strl_word_1)
# print(youtube)

print(f'{b_word_1}; {type(b_word_1)}\n'
      f'{b_word_2}; {type(b_word_2)}\n'
      f'{b_word_3}; {type(b_word_3)}')

print(f'{str_word_1}; {type(str_word_1)}\n'
      f'{str_word_2}; {type(str_word_2)}\n'
      f'{str_word_3}; {type(str_word_3)}')
