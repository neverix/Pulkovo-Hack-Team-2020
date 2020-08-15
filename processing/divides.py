from scipy.optimize import linear_sum_assignment
import numpy as np


def divide_classes(pairs, studies, classes):
    new_pairs = pairs.copy()
    # распределять надо среди параллельных пар
    for period, group in pairs.groupby(["start", "end"]):
        # распределяем по аудиториям
        # clss = set(group["aud"].apply(pd.Series).stack().reset_index(drop=True))
        # составляем матрицу совместимости кабинетов и преподов
        weights = np.zeros((len(group), len(classes)))
        rows = np.zeros(len(group))
        for i, (k, grp) in enumerate(group.iterrows()):
            for j, cls in classes.iterrows():
                # проверяем, возможно ли вообще их совместить
                impossible = False

                # проверяем по предметам
                study = studies.iloc[grp.study]
                if cls["Без парт"] and not study["Без парт"]:
                    impossible = True
                if study["Доска"] and not cls["Доска"]:
                    impossible = True

                # проверяем по дисциплинам
                disciplines = cls["Подходит для дисциплин"].lower()
                if "все" not in disciplines:
                    check_is = True
                    if "кроме" in disciplines:
                        check_is = False
                    if (grp["cat"].lower() in disciplines) != check_is:
                        impossible = True

                if impossible:
                    weight = -100
                else:
                    # вычисляем вес
                    weight = 0
                    # проверяем по преимуществам
                    advantage = cls["Преимущество у дисциплины"]
                    if grp["cat"] in advantage or grp["course"] in advantage:
                        weight += 100
                    # .
                    if "422" in str(cls["Аудитория"]):
                        weight -= 50
                #
                weights[i, j] = weight
                rows[i] = k
        # используем венгерский алгоритм для поиска соответствий
        _, cols = linear_sum_assignment(weights, maximize=True)
        # задаем выбранные аудитории
        for col, row in zip(cols, rows):
            new_pairs.loc[row, "aud"] = classes.loc[col, "Аудитория"]
    #
    return new_pairs


def divide_teachers(pairs, teachers):
    new_pairs = pairs.copy()
    # распределять надо среди параллельных пар
    for period, group in pairs.groupby(["start", "end"]):
        # распределяем учителей
        available = group["teachers"]
        all_available = list(set(sum(list(available), [])))
        # составляем матрицу совместимости кабинетов и преподов
        weights = np.zeros((len(group), len(all_available)))
        rows = np.zeros(len(group))
        for i, (k, grp) in enumerate(group.iterrows()):
            for j, cls in enumerate(all_available):
                if cls in grp["teachers"]:
                    cls = teachers[teachers['Преподаватель'] == cls].iloc[0]
                    # вычисляем вес
                    weight = 10000
                    # проверяем по дисциплинам
                    if grp["course"] in cls["Дисциплина"]:
                        weight += 100
                    # используем приоритет
                    try:
                        priority = int(cls["Приоритет при распределении"])
                        weight += 10000 / priority
                    except ValueError:
                        pass
                else:
                    weight = 0
                weights[i, j] = weight
                rows[i] = k
        # используем венгерский алгоритм для поиска соответствий
        _, cols = linear_sum_assignment(weights, maximize=True)
        # задаем выбранные аудитории
        for col, row in zip(cols, rows):
            new_pairs.loc[row, "teachers"] = all_available[col]
    #
    return new_pairs
