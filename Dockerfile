FROM alpine:latest

RUN apk add bash python3 python3-dev gcc musl-dev


RUN addgroup -S www-data && adduser -S bingo -G www-data
COPY . /home/bingo/app

WORKDIR /home/bingo/app

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

RUN apk add --no-cache tini

ENTRYPOINT ["/sbin/tini", "--"]

EXPOSE 5000

CMD [ "/usr/bin/python3", "/home/bingo/app/app.py" ]