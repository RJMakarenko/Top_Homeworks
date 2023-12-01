# Примеры палиндромов
# А лис, он умен — крыса сыр к нему носила
# Но невидим архангел, мороз узором лег на храм, и дивен он

input_string = input('Введите строку для проверки: ')
# формируем строку для проверки, избавляясь от всех символов, не являющихся буквами
string_to_check = ''.join(letter.lower() for letter in input_string if
                           letter.isalpha())
# проверяем равенство строки самой себе наоборот
if string_to_check == string_to_check[::-1]:
    # если равенство выполняется выводим
    print(f'Введённая строка "{input_string}" является Палиндромом')
else:
    # иначе выводим
    print(f'Строка "{input_string}" вообще ни разу не палиндром!')
