# Задание 1

# Из внешнего источника мы получили список строк. Мы ожидаем, что там будут числовые значения.
# Объявите переменную с новым, пустым списком.
# Объявите цикл, пройдитесь по списку, примените int() к каждому элементу.
# Используйте конструкцию try - except . Ведь неизвестно, пришли ли валидные данные.
# В случае успеха int() - добавьте это число в новый список.
# В случае неудачи, сделайте принт f-строки о том, что данные невалидны (подставьте переменную)
# Сделайте принт нового списка.

# import time
#
# data_lst = ['1', '2', '3', '4d', 5]
# result_list = []
# for item in data_lst:
#     try:
#         result_list.append(int(item))
#         print(f'Строковое значение "{item}" успешно конвертировано в число!')
#         time.sleep(0.5)
#     except ValueError:
#         print(f'Значение "{item}" указано неверно! Конвертировать в число невозможно!')
# print()
# print(f'Результат обработки: {result_list}')

# ============================================================================================================
# ============================================================================================================

# Задание 2

class IncorrectSymbols(Exception):
    pass


class IncorrectBegin(Exception):
    pass


class IncorrectLength(Exception):
    pass


def is_correct(phone: str) -> bool:
    '''
    Обработка корректности номера телефона.
    '''
    digits: str = ''.join(digit for digit in phone if digit.isdigit())  # Выбираем последовательно все цифры
    other_symbols: str = ''.join(
        symbol for symbol in phone if not symbol.isalnum())  # Выбираем последовательно все остальное
    if not all(symbol in correct_symbols for symbol in other_symbols) or (
            phone.count('+') > 1):  # Если среди символов есть некорректный
        raise IncorrectSymbols  # Вызываем исключение Некорректный символ
    if (phone.count('+') == 1 and digits[0] != '7') or (
            phone.count('+') == 0 and digits[0] != '8'):  # Номер должен начинаться с +7 или 8. Если это не так
        raise IncorrectBegin  # Вызываем исключение Некорректное начало номера
    if len(phone) - len(other_symbols) != 11:  # Проверяем длину номера (длина всех символов - длина цифр)
        raise IncorrectLength  # Вызываем исключение Некорректная длина номера
    return True


correct_symbols = ' ()-+'
phone_numbers = input('Введите телефонные номера, разделив их символом ";" : ').split(';')
for phone in phone_numbers:
    try:
        is_correct(phone)
        print(f'Номер телефона {phone} корректен!')
    except IncorrectSymbols:
        print(f'В номере телефона {phone} есть некорректные символы! Проверьте правильность написания!')
    except IncorrectBegin:
        print(f'В номере телефона {phone} указано неверное начало номера! Номер может начинаться на 8 или +7')
    except IncorrectLength:
        print(f'В номере телефона {phone} неверное количество цифр! Длина номера должна составлять 11 символов!')
    except Exception:
        print(f'Неопознанная ошибка!')
