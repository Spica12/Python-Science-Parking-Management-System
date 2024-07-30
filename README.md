# Parking Management System

Parking Management System - це система автоматично визначає номери автомобільних знаків на зображеннях, відстежує тривалість паркування для кожного унікального транспортного засобу та розраховує накопичені паркувальні витрати. Веб-застосунок включає управління обліковими записами користувачів, функції адміністратора, користувача та розширені можливості.

## Функції

- Управління обліковими записами користувачів
- Додавання/видалення зареєстрованих номерних знаків
- Галаштування тарифів на паркування,
- Додавання/видалення транспортного засобу в чорний список.
- Перегляд користувачем власної інформації про номерний знак та історії паркування.
- Завантаження зображень оператором або адміністратором.
- Детекція номерного знаку на зображеннях.
- Оптичне розпізнавання символів для ідентифікації тексту номерного знаку.
- Пошук номера авто у базі даних зареєстрованих транспортних засобів.
- Відстеження тривалості паркування.
- Запис часу в'їзду/виїзду кожного разу, коли визначається номерний знак.
- Розрахунок загальної тривалості паркування для кожного унікального номерного знаку.
- Зберігання даних про тривалість, пов'язаних із номерними знаками, в базі даних.
- Розрахунок вартості паркування.
- Сповіщення користувача, якщо накопичені парковочні витрати перевищують встановлені ліміти.
- Генерація звітів про розрахунки, які можна експортувати у форматі CSV.
- Візуалізація про кількість вільних та зайнятих паркомісць.


## Головна сторінка

<div align="left" width="569" height="285">
  <img src="readme_screenshots/parking_spots.png">
</div>

## Реєстрація

##









# Підготовка проекту

Через `cmd` ввести команду та після перейти в створену папку

```
git clone https://github.com/Spica12/Python-Science-Parking-Management-System.git
```

Якщо треба встановити віртуальне середовище в папці з проектом, то ввести наступні команди.

Якщо ні - то пропустити цей крок.

```
poetry config --local virtualenvs.in-project true

C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe -m venv .venv

poetry env use .venv\Scripts\python.exe
```

Запустити віртуальне середовище

```
poetry shell
```
# Оновити бібліотеки для контейнерів
```
poetry lock --no-update
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

# Запуск docker-compose

```
docker-compose up --build
```

# Зайти в контейнер з django

```
docker exec -it python-science-parking-management-system-django-1 bash
```

Щоб вийти з контейнера необхідно ввести `exit`

# Виконати міграції бази даних в docker-compose
```
docker-compose exec django python manage.py migrate
```

# Створити суперюзера

Зайти в контейнер django

Ввести команду по створенню суперюзера
```
python manage.py createsuperuser
```
Ввести дані нового юзера

# Створити application
```
python manage.py startapp appname
```
