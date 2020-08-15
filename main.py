from processing import *
from readers import *
from post import *
from contextlib import redirect_stdout


def main():
    print("Читаю приложения...")
    calendar = read_1("data/Приложение №1.xlsx")
    studies, classes, teachers = read_2("data/Приложение №2.xlsx")
    mat = read_5(year, teachers, "data/Приложение №5.xls")
    # curriculum = read_3_all("data/Приложение 3 (docx)")

    print("Создаю пары...")
    pairs = gen_pairs(year, calendar, studies, classes, teachers, mat)

    print("Подбираю аудитории...")
    pairs = divide_classes(pairs, studies, classes)

    print("Подбираю учителей...")
    pairs = divide_teachers(pairs, teachers)

    print("Сохраняю файл...")
    save_file(pairs, "out.xlsx")

    print("Создаю отчет...")
    metric = metrics(pairs, calendar, classes, teachers)

    with open("report.txt", 'w') as f, redirect_stdout(f):
        print_metric(metric)

    print("Готово!")


if __name__ == '__main__':
    main()
