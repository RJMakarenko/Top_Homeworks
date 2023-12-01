from pprint import pprint

from marvel import full_dict

# Task 2
numbers = list(map(lambda x: int(x) if x.isdigit() else None, input().split()))
print('Список чисел, которые ввел пользователь (None если ввёл не число): ')
print(numbers)
print()

# Task 3
filtered_dict = dict(filter(lambda item: item[0] in numbers, full_dict.items()))
print('Отфильтрованный по ID, находящимся в предыдущем списке, словарь: ')
print(filtered_dict)
print()

# Task 4
directors_set = {film["director"] for film in full_dict.values()}
print('Множество режиссеров: ')
print(directors_set)
print()

# Task 5
str_year_dict = {key: {"title": value["title"],
                       "year": str(value["year"]),
                       "director": value["director"],
                       "screenwriter": value["screenwriter"],
                       "producer": value["producer"],
                       "stage": value["stage"]}
                 for key, value in full_dict.items()}
print('Словарь, в котором год - это строка:')
pprint(str_year_dict, sort_dicts=False)
print()

# Task 6
new_dict = dict(filter(lambda item: item[1]['title'][0] == 'Ч', full_dict.items()))
print('Словарь фильмов, начинающихся с буквы Ч: ')
print(new_dict)
print()

# Task 7 Сортировка по названию фильма
sorted_dict = dict(sorted(full_dict.items(), key=lambda item: item[1]["title"]))
print('Словарь, отсортированный по названию фильма: ')
pprint(sorted_dict, sort_dicts=False)
print()

# Task 8 Сортировка по названию фильма и году выпуска
sorted_dict = dict(sorted(full_dict.items(), key=lambda item: (item[1]["title"], item[1]["year"])))
print('Словарь, отсортированный по фильму и году выпуска: ')
pprint(sorted_dict, sort_dicts=False)
print()

# Task 9 Отсортированный в обратном порядке по году словарь фильмов, начинающихся с буквы Ж
new_dict_movies_startswith_ZH = dict(sorted(filter(lambda item: item[1]['title'][0] == 'Ж', full_dict.items()),
                                            key=lambda item: item[1]["year"], reverse=True))
print('Словарь, отсортированный в обратном порядке по году словарь фильмов, начинающихся с буквы Ж: ')
pprint(new_dict_movies_startswith_ZH, sort_dicts=False)
