# [Parking Management System](https://accurate-josy-spica-40cb5916.koyeb.app/)

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


## Install

### Підготовка проекту

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

### Запуск PostgresSQL

```
docker run --name pysci_parking -p 5432:5432 -e POSTGRES_PASSWORD=567234 -e POSTGRES_DB=postgres -d postgres
```

Виконати міграції
```
python manage.py migrate
```

### Заповнити .env

```
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=567234
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

BOT_TOKEN=token

SECRET_KEY=key
DEBUG=true
ALGORITHM=algorithm
DJANGO_ALLOWED_HOSTS=

EMAIL_HOST=host.example.ua
EMAIL_PORT=port
EMAIL_HOST_USER=address@example.net
EMAIL_HOST_PASSWORD=password
```

### Запуск застосунку

```
python manage.py runserver
```

## Запуск через docker-compose

```
docker-compose up --build
```

## Development team

1. Team Lead [Spica12](https://github.com/Spica12)
2. Scrum Master [Dmytro Klepats](https://github.com/Klepats)
3. Python Developer [Pelmenoff](https://github.com/Pelmenoff)
4. Python Developer [Vladyslav Bondarenko](https://github.com/VladyslavBon)





















## Screenshots
<details open>
<summary>Реєстрація та вхід</summary>

Головна сторінка

<div align="left" width="569" height="285">
  <img src="readme_screenshots/parking_spots.png">
</div>

Реєстрація

<div align="left" width="569" height="285">
  <img src="readme_screenshots/sign_up.png">
</div>

Вхід в застосунок

<div align="left" width="569" height="285">
  <img src="readme_screenshots/login.png">
</div>

</details>
<details open>
<summary>Admin</summary>

<div align="left" width="569" height="285">
  <img src="readme_screenshots/admin_profile.png">
</div>

<div align="left" width="569" height="285">
  <img src="readme_screenshots/admin_profile_manage.png">
</div>

</details>

<details open>
<summary>Admin Panel</summary>

<div align="left" width="569" height="285">
  <img src="readme_screenshots/admin_panel.png">
</div>


<div align="left" width="569" height="285">
  <img src="readme_screenshots/admin_user_management.png">
</div>

Parking tariffs

<div align="left" width="569" height="285">
  <img src="readme_screenshots/admin_list_tariffs.png">
</div>

<div align="left" width="569" height="285">
  <img src="readme_screenshots/admin_add_tariff.png">
</div>

Vehicles Management

<div align="left" width="569" height="285">
  <img src="readme_screenshots/admin_vehicles_management.png">
</div>

Payments Management

<div align="left" width="569" height="285">
  <img src="readme_screenshots/admin_payments_management.png">
</div>

Parking Spot

<div align="left" width="569" height="285">
  <img src="readme_screenshots/admin_parking_spot_list.png">
</div>

<div align="left" width="569" height="285">
  <img src="readme_screenshots/admin_add_new_parking_spot.png">
</div>

</details>

<details open>
<summary>User</summary>

<div align="left" width="569" height="285">
  <img src="readme_screenshots/user_profile.png">
</div>

<div align="left" width="569" height="285">
  <img src="readme_screenshots/user_profile_manage.png">
</div>

<div align="left" width="569" height="285">
  <img src="readme_screenshots/user_change_password.png">
</div>

<div align="left" width="569" height="285">
  <img src="readme_screenshots/user_reset_password.png">
</div>

User vehicles

<div align="left" width="569" height="285">
  <img src="readme_screenshots/user_my_vehicles.png">
</div>

<div align="left" width="569" height="285">
  <img src="readme_screenshots/user_detail_vehicle.png">
</div>

<div align="left" width="569" height="285">
  <img src="readme_screenshots/user_detail_parking_session.png">
</div>

User payments

<div align="left" width="569" height="285">
  <img src="readme_screenshots/user_payments_list.png">
</div>

User account

<div align="left" width="569" height="285">
  <img src="readme_screenshots/user_my_account.png">
</div>

<div align="left" width="569" height="285">
  <img src="readme_screenshots/user_my_account_deposit.png">
</div>

</details>

</details>
