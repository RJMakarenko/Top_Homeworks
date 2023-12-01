# Task 1
# Напишите скрипт, который будет проверять номер телефона на валидность. Пользователь вводит номер телефона, а
# скрипт проверяет его и сообщает, правильный формат ввода номера, или нет.
# Критерии проверки номера
# Проверка длины номера (11 знаков ровно)
# Номер может начинаться на 8 или +7 (плюс не считается знаком)
# Проверка на числа - номер должен состоять только из чисел
# Проверка должна проходить, если номер записан в любом формате (скобки, тире, +7, с пробелами между цифрами,
# с пробелами в начале и конце строки)
# Все ниже перечисленные номера должны пройти проверку.
# Вводные данные
# +77053183958
# +77773183958
# 87773183958
# +(777)73183958
# +7(777)-731-83-58
# +7(777) 731 83 58

def is_correct(phone: str) -> bool:
    '''
    Обработка корректности номера телефона.
    '''
    digits: str = ''.join(digit for digit in phone if digit.isdigit())  # Выбираем последовательно все цифры
    other_symbols: str = ''.join(
        symbol for symbol in phone if not symbol.isalnum())  # Выбираем последовательно все остальное
    if not all(symbol in correct_symbols for symbol in other_symbols):  # Если среди символов есть некорректный
        return False  # значит возвращаем Ложь
    if (phone.count('+') > 0 and (phone.count('+') != 1 or phone.find('+') != 0)) or \
            (phone.count('+') == 1 and digits[0] != '7'):  # Если в номере есть плюс - он должен быть один,
        # стоять на первом месте и после него обязательно 7
        return False
    if digits[0] != '7' and digits[0] != '8': # Если не начинается с 7 или 8
        return False
    if len(phone) - len(other_symbols) != 11: # Проверяем длину номера (длина всех символов - длина цифр)
        return False
    return True


correct_symbols = ' ()-+'
# correct_phone_numbers = ['+77053183958', '+77773183958', '87773183958', '+(7777)3183958',
#                          '8 777 318 39 58', '8777 318 39 58', '+7 777 3-1-8-3-9-5-8',
#                          '+7(777)-731-83-58', '+7(777) 731 83 58', '87773183958']
# incorrect_phone_numbers = ['+770+53183958', '+773773183958', '8777318395@8', '+(8777)3183958',
#                            '+87773183958', '8+777 318 39 58', '+7 777 3-1-8-3-9-518',
#                            '+7(777)-731-83-5- +8', '+7(7877) 731 83 58', '8_777_3183958']
# for phone in correct_phone_numbers:
#     print(is_correct(phone))
# for phone in incorrect_phone_numbers:
#     print(is_correct(phone))
phone_number = input('Введите номер телефона для проверки: ')
if is_correct(phone_number):
    print(f'Номер телефона {phone_number} корректен!')
else:
    print(f'В номере телефона {phone_number} есть ошибки! Проверьте правильность написания!')

# Task 2
# Напишите скрипт, проверки пароля на валидность. Пользователь вводит пароль, а скрипт проверяет его и сообщает
# надёжный это пароль, или стоит придумать другой?
# Критерии проверки пароля
# Должен содержать хотя бы один спецзнак
# Не должен содержать пробел
# Должен содержать символы разных регистров (большие и маленькие)
# Должен быть более 7 символов длиной

# Вариант 1

# password_to_check = input()
# if len(password_to_check) > 7 and password_to_check.find(' ') == -1 and not password_to_check.isalnum() and\
#     not password_to_check.isupper() and not password_to_check.islower():
#     print(f'Пароль {password_to_check} валиден! Все проверки пройдены!')
# else:
#     print(f'Пароль {password_to_check} ненадежен! Вам лучше придумать другой пароль!')


# Вариант 2

# password_to_check = input()
# right_length = True if len(password_to_check) > 7 else False
# no_spaces = True if password_to_check.find(' ') == -1 else False
# special_character = True if not password_to_check.isalnum() else False
# letters_in_both_registers = True if not password_to_check.isupper() and not password_to_check.islower() else False
# if right_length and no_spaces and special_character and letters_in_both_registers:
#     print(f'Пароль {password_to_check} валиден! Все проверки пройдены!')
# else:
#     print(f'Пароль {password_to_check} ненадежен! Вам лучше придумать другой пароль!')
