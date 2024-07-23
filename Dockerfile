# # Образ Python
# FROM python:3.11.2-slim

# RUN pip install poetry
# WORKDIR /app

# COPY poetry.lock /app/poetry.lock
# COPY pyproject.toml /app/pyproject.toml
# RUN poetry install

# # COPY . /app/
# COPY src /app/src
# COPY manage.py /app/manage.py


# EXPOSE 8000
# CMD ["poetry", "run", "python3", "manage.py", "runserver", "0.0.0.0:8000"]


# Образ Python
FROM python:3.11.2-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY /bot /app/bot
COPY /config /app/config
COPY /parking_service /app/parking_service
COPY /vehicles /app/vehicles
COPY /adminapp /app/adminapp
COPY /plate_recognition /app/plate_recognition
COPY /users /app/users
COPY .env /app/.env
COPY manage.py /app/manage.py

EXPOSE 8000
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
