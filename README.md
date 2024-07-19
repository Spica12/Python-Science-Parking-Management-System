# Підготовка проекту

Через `cmd` ввести команду та після перейти в створену папку

```
git clone https://github.com/Spica12/Python-Science-Parking-Management-System.git
```

Якщо треба встановити віртуальне середовище в папці з проектом, то ввести наступні команди.

Якщо ні - то пропустити цей крок.

```
poetry config --local virtualenvs.in-project true

C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe -m venv .venv

poetry env use .venv\bin\Scripts\python.exe
```

Запустити віртуальне середовище

```
poetry shell
```


# Запуск docker-compose

```
docker-compose up --build
```

# Зайти в контейнер з django (щоб вийти з контейнера необхідно ввести `exit`)

```
docker exec -it docker exec -it python-science-parking-management-system-django-1 bash
```

# Виконати міграції бази даних
```
python manage.py migrate
```

# Створити суперюзера

Зайти в контейнер django

Ввести команду по створенню суперюзера та ввести дані
```
python manage.py createsuperuser
```
