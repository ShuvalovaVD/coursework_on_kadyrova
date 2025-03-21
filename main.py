import json

with open(file="data.json", mode="r", encoding="utf-8") as file_in:
    films_dictionary = json.load(file_in)


def request_films_complying_one_condition(par, val, rel):
    """
    Запрашивает фильмы, удовлетворяющие одному условию
    :param par: параметр ("год производства"/"страны производства"/.../"актеры")
    :param val: значение параметра
    :param rel: отношение между параметром и значением: "="/">"/"<"/">="/"<="
    :return: мн-во фильмов films
    Пример запроса №1: par="год производства", val="2020", rel=">" - фильмы после 2020 года выпуска
    Пример запроса №2: par="актеры", val="Роберт Паттинсон", rel=None - фильмы, в которых снимался Робер Паттинсон
    """

    if par == "длительность":
        f = lambda x: int(x.split(":")[0]) * 60 + int(x.split(":")[1])  # преобразует длильность в str в минуты в int
        tmp_dict = {"=": lambda x, y: f(x) == f(y), ">": lambda x, y: f(x) > f(y), "<": lambda x, y: f(x) < f(y),
                    ">=": lambda x, y: f(x) >= f(y), "<=": lambda x, y: f(x) <= f(y)}
    else:
        tmp_dict = {"=": lambda x, y: x == y, ">": lambda x, y: x > y, "<": lambda x, y: x < y,
                    ">=": lambda x, y: x >= y, "<=": lambda x, y: x <= y, None: lambda x, y: y in x}
    check_func = tmp_dict[rel]

    films = set()
    for film_name, film_info in films_dictionary.items():
        if check_func(film_info[par], val):
            films.add(film_name)
    return films


def request_films_complying_many_conditions(conds, cond_rel):
    """
    Запрашивает фильмы, удовлетворяющие многим условиям
    :param conds: список условий [(par1, val1, rel1), (par2, val2, rel2), ...]
    :param cond_rel: отношение между условиями: "И" - должны выполняться все условия, "ИЛИ" - хотя бы одно
    :return: мн-во фильмов films
    """

    if cond_rel == "И":
        func = lambda x, y: x.intersection(y)
    else:
        func = lambda x, y: x.union(y)

    films = set()
    for i in range(len(conds)):
        par, val, rel = conds[i]
        films_i = request_films_complying_one_condition(par, val, rel)
        if i == 0:
            films = films_i
        else:
            films = func(films, films_i)
    return films


def request_sort_films_by_criteria(par, criteria):
    """
    Запрашивает список фильмов и значения их параметров, отсортированных по заданному критерию
    :param par: параметр ("год производства"/"длительность"/"рейтинг IMDb"/"бюджет в $")
    :param criteria: критерий: "increase" - возрастание, "decrease" - убывание
    :return: sorted_films_data
    """

    films_data = [(film_name, film_info[par]) for film_name, film_info in films_dictionary.items()]

    if criteria == "increase":
        reverse_par = False
    else:
        reverse_par = True
    if par == "длительность":
        cmp = lambda x: int(x[1].split(":")[0]) * 60 + int(x[1].split(":")[1])
    else:
        cmp = lambda x: x[1]

    sorted_films_data = sorted(films_data, key=cmp, reverse=reverse_par)
    return sorted_films_data


def get_main_option():
    print("Выберите пункт:")
    print("1. Вывести фильмы, удовлетворяющие заданным(-ому) условиям(-ю)")
    print("2. Вывести фильмы, отсортированные по заданному критерию")
    print("3. Вывести информацию по фильму")
    print("4. Вывести список всех фильмов в \"Фильмотеке\"")
    print("5. Завершить программу")
    while True:
        try:
            main_option = int(input("Введите номер пункта: "))
        except ValueError:
            print("Вы ввели что-то, отличное от целого числа. Повторите ввод.")
        else:
            if main_option not in (1, 2, 3, 4, 5):
                print("Вы ввели целое число, отличное от 1, 2, 3, 4 или 5. Повторите ввод.")
            else:
                return main_option


