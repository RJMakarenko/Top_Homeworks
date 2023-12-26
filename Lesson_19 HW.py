from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import List


class JsonFile:
    """
     Класс для работы с JSON файлами.
     Методы:
     - read_file() - чтение данных из JSON файла
     - write_file() - запись данных в JSON файл
     """

    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        """
        Чтение из файла JSON файла
        :return: Данные из JSON файла
        """
        with open(self.filename, encoding='UTF-8') as cities_json:
            json_data = json.load(cities_json)
        return json_data

    def write_file(self, data) -> None:
        """
        Запись в JSON файл
        :param data: данные для записи
        :return:
        """
        with open(self.filename, "w", encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


@dataclass
class City:
    name: str
    population: int
    subject: str
    district: str
    latitude: float
    longitude: float
    is_used: bool = False


class Cities:
    """
    Класс для представления данных о городах из JSON-файла.
    """

    def __init__(self, data):
        self.cities_data = data
        self.all_cities = self.get_data()

    def get_data(self):
        all_cities = []
        for city in self.cities_data:
            city_instance = City(name=city["name"],
                                 population=city["population"],
                                 subject=city["subject"],
                                 district=city["district"],
                                 latitude=float(city["coords"]['lat']),
                                 longitude=float(city["coords"]['lon'])
                                 )
            all_cities.append(city_instance)
        return all_cities


class CitiesGame:
    """
    Класс описывающий саму игру.
    Методы:
    __init__(self, cities) - Конструктор класса игры
    check_answer_starts_with_correct_letter(self, current_city, last_city="") - Проверка правильности названного города
    (начинается с правильной буквы)
    get_last_letter(self, last_city: str) - Получение корректной последней буквы последнего названного города
    def human_step(self) - описание хода игрока
    def ai_step(self)  - описание хода компьютера
    """

    def __init__(self, cities_instances):
        self.cities_obj: Cities = cities_instances
        self.cities: List[City] = self.cities_obj.all_cities
        self.cities_in_old_answer: set = set()
        # Список букв, на которые городов в России не существует
        self.bad_letters: list = ['ё', 'ы', 'ь', 'ъ']
        self.human_answer: str | City = ""
        self.ai_answer: str | City = ""

    def check_answer_starts_with_correct_letter(self, current_city: str | City, last_city: str | City = "") -> bool:
        if last_city != "":  # Если второй города уже назывался
            # определяем правильную последнюю букву (по умолчанию последняя)
            correct_letter = self.get_last_letter(last_city.name)
            if not current_city.lower().startswith(correct_letter):  # проверяем начало названого игроком города
                # на соответствие последней букве города компьютера
                print('Вы проиграли! Названный Вами город начинается не с правильной буквы!')
                return False
        return True

    def get_last_letter(self, last_city: str) -> str:
        """
        Получаем последнюю букву текущего названого города, по правилам игры
        :return: Последняя правильная буква
        """
        if last_city[-1].lower() in self.bad_letters:
            return last_city[-2].lower()
        return last_city[-1].lower()

    def human_step(self) -> bool:
        """
        Обработка хода игрока
        :return: Булево значение: True - ход корректен
        """
        self.human_answer: str = input('Введите город: ').capitalize()
        if self.human_answer == 'Стоп':
            print('Вы проиграли!!!')
            return False
        for city in self.cities:
            if self.human_answer == city.name:
                self.human_answer = city
                if not city.is_used:
                    city.is_used = True
                    break
                else:
                    print('Вы проиграли! Такой город уже назывался!')
                    return False
        else:
            print('Вы проиграли! Такого города в России нет!')
            return False
        if not self.check_answer_starts_with_correct_letter(self.human_answer.name, self.ai_answer):
            return False
        self.cities_in_old_answer.add(self.human_answer.name)
        return True

    def ai_step(self) -> bool:
        """
        Обработка хода компьютера
        :return: Булево значение: True - ход корректен
        """
        last_letter = self.get_last_letter(self.human_answer.name)
        print(f'Принято! Ваш город "{self.human_answer.name.capitalize()}". '
              f'Мне на {last_letter.upper()}')
        # формируем список городов начинающихся с нужной буквы
        # и на данный момент неиспользованных
        variants = [city for city in self.cities if city.name[0] == last_letter.upper() and not city.is_used]
        # если такой список окажется пустым - значит городов на указанную букву не осталось
        # победа Игрока
        if not variants:
            print(f'Я не знаю больше городов на букву {last_letter.upper()}. Вы выиграли! Поздравляю!!!')
            return False
        # выбираем из собранного списка случайный город
        self.ai_answer: City = variants.pop(random.randint(0, len(variants) - 1))
        # ставим признак того что город уже использовался
        # пользуясь тем, что мы храним ссылку на экземпляр класса
        # изменяем признак самого экземпляра класса
        self.ai_answer.is_used = True
        print(
            f'Мой ответ "{self.ai_answer.name.capitalize()}". Вам на '
            f'{self.get_last_letter(self.ai_answer.name).upper()}')
        return True


class GameManager:
    """
    Класс обработки запуска игры
    """

    def __init__(self, json_data: JsonFile, cities_data: Cities, game_data: CitiesGame):
        self.json_file = json_data
        self.cities = cities_data
        self.game = game_data

    def start_game(self):
        while True:
            if not self.game.human_step():
                break
            if not self.game.ai_step():
                break

    @staticmethod
    def player_meeting():
        print('Привет! Сыграем в "Города"?')
        print('Название городов можете указывать с маленькой буквы, я все равно пойму.')
        print('Если название заканчивается на Ё, Ы, Ь, или Ъ то соперник называет город на предпоследнюю букву.')
        print('Если назовёте город, которого нет в России, или город, который уже назывался - Вы проиграли!')
        print('Если не знаете города - напишите "стоп" и игра закончится!')
        print('Первый ход - за Вами!!! Начинаем!!!')
        print()

    def __call__(self):
        self.player_meeting()
        self.start_game()
        print('Игра окончена!')
        input('Нажмите на любую клавишу для выхода...')


if __name__ == "__main__":
    # Создаем экземпляр класса JsonFile
    json_file = JsonFile("cities.json")
    # Создаем экземпляр класса Cities
    cities = Cities(json_file.read_file())  # Хранит в себе множество городов РФ
    # Создаем экземпляр класса CityGame
    game = CitiesGame(cities)
    # # Создаем экземпляр класса GameManager
    game_manager = GameManager(json_file, cities, game)
    # # Запускаем игру
    game_manager()
