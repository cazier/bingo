from flask import Flask, render_template, url_for
from flask_socketio import SocketIO


from random import shuffle, sample
from pprint import pprint

app = Flask(__name__)
app.config["SECRET_KEY"] = "SocketSecret!"
app.config["DEBUG"] = True
socketio = SocketIO(app)

GAMES = dict()


class Bingo(object):
    def __init__(self, title: str = "BINGO") -> None:
        self.title = title.upper()

        self.boards = {
            l: range((i * 15) + 1, ((i + 1) * 15) + 1) for i, l in enumerate(self.title)
        }

        self.numbers = [(l, n) for l in self.boards.keys() for n in self.boards[l]]
        shuffle(self.numbers)

        self.players = set()

    def generate_board(self) -> list:
        while (
            gen := zip(*(sample(population=v, k=5) for _, v in self.boards.items()))
        ) in self.players:
            pass

        self.players.add(gen)

        return gen

    def call_number(self) -> int:
        return "".join({str(i) for i in self.numbers.pop()})


@app.route("/")
def index():
    GAMES[0] = Bingo()
    return render_template(template_name_or_list="index.html")


@socketio.on("call")
def call():
    call = GAMES[0].call_number()
    socketio.emit("call", {"callout": call})


@socketio.on("new")
def new():
    GAMES[0] = Bingo()
    socketio.emit("new")


@app.route("/play")
def play():
    return render_template(template_name_or_list="play.html", game=GAMES[0])


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port="5000")
