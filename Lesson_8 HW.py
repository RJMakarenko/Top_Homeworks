from marvel import full_dict


class IncorrectStage(Exception):
    pass


stage = {1: "Первая фаза",
         2: "Вторая фаза",
         3: "Третья фаза",
         4: "Четвёртая фаза",
         5: "Пятая фаза",
         6: "Шестая фаза"}

while True:
    try:
        user_stage = int(input('Введите номер фазы: '))
        if user_stage < 0 or user_stage > 6:
            raise IncorrectStage
        break
    except ValueError:
        print('Номер фазы должен быть числом!')
    except IncorrectStage:
        print('Такой фазы не существует!')
result = []
for film in full_dict.values():
    if film['stage'] == stage[user_stage]:
        result.append(film)
print(f'Найдено {len(result)} фильмов:')
print()
for i, film in enumerate(result, 1):
    print(f'{i}. \tНазвание: "{film["title"]}"\n\tГод выхода в прокат: {film["year"]}\n\t'
          f'Режиссёр: {film["director"]}\n\tАвтор сценария: {film["screenwriter"]}\n\t'
          f'Продюссер: {film["producer"]}')
    print()