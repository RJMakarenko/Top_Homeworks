import json

from cities import cities_list

bad_letters = ['ы', 'ь', 'ъ']  # Список букв, на которые городов в России не существует
all_cities = set()  # Множество, в котором будем хранить все города
cities_in_old_answers = set()  # Множество, в котором будем хранить все раннее названные города
'''
Пытаемся открыть json файл с результатами игры.
Если файл не существует - создаем его.
Из файла в переменную results считываем содержимое (счет последних игр).
'''
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


class OldAnswer(Exception):
    '''
    Исключение если город уже назывался
    '''
    pass


class CityNotInBase(Exception):
    '''
    Исключение если города в России нет
    '''
    pass


class IncorrectLetterToStart(Exception):
    '''
    Исключение если названый город начинается с неверной буквы
    '''
    pass


def game_results():
    print(f'Текущий счет последних 5 игр:\n'
          f'Компьютер: {results["Game_score"].count("CPU")}\n'
          f'Игрок: {results["Game_score"].count("User")}\n')


def check_answer(city1: str, city2: str = '') -> bool:
    '''
    Функция проверки правильности названного игроком города.
    Проверять правильность ответа компьютера смысла нет, т.к. он берет города только из Базы.

    :param city1: Город, который назвал игрок
    :param city2: Город, который выбрал компьютер. По умолчанию - пусто.
    :return: Результат проверки на ранее названый, на существование города и на правильность первой буквы.

    '''

    if city1 in cities_in_old_answers:  # Проверяем ответ среди ранее названых
        raise OldAnswer  # Если уже назывался - исключение
    if city1 not in all_cities:  # Проверяем наличие города в России
        raise CityNotInBase
    if city2 != '':  # Если второй города уже назывался
        correct_letter = city2.lower()[-1]  # определяем правильную последнюю букву (по умолчанию последняя)
        if correct_letter in bad_letters:  # если последняя есть в списке неправильных букв
            correct_letter = city2.lower()[-2]  # то правильная последння буква - предпоследняя
        if not city1.lower().startswith(correct_letter):  # проверяем начало названого игроком города
            # на соответствие последней букве города компьютера
            raise IncorrectLetterToStart
    return True  # если исключений не возникло - значит город существует, не назывался, и начинается с правильной буквы


all_cities_json = json.dumps(cities_list, ensure_ascii=False)  # Из предложенного словаря создаем json-объект

for city in json.loads(all_cities_json):
    all_cities.add(city["name"].lower())  # Из json файла создаем список городов из Базы,
    # приводим все к нижнему регистру для удобства

print('Привет! Сыграем в "Города"?')
print('Название городов можете указывать с маленькой буквы, я все равно пойму.')
print('Если название заканчивается на Ь, Ы или Ъ то соперник называет город на предпоследнюю букву.')
print('Если назовёте город, которого нет в России, или город, который уже назывался - Вы проиграли!')
print('Если не знаете города - напишите "стоп" и игра закончится!')
print('Начинаем!!!')
print()
game_results()
user_input = input('Введите город: ').lower()
computer_input = ''

while True:
    if user_input.lower() == 'стоп':
        print('Вы проиграли!!!')
        break
    else:
        try:
            check_answer(user_input, computer_input)
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
        if user_input[-1].lower() in bad_letters:
            last_letter = user_input[-2]
        else:
            last_letter = user_input[-1]
        print(f'Принято! Ваш город "{user_input.capitalize()}". Мне на {last_letter.upper()}')
        all_cities.remove(user_input)  # удаляем город, названый игроком из списка городов
        cities_in_old_answers.add(user_input.lower())  # добавляем город в список названых
    variants = {city for city in all_cities if city.startswith(last_letter)}  # формируем варианты ответа компьютера
    # в них включаем все возможные города, начинающиеся с последней буквы города игрока
    if not variants:  # если таких вариантов нет, значит победа за игроком
        print('Вы выиграли! Поздравляю!!!')
        results["Game_score"].insert(0, "User")
        results["Game_score"].pop()
        break
    else:
        computer_input = variants.pop()  # иначе получаем случайный город из списка вариантов
        all_cities.remove(computer_input)  # удаляем город, названый компьютером из списка городов
        cities_in_old_answers.add(computer_input.lower())  # добавляем город в список названых
        variants.clear()  # после ответа компьютера, список вариантов очищаем
        if computer_input[-1] in bad_letters:
            last_letter = computer_input[-2]
        else:
            last_letter = computer_input[-1]
        print(f'Мой ответ "{computer_input.capitalize()}". Вам на {last_letter.upper()}')
        user_input = input('Введите город: ').lower()

with open("results.json", "w", encoding='UTF-8') as results_file:
    json.dump(results, results_file, ensure_ascii=False, indent=4)
