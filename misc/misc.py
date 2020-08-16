from collections import Counter


def duplicates(lst):
    return [k for k, v in Counter(lst).items() if v > 1]


def err_check(pairs):
    # проверка на ошибки
    for period, group in pairs.groupby(["start", "end"]):
        auds = list(group.aud)
        for dup in duplicates(auds):
            yield "aud", dup, period
        teachers = list(group.teachers)
        for dup in duplicates(teachers):
            yield "teacher", dup, period
