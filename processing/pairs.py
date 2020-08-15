from fuzzywuzzy import process, fuzz
from pandas import DataFrame
from misc.dates import *


def gen_pairs(year, calendar, studies, classes, teachers, mat, curriculum=None):
    data = []
    # итерируем по группам
    for i, (type, aud, start, end, cat, course) in calendar.iterrows():
        start = to_dt(year, start)
        end = to_dt(year, end)
        # выбираем учебную программу, которой соответствует категория
        studies_list = [(studies['Учебная программа'].iloc[i], i) for i in studies.index]
        (study, index), confidence = process.extractOne(f"{type} {course}", studies_list, scorer=fuzz.token_set_ratio)
        # выбираем программу, соответствующую выбранной
        if curriculum:
            (plan_name, study_plan), _ = process.extractOne(f"{cat} {course}", curriculum, scorer=fuzz.token_set_ratio)
        study = studies.iloc[index]
        # выбираем учителей, преподающих категорию
        available_teachers = []
        for i, programs in teachers["Учебные программы"].astype(str).iteritems():
            programs = [int(x) - 1 for x in programs.split(';')]
            if index in programs:
                available_teachers.append(teachers["Преподаватель"].iloc[i])
        # готовимся к циклу, где мы распишем занятия по парам
        hours = int(study["Занятия в классе(теоретические и практические занятия),  ак. часов"])
        total_hours, hours_left = hours, hours
        day = start
        pair = 0
        # расписываем все часы
        while hours_left > 0:
            # если мы прошли все пары за день, переходим на следующий день
            if pair == len(pair_times):
                pair = 0
                day += td(days=1)
                continue
            # если дошли до конца, пора остановиться
            if day > end:
                break
            # смотрим, кто в отпуске
            available = []
            for teacher in available_teachers:
                if mat.loc[day.date().strftime("%Y-%m-%d"), teacher] == 1:
                    available.append(teacher)
            # пропускаем, если нет учителей
            if not available:
                day += td(days=1)
                continue
            # выбираем подходящие аудитории
            auds = []
            for i, cls in classes.iterrows():
                auds.append(cls["Аудитория"])
            # смотрим, когда пара идет
            pair_start, pair_end = pair_times[pair]
            hour_start = total_hours - hours_left
            hour_end = hour_start + 2
            # выбираем тему (медленно)
            if curriculum:
                plan_hours = 0
                theme = []
                for _, group in study_plan.iterrows():
                    t = group["Тема"]
                    try:
                        l = float(group["Лекция"].strip())
                    except ValueError:
                        l = 0
                    try:
                        p = float(group["Практика"])
                    except ValueError:
                        p = 0
                    new_plan_hours = plan_hours + l + p
                    if (hour_start < plan_hours < hour_end) or (hour_start < new_plan_hours < hour_end):
                        theme.append(t)
                    plan_hours = new_plan_hours
                theme = '\n'.join(theme)
            else:
                theme = ""
            # добавляем пару
            data.append((day + pair_start, day + pair_end, hour_start, hour_end, auds, cat, type, course, available,
                         index, theme))
            # переходим на следующую
            hours_left -= 2  # два академических часа
            pair += 1
    df = DataFrame(data,
                   columns=["start", "end", "aca_start", "aca_end", "aud", "cat", "type", "course", "teachers", "study",
                            "theme"])
    return df
