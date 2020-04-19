from flask import Flask, render_template, url_for, request, abort, session
import flask_socketio

import os

from typing import Iterable
from random import shuffle, sample
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv(
    key="SECRET_KEY", default="correctbatteryhorsestaple"
)
app.config["DEBUG"] = os.getenv(key="DEBUG_APP", default=False)
socketio = flask_socketio.SocketIO(app)

GAMES = dict()


class Bingo(object):
    def __init__(self, code: str, title: str = "BINGO") -> None:
        self.code = code
        self.title = title.upper()

        self.boards = {
            l: range((i * 15) + 1, ((i + 1) * 15) + 1) for i, l in enumerate(self.title)
        }

        self.numbers = [(l, n) for l in self.boards.keys() for n in self.boards[l]]
        shuffle(self.numbers)
        self.callouts = self.numbers[:]

        self.players: set = set()

    def generate_board(self) -> Iterable:
        while (
            gen := zip(*(sample(population=v, k=5) for _, v in self.boards.items()))
        ) in self.players:
            pass

        self.players.add(gen)

        return gen

    def call_number(self) -> str:
        return "-".join((str(i) for i in self.numbers.pop()))

    def check_answers(self) -> str:
        return ", ".join(
            [
                "-".join((str(k) for k in i))
                for i in self.callouts
                if i not in self.numbers
            ][::-1]
        )


@app.route("/", methods=["GET"])
def index():
    return render_template(template_name_or_list="index.html")


@app.route("/play", methods=["GET", "POST"])
def play():
    if request.method == "POST":
        if (host := request.form.get(key="host", default=False, type=bool)) :
            code = generate_room_code()

            GAMES[code] = Bingo(code=code)

        elif (code := request.form.get("room", False)) :
            code = code.upper()
            if code not in GAMES.keys():
                return render_template(
                    template_name_or_list="index.html",
                    errors="That's not the room code!",
                )

        else:
            return abort(500)

        session["host"] = host
        session["code"] = code

    elif request.method == "GET":
        host = session.get("host")
        code = session.get("code")

        if code not in GAMES.keys():
            return render_template(
                template_name_or_list="index.html",
                errors="That room no longer exists. Please make a new one!",
            )

    return render_template(
        template_name_or_list="play.html", game=GAMES[code], host=host
    )


@socketio.on("call")
def call():
    code = rooms(request=request)
    socketio.emit("call", {"callout": GAMES[code].call_number()}, room=code)


@socketio.on("check")
def check():
    code = rooms(request=request)
    socketio.emit("check", {"numbers": GAMES[code].check_answers()}, room=code)


@socketio.on("new")
def new():
    code = rooms(request=request)
    GAMES[code] = Bingo(code)
    socketio.emit("new", room=code)


@socketio.on("join")
def join(data):
    flask_socketio.join_room(room=data)


def generate_room_code() -> str:
    letters = "".join(sample(population=ascii_uppercase, k=4))
    while letters in GAMES.keys():
        return generate_room_code()

    return letters


def rooms(request) -> str:
    return [room for room in flask_socketio.rooms() if room != request.sid][0]


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port="5000")
