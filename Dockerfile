FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/TestProject

RUN pip install pipenv

COPY Pipfile Pipfile.lock /usr/TestProject/
RUN pipenv install --system --deploy
COPY . /usr/TestProject/