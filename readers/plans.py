import os
from pandas import DataFrame
from docx import Document


def read_3 (fn, t):
    l = list()
    for i, row in enumerate(t.rows[2:]):
      d = dict()
      d['Учебная программа'] = fn[:-4]
      d['Тема'] = row.cells[1].text
      if not d["Тема"] or not ("Тема" in d["Тема"] or "контроль" in d["Тема"].lower()):
        continue
      d['Лекция'] = row.cells[3].text
      d['Практика'] = row.cells[4].text
      l.append(d)
    df = DataFrame(l, columns = ['Учебная программа', 'Тема', 'Лекция', 'Практика'])
    return df


def read_3_all(dn="app3"):
    #находим все файлы с учебными программами
    directory = dn
    files = os.listdir(directory)
    curriculum = DataFrame(columns=['Учебная программа', 'Тема', 'Лекция', 'Практика'])
    for file in files:
      doc = Document(directory + '/' + file)
      table = doc.tables[0]
      df = read_3(file, table)
      curriculum = curriculum.append(df)
    curriculum = list(curriculum.groupby("Учебная программа"))
    return curriculum
