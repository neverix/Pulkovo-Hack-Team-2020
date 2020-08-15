import pandas as pd
from pandas import DataFrame

drop_cols = ["Начальная подготовка", "Начальная подготовка СД", "СПАСОП", "ПОЗ ВС", "Типы ВС", "ПТМ", "ЭБ",
             "Рабочий люльки"]


def read_1(filename="data/Приложение №1.xlsx"):
    df = pd.read_excel(filename)
    # переворачиваем
    df = df.T
    # выбираем категории (строка 5)
    cats = df.iloc[4]
    # выбираем названия (строка 7)
    df.columns = list(df.iloc[6])
    df = df.iloc[7:]
    # выбираем дни недели (столбец 2)
    df.index = df.iloc[:, 1]
    df = df.iloc[:, 2:]
    cats = cats[2:]
    # распространяем категории
    cats = cats[df.columns.notnull()]
    cats = cats.fillna(method="ffill")
    # убираем строки и столбцы с NaN
    df = df.loc[df.index.notnull(), df.columns.notnull()]
    # убираем "невидимые" столбцы
    df.drop(drop_cols, axis=1, inplace=True)

    for i in df.index:
        for k, j in enumerate(df.columns):
            x = df.loc[i, j]
            # делим на события
            x = x.split("\n\n") if isinstance(x, str) else []
            # делим неделю на даты
            start, end = [f for f in i.split('\n') if f][-1].split('-')
            # добавляем неделю и название
            x = [(y, start, end, cats.iloc[k], j) for y in x]
            # сохраняем результат
            df.loc[i, j] = x
    # уплощаем
    flat = list(df.values.flat)
    # совмещаем все клетки
    flat = sum(flat, [])

    # снова преобразуем
    for i, (text, start, end, cat, name) in enumerate(flat):
        texts = []
        aud = ''
        for d in text.split('\n'):
            if "ауд" in d:
                aud = d.split("ауд.")[-1]
            elif "ИАС" in d:
                aud = d.split("ИАС")[-1]
            elif '.' in d:
                if '-' in d:
                    start, end = d.split('-')
                elif '–' in d:
                    start, end = d.split('–')
                else:
                    start = d
            else:
                texts.append(d)
        text = ' '.join(texts)
        flat[i] = text, aud, start, end, cat, name
    # превращаем обратно в df
    df = DataFrame(flat, columns=["text", "aud", "start", "end", "cat", "name"])
    # обрезаем пробелы
    df = df.apply(lambda x: x.str.strip())
    # объединяем группы, занимающие несколько рядов
    df.drop_duplicates(inplace=True)
    return df
