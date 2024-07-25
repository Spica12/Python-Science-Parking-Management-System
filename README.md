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
