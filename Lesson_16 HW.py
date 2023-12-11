from __future__ import annotations

import csv
import json
from pprint import pprint
from typing import List, Dict, Any


class JsonAppendError(BaseException):
    pass


class CsvFileHandler:
    def __init__(self):
        self.data = None

    def read_file(self, filepath: str, as_dict=False) -> list[str] | list[list[str]]:
        '''
        Метод чтения из CSV файла
        :param filepath: Имя файла для чтения
        :param as_dict: Флаг выходного формата. True - словарь, False - список
        :return: Возвращает список словарей или список списков в зависимости от флага as_dict
        '''
        if as_dict:
            with open(filepath, encoding='UTF-8') as file:
                self.data = csv.DictReader(file, delimiter=';')
                out_dict = []
                for row in self.data:
                    out_dict.append(row)
                return out_dict
        else:
            with open(filepath, encoding='UTF-8') as file:
                self.data = csv.reader(file, delimiter=';')
                out_list = []
                for row in self.data:
                    out_list.append(row)
                return out_list

    def write_file(self, filepath: str, data: list) -> None:
        '''
        Метод записи в CSV файл
        Записывает данные в виде словаря!!!
        :param filepath: имя файла
        :param data: список данных для записи
        :return: Ничего не возвращает, просто создает файл csv
        '''
        with open(filepath, 'w', encoding='UTF-8', newline='') as file:
            field_names = data[0]
            file_writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
            file_writer.writeheader()
            for item in data[1:]:
                data_to_write = {}
                for field_index, fields in enumerate(item):
                    data_to_write[field_names[field_index]] = fields
                file_writer.writerow(data_to_write)

    def append_file(self, filepath: str, data: list) -> None:
        '''
        Метод дозаписи в существующий файл
        :param filepath: имя файла
        :param data: список данных для дозаписи
        :return: Ничего не возвращает, просто создает файл csv
        '''
        with open(filepath, 'a', encoding='UTF-8', newline='') as file:
            field_names = data[0]
            file_writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
            for item in data[1:]:
                data_to_write = {}
                for field_index, fields in enumerate(item):
                    data_to_write[field_names[field_index]] = fields
                file_writer.writerow(data_to_write)


class TxtFileHandler:
    def __init__(self):
        self.data = None

    def write_file(self, filepath: str, data: list) -> None:
        '''
        Метол записи TXT файла
        :param filepath: имя файла для записи
        :param data: список данных
        :return: Ничего не возвращает - создает файл формата TXT
        '''
        with open(filepath, 'w', encoding='UTF-8') as file:
            for string in data:
                string_data = ' '.join(string)
                file.writelines(string_data)
                file.writelines('\n')

    def read_file(self, filepath: str) -> List[str]:
        '''
        Читает данный из указанного файла
        :param filepath: имя файла
        :return: список строк
        '''
        with open(filepath, encoding='UTF-8') as file:
            self.data = file.readlines()
        return self.data

    def append_file(self, filepath: str, data: list) -> None:
        '''
        Метод дозаписи в TXT файл
        :param filepath: имя файла
        :param data: список входных данных
        :return: Ничего не возвращает, дозаписывает данные в файл
        '''
        with open(filepath, 'a', encoding='UTF-8') as file:
            for string in data:
                string_data = ' '.join(string)
                file.writelines(string_data)
                file.writelines('\n')


class JsonFileHandler:
    def __init__(self):
        self.data = None

    def read_file(self, filepath: str):
        '''
        Читает данные из JSON файла
        :param filepath: имя файла
        :return: возвращает объект JSON
        '''
        with open(filepath, encoding='UTF-8') as file:
            self.data = json.load(file)
        return self.data

    def write_file(self, filepath: str, data: list, as_dict=False) -> None:
        '''
        Метод записи в JSON файл
        :param filepath: имя файла
        :param data: список входных данных
        :param as_dict: флаг формата записи. True - Словарь словарей (JSON) False - Список списков JSON
        :return: Ничего не возвращает
        '''
        if as_dict:
            field_names = data[0]
            json_data = {}
            for row_number, item in enumerate(data[1:], 1):
                data_to_write = {}
                for field_index, fields in enumerate(item):
                    data_to_write[field_names[field_index]] = fields
                json_data[row_number] = data_to_write
            with open(filepath, 'w', encoding='UTF-8') as file:
                json.dump(json_data, file, ensure_ascii=False, indent=4)
        else:
            with open('result.json', 'w') as file:
                data_to_write = json.dumps(data, ensure_ascii=False, indent=4)
                json.dump(data_to_write, file)

    def append_file(self, data) -> None:
        raise JsonAppendError('Данный тип файла не поддерживает операцию дописывания')


list_of_students = [
    ['Фамилия', 'Имя', 'Возраст'],
    ['Иванов', 'Иван', '20'],
    ['Петров', 'Петр', '21'],
    ['Сидоров', 'Сидор', '22'],
]

list_of_students_2 = [
    ['Фамилия', 'Имя', 'Возраст'],
    ['Васильев', 'Василий', '25'],
]

# Создаем объект CSV handler
csv_handler = CsvFileHandler()

# Записываем данные в файл
csv_handler.write_file('result.csv', list_of_students)
csv_handler.append_file('result.csv', list_of_students_2)

# Читаем данные из файла
students_list = csv_handler.read_file('result.csv')
students_dict = csv_handler.read_file('result.csv', as_dict=True)

print('Список студентов CSV файл:')
pprint(students_list)
print()
print('Словарь студентов CSV файл:')
pprint(students_dict, sort_dicts=False)
print()

# Создаем объект TXT handler
txt_handler = TxtFileHandler()

# Записываем данные в txt
txt_handler.write_file('result.txt', list_of_students)
txt_handler.append_file('result.txt', list_of_students_2)

# Читаем данные из txt
txt_result = txt_handler.read_file('result.txt')
print('Список студентов TXT файл:')
pprint(txt_result)
print()

# Создаем объект JSON handler
json_handler = JsonFileHandler()

# Записываем данные в JSON в виде словаря
json_handler.write_file('result.json', list_of_students, as_dict=True)
json_dict = json_handler.read_file('result.json')
print('Словарь студентов JSON файл:')
pprint(json_dict)
print()

# Записываем данные в JSON в виде списка
json_handler.write_file('result.json', list_of_students)
json_list = json_handler.read_file('result.json')
print('Список студентов JSON файл:')
pprint(json_list)
print()
