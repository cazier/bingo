FROM python:3.9-alpine

RUN adduser -S bingo -G www-data
COPY . /home/bingo/app

WORKDIR /home/bingo/app

RUN pip install pipenv
RUN pipenv install --system

EXPOSE 5000

ENTRYPOINT [ "gunicorn", "bingo.web:app", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:5000" ]
