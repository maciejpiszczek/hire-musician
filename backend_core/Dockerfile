FROM python:3.10

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install -U pipenv
RUN pipenv install --system

COPY . .

CMD python manage.py runserver 0.0.0.0:8000
