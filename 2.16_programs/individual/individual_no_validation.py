#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import datetime as dt
import os
import json
import copy


def load_workers(file_name):
    """
    Загрузка списка людей из json
    """
    if file_name.split(".", maxsplit=1)[-1] != "json":
        print("Несоответствующий формат файла", file=sys.stderr)
        return []

    if not os.path.exists(f"{os.getcwd()}/{file_name}"):
        print("Заданного файла не существует!", file=sys.stderr)
        return []

    with open(file_name, "r", encoding="utf-8") as f_in:
        data = json.load(f_in)
        flag = True
        if flag:
            for i in data:
                i["birth"] = dt.datetime.strptime(
                    i["birth"], "%d.%m.%Y"
                ).date()
            return data
        else:
            return []


def save_workers(file_name, people_list):
    """
    Сохранение списка людей в json
    """
    flag = False
    # Проверка заданного имени файла
    if file_name.split(".", maxsplit=1)[-1] != "json":
        print("Заданный формат файла не .json", file=sys.stderr)
        return False

    # Проверка файла gitignore, если есть - далее
    content = os.listdir(os.getcwd())
    if ".gitignore" in content:
        flag = True
    if not flag:
        file = open(".gitignore", "w")
    file = f"{os.getcwd()}/.gitignore"
    with open(file, "r+", encoding="utf-8") as gi:
        if file_name not in gi:
            gi.write(f"{file_name}\n")

    # Делаем копию списка, чтобы его не затронуть
    lst = copy.deepcopy(people_list)
    # Сериализация даты в строку для записи в файл
    for i in lst:
        i['birth'] = i['birth'].strftime("%d.%m.%Y")

    # Дамп в json списка
    with open(file_name, "w", encoding="utf-8") as f_out:
        json.dump(lst, f_out, ensure_ascii=False, indent=4)
    lst.clear()


def add_people():
    """
    Добавить людей
    """
    name = input("Введите фамилию и имя через пробел: ")
    pnumber = input("Введите номер телефона: ")
    birth = input("Введите дату рождения (01.01.2077): ").split(".")
    birth_dt = dt.datetime(int(birth[2]), int(birth[1]), int(birth[0]))
    return {"name": name, "pnumber": pnumber, "birth": birth_dt}


def display_people(people_list):
    """
    Вывести людей из списка
    """
    if people_list:
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 14, "-" * 19
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^14} | {:^19} |".format(
                "№п/п", "Фамилия Имя", "Номер телефона", "Дата рождения"
            )
        )
        print(line)
        for nmbr, person in enumerate(people_list, 1):
            print(
                "| {:>4} | {:<30} | {:<14} | {:>19} |".format(
                    nmbr,
                    person.get("name", ""),
                    person.get("pnumber", ""),
                    person.get("birth", "").strftime("%d.%m.%Y"),
                )
            )
        print(line)
    else:
        print("Список людей пуст!")


def correct_date(print_month):
    """
    Скорректировать номер месяца
    """
    month_by_text = {
        "январь": "01",
        "февраль": "02",
        "март": "03",
        "апрель": "04",
        "май": "05",
        "июнь": "06",
        "июль": "07",
        "август": "08",
        "сентябрь": "09",
        "октябрь": "10",
        "ноябрь": "11",
        "декабрь": "12",
    }
    if print_month.isalpha():
        print_month.lower()
        for key, value in month_by_text.items():
            if key == print_month:
                print_month = value
    if len(print_month) == 1:
        return "0" + print_month
    else:
        return print_month


def select_people(people_list, correct_printed_month):
    """
    Выбрать людей по заданному месяцу рождения
    """
    result = []
    for person in people_list:
        birth = person.get("birth")
        if correct_printed_month == birth.strftime("%m"):
            result.append(person)
    return result


def main():
    """
    Основная функция программы
    """
    people = []
    print("Программа запущена, введите help для просмотра команд!")

    while True:
        command = input(">>> ").lower()

        if command == "exit":
            break

        elif command == "add":
            person = add_people()
            people.append(person)
            if len(people) > 1:
                people.sort(key=lambda item: item.get("name", ""))

        elif command == "list":
            display_people(people)

        elif command.startswith("select "):
            parts = command.split(" ", maxsplit=1)
            printed_month = parts[1]
            corrected_month = correct_date(printed_month)
            selected = select_people(people, corrected_month)
            if len(selected) > 0:
                display_people(selected)
            else:
                print(
                    "Людей, чьи дни рождения приходятся на этот месяц нет!"
                )

        elif command.startswith("save "):
            parts = command.split(" ", maxsplit=1)
            fn = parts[1].split(".")
            file_name = f"{fn[0]}.{fn[1]}"
            save_workers(file_name, people)

        elif command.startswith("load "):
            parts = command.split(" ", maxsplit=1)
            file_name = parts[1]
            temp = copy.deepcopy(people)
            people = load_workers(file_name)
            if not people:
                people = copy.deepcopy(temp)
            temp.clear()

        elif command == "help":
            print("Список доступных команд:")
            print("add - добавить человека;")
            print("list - вывести список людей;")
            print(
                "select <месяц> ('Январь' / '01') - запросить людей, чьи "
                "дни рождения приходятся на указанный месяц;"
            )
            print("save <имя_файла.json> - сохранить список людей в json")
            print("load <имя_файла.json> - загрузить список людей из json")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда: {command}", file=sys.stderr)


if __name__ == "__main__":
    main()
