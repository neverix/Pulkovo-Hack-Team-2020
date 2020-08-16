def metrics(pairs, calendar, classes, teachers):
    # создает отчет
    months = []
    # по месяцам
    for month in range(1, 12 + 1):
        pair = pairs[pairs["start"].apply(lambda x: x.month == month)]
        clss = {}
        # использование аудиторий (% от 28 дней в месяц, весь день пары)
        for _, cls in classes.iterrows():
            cls = cls["Аудитория"]
            clss[cls] = len(pair[pair["aud"] == cls]) / (4 * 28)
        events = {}
        # считаем сколько прошло групп каждого типа
        for name, group in calendar.groupby("name"):
            # if type != '':
            #   name = f"{name}: {type}"
            events[name] = len(group[group["start"].apply(lambda x: int(x.split('.')[1]) == month)])
        hours = {}
        # сколько часов работает каждый учитель
        for t, teacher in teachers.iterrows():
            teacher = teacher["Преподаватель"]
            hours[teacher] = len(pair[pair["teachers"] == teacher]) * 2
        months.append((clss, events, hours))
    # считаем итог
    final_month = ({}, {}, {})
    for types in months:
        for i, objects in enumerate(types):
            for name, count in objects.items():
                try:
                    final_month[i][name] += count
                except KeyError:
                    final_month[i][name] = count
    months.append(final_month)
    return months


def print_metric(metric):
    for i, (clss, events, teas) in enumerate(metric):
        if i < 12:
            print(f"Месяц {i + 1}:")
        else:
            print("Итого:")
        print(" Проведено групп:")
        for name, count in events.items():
            if count == 0:
                continue
            print(f"  {name} - {count}")
        print(" Использование кабинетов:")
        for cls, pct in clss.items():
            if i == 12:
                pct /= 12
            if pct < 0.01:
                continue
            print(f"  Кабинет {cls}: {int(pct * 100)}%")
        print(" Загрузка преподавателей:")
        for name, hours in teas.items():
            if hours == 0:
                continue
            print(f"  {name}: {hours}ч")
