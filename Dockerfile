FROM alpine:latest

RUN apk add bash python3 python3-dev gcc musl-dev


RUN addgroup -S www-data && adduser -S bingo -G www-data
COPY . /home/bingo/app

WORKDIR /home/bingo/app

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install gunicorn

RUN apk add --no-cache tini

ENTRYPOINT ["/sbin/tini", "--"]

EXPOSE 5000

<<<<<<< HEAD
CMD [ "gunicorn", "app:app", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000" ]
=======
CMD [ "/usr/bin/python3", "/home/bingo/app/app.py" ]

>>>>>>> 42f6de080db11fcb4cbf0e5c5ae2edc6bd95452a
