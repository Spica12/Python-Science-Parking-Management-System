# Образ Python
FROM python:3.12

RUN pip install poetry
WORKDIR /app

COPY poetry.lock /app/poetry.lock
COPY pyproject.toml /app/pyproject.toml
RUN poetry install

# COPY . /app/
COPY src /app/src
COPY manage.py /app/manage.py


EXPOSE 8000
CMD ["poetry", "run", "python3", "manage.py", "runserver", "0.0.0.0:8000"]
