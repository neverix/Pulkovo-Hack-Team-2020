import pandas as pd
from pandas import DataFrame
import numpy as np
from misc.dates import *


def read_6(filename="data/Приложение №6.xlsx"):
    df = pd.read_excel(filename)
    flat = []
    # выбираем каждый курс
    for course, group in df.groupby("Наименование Курса"):
        # сортируем по месяцам
        group = group.sort_values("Плановый месяц обучения")
        # а вот тут лучше бы какой-то умный алгоритм, но я ничего иного не придумал
        # тупо проходим по дням
        for i in np.linspace(start=12, stop=350, num=len(group)).astype(int):
            date = datetime.date(year, 1, 1) + datetime.timedelta(days=int(i))
            flat.append(("", "", f"{date.day}.{date.month}", "31.12", "", course))
    # превращаем обратно в df
    df = DataFrame(flat, columns=["text", "aud", "start", "end", "cat", "name"])
    # обрезаем пробелы
    df = df.apply(lambda x: x.str.strip())
    return df

