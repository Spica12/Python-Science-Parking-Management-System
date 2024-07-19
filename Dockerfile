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

COPY poetry.lock /app/poetry.lock
COPY pyproject.toml /app/pyproject.toml
COPY requirements.txt /app/requirements.txt
COPY .env /app/.env

RUN pip install -r requirements.txt

COPY src /app/src
COPY manage.py /app/manage.py

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
