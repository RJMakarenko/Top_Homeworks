from typing import Callable
import csv


def password_checker(func: Callable[[str], None]) -> Callable:
    def wrapper(password: str) -> None:
        length_flag: bool = len(password) > 8
        upper_letter_flag: bool = any(letter.isdigit() for letter in password)
        lower_letter_flag: bool = any(letter.islower() for letter in password)
        digit_symbol_flag: bool = any(symbol.isdigit() for symbol in password)
        special_character_flag: bool = any(not symbol.isalnum() for symbol in password)
        if all([length_flag, upper_letter_flag, lower_letter_flag, digit_symbol_flag, special_character_flag]):
            func(password)
        else:
            print('Пароль не соответствует требованиям безопасности!')

    return wrapper


@password_checker
def register_user(password: str) -> None:
    print('Успешная регистрация!')


# register_user('123')  # Регистрация не проходит
# register_user('123AAAAaaaFFF')  # Регистрация не проходит
# register_user('AAAAAaaaHjGj')  # Регистрация не проходит
# register_user('123AA!FdF')  # Успешная регистрация
# register_user('1Aa!')  # Регистрация не проходит
# register_user('AaaaaafffddF!')  # Регистрация не проходит


def password_validator(min_length: int = 8, min_uppercase: int = 1, min_lowercase: int = 1, min_special_chars: int = 1):
    """
        Декоратор для валидации паролей.
        Параметры:
        length (int): Минимальная длина пароля (по умолчанию 8).
        uppercase (int): Минимальное количество букв верхнего регистра (по умолчанию 1).
        lowercase (int): Минимальное количество букв нижнего регистра (по умолчанию 1).
        special_chars (int): Минимальное количество спец-знаков (по умолчанию 1).
        Пример использования:
        @password_validator(length=10, uppercase=2, lowercase=2, special_chars=2)
        def register_user(username: str, password: str):
        pass
        """

    def pass_validator(func: Callable) -> Callable:

        def wrapper(username: str, password: str) -> Callable:
            length_flag: bool = len(password) >= min_length
            if not length_flag:
                raise ValueError(f"Длина пароля меньше {min_length}")
            upper_letters_flag: bool = len([letter for letter in password if letter.isupper()]) >= min_uppercase
            if not upper_letters_flag:
                raise ValueError(f"Количество букв верхнего регистра меньше {min_uppercase}")
            lower_letters_flag: bool = len([letter for letter in password if letter.islower()]) >= min_lowercase
            if not lower_letters_flag:
                raise ValueError(f"Количество букв нижнего регистра меньше {min_lowercase}")
            special_characters_flag: bool = len([symbol for symbol in password
                                                 if not symbol.isalnum()]) >= min_special_chars
            if not special_characters_flag:
                raise ValueError(f"Количество спецсимволов меньше {min_special_chars}")

            return func(username, password)

        return wrapper

    return pass_validator


def username_validator(func: Callable) -> Callable:
    def wrapper(username: str, password: str) -> None:
        if ' ' in username:
            raise ValueError('В имени пользователя присутствуют недопустимые символы!')
        else:
            func(username, password)

    return wrapper


@username_validator
@password_validator()
def register_user(username: str, password: str) -> None:
    with open('result.csv', mode="w", encoding="UTF-8") as file:
        filewriter = csv.writer(file, delimiter=",")
        filewriter.writerow([username, password])


try:
    # register_user('BartSimpson', 'FFDFDFSDF!')    # Ошибка букв нижнего регистра
    # register_user('Gomer Simpson', 'aFFDFDFSDF!') # Ошибка в имени пользователя
    # register_user('GomerSimpson', 'aasffffsas!')  # Ошибка букв верхнего регистра
    # register_user('GomerSimpson', 'aasffffsasSD') # Ошибка спецсимволов
    # register_user('GomerSimpson', 'aasfffsasSD!') # Успешная регистрация
    print('Регистрация прошла успешно!')
except ValueError as error:
    print(f'Ошибка: {error}')
