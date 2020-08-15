import datetime


td = datetime.timedelta


def to_dt(year, dot_str):
    try:
        return datetime.datetime.strptime(f"{year}-{dot_str}", "%Y-%d.%m")
    except ValueError:
        # опечатка. underfit на столе, overfit на спине.
        return datetime.datetime.strptime(f"{year}-{dot_str}", "%Y-%d..%m")


def dt_to_day(dt):
    return (dt.date() - datetime.date(dt.year, 1, 1)).days


pair_times = [
         (td(hours=9, minutes=0), td(hours=10, minutes=30)),
         (td(hours=10, minutes=40), td(hours=12, minutes=10)),
         (td(hours=12, minutes=50), td(hours=14, minutes=20)),
         (td(hours=14, minutes=30), td(hours=16, minutes=0)),
]


holidays = ['1.1.2020', '2.1.2020', '3.1.2020', '4.1.2020', '5.1.2020', '6.1.2020', '7.1.2020',
            '8.1.2020', '23.2.2020', '8.3.2020', '1.5.2020', '9.5.2020', '12.6.2020', '4.11.2020']
holidays = [datetime.datetime.strptime(x, "%d.%m.%Y") for x in holidays]
weekdays = "Понедельник Вторник Среда Четверг Пятница Суббота Воскресенье".split(' ')
