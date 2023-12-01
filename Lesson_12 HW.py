import json

cities_in_old_answers: set = set()  # Множество, в котором будем хранить все раннее названные города


class OldAnswer(Exception):
    """
    Исключение если город уже назывался
    """
    pass


class CityNotInBase(Exception):
    """
    Исключение если города в России нет
    """
    pass


class IncorrectLetterToStart(Exception):
    """
    Исключение если названый город начинается с неверной буквы
    """
    pass


def game_results() -> dict:
    """
    Функция вывода результатов последних пяти игр.
    Выводит на экран текущий счет, который хранится в файле results.json.
    Если такого файла не существует - он будет создан с начальным счетом 0 - 0
    :return Словарь с результатами последних игр
    """
    try:
        with open("results.json") as results_file:
            results = json.load(results_file)
    except FileNotFoundError:  # Если файл не найден создадим файл json
        with open("results.json", "w") as results_file:
            # {"Game_score": [0, 0, 0, 0, 0]}
            # список результатов последних 5 игр
            json.dump({"Game_score": [0, 0, 0, 0, 0]}, results_file)
        with open("results.json") as results_file:
            results = json.load(results_file)
    print(f'Текущий счет последних 5 игр:\n'
          f'Компьютер: {results["Game_score"].count("CPU")}\n'
          f'Игрок: {results["Game_score"].count("User")}\n')
    return results


def load_cities_from_file(filename: str) -> set:
    """
    Заполнение множества городов.
    :param filename: Имя входного json файла
    :return: Множество, содержащее все города России
    """
    with open(filename, encoding='UTF-8') as cities_json:
        all_cities = set()
        for city in json.load(cities_json):
            all_cities.add(city["name"].lower())  # Из json файла создаем список городов из Базы,
            # приводим все к нижнему регистру для удобства
    return all_cities


def check_answer(all_cities: set, city1: str, city2: str = '') -> bool:
    """
    Функция проверки правильности названного игроком города.
    Проверять правильность ответа компьютера смысла нет, т.к. он берет города только из Базы.

    :param city1: Ход игрока
    :param city2: Ход компьютера. По умолчанию - пусто.
    :return: Результат проверки на ранее названый, на существование города и на правильность первой буквы.

    """
    if city1 in cities_in_old_answers:  # Проверяем ответ среди ранее названых
        raise OldAnswer  # Если уже назывался - исключение
    if city1 not in all_cities:  # Проверяем наличие города в России
        raise CityNotInBase
    if city2 != '':  # Если второй города уже назывался
        correct_letter = get_last_letter(city2)  # определяем правильную последнюю букву (по умолчанию последняя)
        if not city1.lower().startswith(correct_letter):  # проверяем начало названого игроком города
            # на соответствие последней букве города компьютера
            raise IncorrectLetterToStart
    return True  # если исключений не возникло - значит город существует, не назывался, и начинается с правильной буквы


def game_start() -> None:
    """
    Вывод приветственного сообщения при старте новой игры
    и описание правил
    """
    print('Привет! Сыграем в "Города"?')
    print('Название городов можете указывать с маленькой буквы, я все равно пойму.')
    print('Если название заканчивается на Ё, Ы, Ь, или Ъ то соперник называет город на предпоследнюю букву.')
    print('Если назовёте город, которого нет в России, или город, который уже назывался - Вы проиграли!')
    print('Если не знаете города - напишите "стоп" и игра закончится!')
    print('Первый ход - за Вами!!! Начинаем!!!')
    print()


def get_last_letter(current_city: str) -> str:
    """
    Получаем последнюю букву текущего названого города, по правилам игры
    :param current_city: Последний названый город
    :return: Последняя правильная буква
    """
    bad_letters: list = ['ё', 'ы', 'ь', 'ъ']  # Список букв, на которые городов в России не существует
    if current_city[-1].lower() in bad_letters:
        return current_city[-2].lower()
    return current_city[-1].lower()


def save_score(score: dict) -> None:
    """
    Сохранение результата игры в json файл
    :param score: Словарь, раннее заполненный из файла с результатами
    """
    with open("results.json", "w", encoding='UTF-8') as results_file:
        json.dump(score, results_file, ensure_ascii=False, indent=4)


def main() -> None:
    """
    Основная функция игры. Ничего не возвращает.
    """
    results: dict = game_results()
    all_cities: set = load_cities_from_file("cities.json")
    game_start()
    user_input: str = input('Введите город: ').lower()
    computer_input: str = ''

    while True:
        if user_input.lower() == 'стоп':
            print('Вы проиграли!!!')
            break
        else:
            try:
                # проверяем правильность ответа пользователя
                # в случае неверного ответа генерируем соответствующее исключение
                check_answer(all_cities, user_input, computer_input)
            except OldAnswer:
                print('Вы проиграли! Такой город уже назывался!')
                results["Game_score"].insert(0, "CPU")
                results["Game_score"].pop()
                break
            except CityNotInBase:
                print('Вы проиграли! Такого города в России нет!')
                results["Game_score"].insert(0, "CPU")
                results["Game_score"].pop()
                break
            except IncorrectLetterToStart:
                print('Вы проиграли! Названный Вами город начинается не с правильной буквы!')
                results["Game_score"].insert(0, "CPU")
                results["Game_score"].pop()
                break
            last_letter: str = get_last_letter(user_input)
            print(f'Принято! Ваш город "{user_input.capitalize()}". Мне на {last_letter.upper()}')
            all_cities.remove(user_input)  # удаляем город, названый игроком из списка городов
            cities_in_old_answers.add(user_input.lower())
            variants: set = {city for city in all_cities if
                             city.startswith(last_letter)}  # формируем варианты ответа компьютера
            # в них включаем все возможные города, начинающиеся с последней буквы города игрока
            if not variants:  # если таких вариантов нет, значит победа за игроком
                print(f'Я не знаю больше городов на букву {last_letter.upper()}. Вы выиграли! Поздравляю!!!')
                results["Game_score"].insert(0, "User")
                results["Game_score"].pop()
                break
            else:
                computer_input = variants.pop()  # иначе получаем случайный город из списка вариантов
                all_cities.remove(computer_input)  # удаляем город, названый компьютером из списка городов
                cities_in_old_answers.add(computer_input.lower())  # добавляем город в список названых
                variants.clear()  # после ответа компьютера, список вариантов очищаем
                last_letter = get_last_letter(computer_input)
                print(f'Мой ответ "{computer_input.capitalize()}". Вам на {last_letter.upper()}')
                user_input = input('Введите город: ').lower()
    save_score(results)


if __name__ == '__main__':
    main()