def get_one_condition():
    print("Выберите параметр, для которого будет задано условие:")
    print("1. год производства")
    print("2. страны производства")
    print("3. длительность")
    print("4. режиссер")
    print("5. жанры")
    print("6. рейтинг IMDb")
    print("7. бюджет в $")
    print("8. актеры")
    while True:
        try:
            parameter_number = int(input("Введите номер параметра: "))
        except ValueError:
            print("Вы ввели что-то, отличное от целого числа. Повторите ввод.")
        else:
            if parameter_number not in (1, 2, 3, 4, 5, 6, 7, 8):
                print("Вы ввели целое число, отличное от 1, 2, 3, 4, 5, 6, 7 или 8. Повторите ввод.")
            else:
                break
    tmp_dict = {1: "год производства", 2: "страны производства", 3: "длительность", 4: "режиссер", 5: "жанры",
                6: "рейтинг IMDb", 7: "бюджет в $", 8: "актеры"}
    parameter = tmp_dict[parameter_number]
    if parameter in ("страны производства", "жанры", "актеры"):
        if parameter == "страны производства":
            print("По данному параметру будут отобраны фильмы, одно из мест съемок которых было в указанной стране.")
            value = input("Введите название страны: ")
        elif parameter == "жанры":
            print("По данному параметру будут отобраны фильмы, которые относятся к указанному жанру.")
            value = input("Введите название жанра: ")
        else:
            print("По данному параметру будут отобраны фильмы, в которых снимался указанный актер.")
            value = input("Введите имя актера: ")
        relation = None
    elif parameter == "режиссер":
        value = input("Введите имя режиссёра: ")
        relation = "="
    else:
        print("После того, как вы введёте значение выбранного параметра,",
              "будет установлено отношение между ними (=/>/</...)")
        if parameter == "длительность":
            while True:
                value = input("Введите длительность в формате [часы]:[минуты] (без квадратных скобок): ")
                if value.count(":") != 1 or (not value.split(":")[0].isdigit()) or (not value.split(":")[1].isdigit()):
                    print("Вы нарушили формат ввода. Повторите ввод.")
                    continue
                if int(value.split(":")[1]) >= 60:
                    print("Минут должно быть меньше 60. Повторите ввод.")
                    continue
                break
        elif parameter in ("год производства", "бюджет в $"):
            while True:
                try:
                    value = int(input(f"Введите {parameter}: "))
                except ValueError:
                    print("Вы ввели что-то, отличное от целого числа. Попробуйте ещё раз.")
                else:
                    if parameter == "год производства" and (value > 2025 or value < 1895):
                        print("Вы ввели некорректный год. Повторите ввод.")
                        continue
                    if parameter == "бюджет в $" and value <= 0:
                        print("Вы ввели некорректный бюджет. Повторите ввод.")
                        continue
                    break
        elif parameter == "рейтинг IMDb":
            while True:
                try:
                    value = float(input("Введите рейтинг IMDb: "))
                except ValueError:
                    print("Вы ввели что-то отличное от вещественного или целого числа, или ввели запятую.",
                          "Повторите ввод.")
                else:
                    if not (0 <= value <= 10):
                        print("Рейтинг не может выходить за рамки диапазона [0; 10]. Повторите ввод.")
                        continue
                    break

        while True:
            relation = input("Введите отношение между параметром и значением: =/>/</>=/<= (без символа слеша): ")
            if relation in ("=", ">", "<", ">=", "<="):
                break
            print("Вы ввели что-то отличное от =/>/</>=/<=. Повторите ввод.")
    return parameter, value, relation


def get_many_conditions():
    conditions = []
    while True:
        conditions.append(get_one_condition())
        answer = input("Хотите ввести ещё одно условие? +/-: ")
        if answer != "+":
            break
    return conditions


def get_condition_relation():
    print("Вы ввели несколько условий. Введите отношение между ними:",
          "И - найти фильмы, удовлетворяющие всем условиям",
          "ИЛИ - найти фильмы, удовлетворяющие хотя бы одному условию", sep="\n")
    while True:
        cond_rel = input("Отношение И/ИЛИ: ").lower()
        if cond_rel in ("и", "или"):
            break
        print("Некорректный ввод. Повторите ввод.")
    return cond_rel.upper()


def get_sorting_criteria():
    print("Выберите параметр, по которому будет выполнена сортировка:")
    print("1. год производства")
    print("2. длительность")
    print("3. рейтинг IMDb")
    print("4. бюджет в $")
    while True:
        try:
            parameter_number = int(input("Введите номер параметра: "))
        except ValueError:
            print("Вы ввели что-то, отличное от целого числа. Повторите ввод.")
        else:
            if parameter_number not in (1, 2, 3, 4):
                print("Вы ввели целое число, отличное от 1, 2, 3 или 4. Повторите ввод.")
            else:
                break
    tmp_dict = {1: "год производства", 2: "длительность", 3: "рейтинг IMDb", 4: "бюджет в $"}
    parameter = tmp_dict[parameter_number]

    print("Выберите критерий сортировки:")
    print("1. по возрастанию")
    print("2. по убыванию")
    while True:
        try:
            criteria_number = int(input("Выберите номер критерия: "))
        except ValueError:
            print("Вы ввели что-то, отличное от целого числа. Повторите ввод.")
        else:
            if criteria_number not in (1, 2):
                print("Вы ввели целое число, отличное от 1 или 2. Повторите ввод.")
            else:
                break
    if criteria_number == 1:
        criteria = "increase"
    else:
        criteria = "decrease"

    return parameter, criteria


def main():
    print("Начало работы программы \"Фильмотека\"")
    while True:
        main_option = get_main_option()
        if main_option == 1:
            conditions = get_many_conditions()
            if len(conditions) == 1:
                cond = conditions[0]
                par, val, rel = cond
                films = request_films_complying_one_condition(par, val, rel)
            else:
                cond_rel = get_condition_relation()
                films = request_films_complying_many_conditions(conditions, cond_rel)
            if len(films) > 0:
                films = sorted(films)
                for i, f in enumerate(films, start=1):
                    print(f"{i}. {f}")
            else:
                print("По вашему запросу ничего не найдено.")
        elif main_option == 2:
            parameter, criteria = get_sorting_criteria()
            sorted_films_data = request_sort_films_by_criteria(parameter, criteria)
            for i, film_data in enumerate(sorted_films_data, start=1):
                print(f"{i}. {film_data[0]} - {film_data[1]}")
        elif main_option == 3:
            film_name = input("Введите название фильма: ").lower()
            tmp_dict = {f_n.lower(): f_n for f_n in films_dictionary.keys()}
            if film_name not in tmp_dict:
                print("Такого фильма нет в \"Фильмотеке\"")
            else:
                correct_film_name = tmp_dict[film_name]
                print(f"{correct_film_name}:")
                for par, val in films_dictionary[correct_film_name].items():
                    print(f"{par} - ", end="")
                    if type(val) == list:
                        print(*val, sep=", ")
                    else:
                        print(val)
        elif main_option == 4:
            for i, film_name in enumerate(sorted(films_dictionary), start=1):
                print(f"{i}. {film_name}")
        else:
            break
        answer = input("Желаете продолжить? +/-: ")
        if answer != "+":
            break
    print("Завершение работы программы \"Фильмотека\"")


main()
