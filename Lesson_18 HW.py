import json


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
        with open(self.filename, "w", encoding='UTF-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)


class Cities:
    """
    Класс для представления данных о городах из JSON-файла.
    """

    def __init__(self, data):
        self.cities_data = data
        self.all_cities = self.get_data()

    def get_data(self):
        all_cities = set()
        for city in self.cities_data:
            all_cities.add(city["name"].lower())  # Из json файла создаем список городов из Базы
        return all_cities

    def __str__(self):
        return f'Множество городов Российской Федерации:\n[{", ".join(sorted({item for item in self.all_cities})).title()}]'


class CitiesGame:
    """
    Класс описывающий саму игру.
    Методы:
    __init__(self, cities) - Конструктор класса игры
    check_answer(self, current_city, last_city="") - Проверка правил игры
    get_last_letter(self, last_city: str) - Получение корректной последней буквы последнего названного города
    def human_step(self) - описание хода игрока
    def ai_step(self)  - описание хода компьютера
    """

    def __init__(self, cities):
        self.cities_obj: Cities = cities
        self.cities: set = self.cities_obj.all_cities
        self.cities_in_old_answer: set = set()
        # Список букв, на которые городов в России не существует
        self.bad_letters: list = ['ё', 'ы', 'ь', 'ъ']
        self.human_answer: str = ""
        self.ai_answer: str = ""

    def check_answer(self, current_city: str, last_city: str = "") -> bool:
        pass
        if current_city in self.cities_in_old_answer:  # Проверяем ответ среди ранее названых
            print('Вы проиграли! Такой город уже назывался!')
            return False  # Если уже назывался - исключение
        if current_city not in self.cities:  # Проверяем наличие города в России
            print('Вы проиграли! Такого города в России нет!')
            return False
        if last_city != "":  # Если второй города уже назывался
            # определяем правильную последнюю букву (по умолчанию последняя)
            correct_letter = self.get_last_letter(last_city)
            if not current_city.lower().startswith(correct_letter):  # проверяем начало названого игроком города
                # на соответствие последней букве города компьютера
                print('Вы проиграли! Названный Вами город начинается не с правильной буквы!')
                return False
        return True

    def get_last_letter(self, last_city: str) -> str:
        """
        Получаем последнюю букву текущего названого города, по правилам игры
        :param current_city: Последний названый город
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
        self.human_answer: str = input('Введите город: ').lower()
        if self.human_answer == 'стоп':
            print('Вы проиграли!!!')
            return False
        if not self.check_answer(self.human_answer, self.ai_answer):
            return False
        self.cities_in_old_answer.add(self.human_answer)
        self.cities.remove(self.human_answer)
        return True

    def ai_step(self) -> bool:
        """
        Обработка хода игрока
        :return: Булево значение: True - ход корректен
        """
        last_letter = self.get_last_letter(self.human_answer)
        print(f'Принято! Ваш город "{self.human_answer.capitalize()}". '
              f'Мне на {last_letter.upper()}')
        variants: set = {city for city in self.cities if
                         city.startswith(last_letter)}
        if not variants:
            print(f'Я не знаю больше городов на букву {last_letter.upper()}. Вы выиграли! Поздравляю!!!')
            return False
        self.ai_answer: str = variants.pop()
        print(f'Мой ответ "{self.ai_answer.capitalize()}". Вам на {self.get_last_letter(self.ai_answer).upper()}')
        self.cities_in_old_answer.add(self.ai_answer)
        self.cities.remove(self.ai_answer)
        return True


class GameManager:
    """
    Класс обработки запуска игры
    """

    def __init__(self, json_file: JsonFile, cities: Cities, game: CitiesGame):
        self.json_file = json_file
        self.cities = cities
        self.game = game

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
