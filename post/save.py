import pandas as pd
from openpyxl.utils import get_column_letter
from misc import weekdays, err_check


def save_file(pairs, filename="out.xlsx"):
    writer = pd.ExcelWriter(filename)
    for week, group in pairs.groupby(pairs.start.dt.isocalendar().week):
        week_name = f"W{week}"
        # очеловечиваем расписание
        result = pd.DataFrame(index=group.index,
                              columns=["День", "День недели", "Начало", "Конец", "Аудитория", "Курс", "Тип", "Учитель"])
        result["День"] = group["start"].dt.strftime("%d.%m")
        result["День недели"] = group["start"].dt.weekday.apply(lambda x: weekdays[x])
        result["Начало"] = group["start"].dt.strftime('%H:%M')
        result["Конец"] = group["end"].dt.strftime('%H:%M')
        result["Аудитория"] = group["aud"]
        result["Курс"] = group["course"]
        result["Тип"] = group["type"]
        result["Учитель"] = group["teachers"]
        # сортируем и колдуем с индексом
        result.sort_values(["День", "Начало", "Аудитория"], inplace=True)
        result.reindex()
        result.reset_index(inplace=True, drop=True)
        result = result.astype(str)

        # сохраняем
        result.to_excel(writer, index=False, sheet_name=week_name)

        # расширяем столбцы, чтобы все вмещалось
        worksheet = writer.sheets[week_name]
        for i, column in enumerate(result.columns):
            length = result[column].str.len().max()
            worksheet.column_dimensions[get_column_letter(i + 1)].width = length + 5
    writer.save()
