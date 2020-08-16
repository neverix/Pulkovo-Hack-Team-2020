from collections import Counter


def duplicates(lst):
    return [k for k, v in Counter(lst).items() if v > 1]


def err_check(pairs):
    # проверка на ошибки. в итоге не использовалась
    for period, group in pairs.groupby(["start", "end"]):
        auds = list(group.aud)
        for dup in duplicates(auds):
            yield f"Накладка с аудиторией {dup} с {period[0]} до {period[1]}"
        teachers = list(group.teachers)
        for dup in duplicates(teachers):
            yield f"Накладка с учителем {dup} с {period[0]} до {period[1]}"

