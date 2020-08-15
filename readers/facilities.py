import pandas as pd
from pandas import DataFrame
import numpy as np
from misc.dates import *


def read_2(filename="data/Приложение №2.xlsx"):
    studies = pd.read_excel(filename)
    classes = pd.read_excel(filename, 1)
    teachers = pd.read_excel(filename, 2)

    studies = studies.loc[:, "Учебная программа":]
    for i in studies.columns:
        if i != 'Особенности проведения программы':
            studies[i] = studies[i].map(lambda x: 0 if x == '-' or not pd.notnull(x) else x)
        else:
            studies[i] = studies[i].map(lambda x: 'нет' if not pd.notnull(x) else x)
    studies['Без парт'] = studies['Особенности проведения программы'].map(lambda x: 'без' in x.split())
    studies['Доска'] = studies['Особенности проведения программы'].map(lambda x: 'доска' in x.split())
    studies['Приоритет теория'] = studies['Особенности проведения программы'].map(
        lambda x: x.split()[-1].split(',') if 'аудитория' in x.split() and 'практические' not in x.split() else [
            x.split()[-3], x.split()[-1]] if 'или' in x.split() else 0)
    studies['Приоритет практика'] = studies['Особенности проведения программы'].map(
        lambda x: x.split()[-1].split(',') if 'практические' in x.split() else np.nan)

    classes["Аудитория"] = classes["Аудитрия"]
    classes["Без парт"] = classes["Конфигурация аудитории"].map(lambda x: "без" in x.split())
    classes['Доска'] = classes["Конфигурация аудитории"].map(lambda x: 'доска' in x.split())

    return studies, classes, teachers


def make_mat(year, teachers):
    # создаем таблицу на год
    dates = pd.date_range(datetime.datetime(year, 1, 1), datetime.datetime(year, 12, 31))
    mat = DataFrame(1, columns=teachers["Преподаватель"], index=dates)
    # убираем праздники
    for holiday in holidays:
        mat.loc[holiday, :] = 0
    # убираем выходные
    mat[mat.index.to_series().dt.weekday > 4] = 0
    return mat


def read_5(year, teachers, filename="data/Приложение №5.xls"):
    # создаем таблицу на год
    mat = make_mat(year, teachers)

    holidays = pd.read_excel(filename)
    # находим ряды и столбцы
    holidays = holidays.iloc[6:, 1:]
    holidays.index = holidays.iloc[:, 0]
    holidays.columns = holidays.iloc[0]
    # переименовываем фио
    holidays = holidays.iloc[1:-1, 2:-1]
    holidays.index = holidays.index.map(
        lambda x: f'{x.split()[0]} {x.split()[1][0]}.{x.split()[2][0]}.' if len(x.split()) == 3 else x)
    # выделяем декады
    kolvo = holidays.iloc[:, ::2]
    dekada = holidays.iloc[:, 1::2]
    day_start = dekada * 10 + 1
    # добавляем продолжительность отпуска в таблицу
    new_mat = mat.copy()
    for fio, starts in day_start.iterrows():
        for i, start in enumerate(starts):
            try:
                day_start = dt_to_day(datetime.datetime(year, i + 1, int(start)))
                day_end = day_start + kolvo.loc[fio].iloc[i]
                new_mat.loc[:, fio].iloc[day_start:day_end + 1] = 0
            except ValueError:
                pass

    return new_mat
