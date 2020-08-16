# Pulkovo-Hack-Team-2020
Команда "Команда" - Pulkovo Hack 2020
## Инструкция по применению
```
pip3 install numpy scipy pandas fuzzywuzzy flask openpyxl xlsxwriter xlrd
FLASK_ENV=development python server.py
```
## API
### /new_session
Начинает новую сессию. Следует вызвать в самом начале. Метод: POST. Возвращает ID сессии.
### /load
Загружает данные из приложения, находящегося в папке с программой.
### /upload/
Загружают файл в справочник. Метод: POST. С запросом надо прикреплять файл.
#### /upload/calendar
Загружает годовой план-график (Пр. 1).
#### /upload/facilities
Загружает справочник преподавателей и аудиторий (Пр. 2)
#### /upload/leaves
Загружает график отпусков (Пр. 5)
#### /upload/source
Загружает исходник годового план-график (Пр. 6).
### /compute
Выполняет все необходимые вычисления.
### /download/
Скачивает результаты. С ответом прикреплен файл.
#### /download/result
Скачивает расписание.
#### /download/report
Скачивает отчет.
