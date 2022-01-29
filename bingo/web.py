import os
import random
import string
import pathlib
import functools
from typing import Any, TypeVar, Callable, cast

from socketio import ASGIApp, AsyncServer
from starlette.routing import Mount, Route
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette

from .bingo import Bingo

sio = AsyncServer(async_mode="asgi")

GAMES: dict[str, Bingo] = dict()

F = TypeVar("F", bound=Callable[..., Any])


def with_room(func: F) -> F:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):  # type: ignore
        sid = args[0] or kwargs.get("sid")
        for room in sio.rooms(sid):
            if room != sid:
                return await func(room=room, *args, **kwargs)

        return await func(*args, **kwargs)

    return cast(F, wrapper)


async def index(request: Request) -> Response:
    return templates.TemplateResponse(name="index.html", context={"request": request})


async def play(request: Request) -> Response:
    if request.method == "POST":
        form = await request.form()

        if host := bool(form.get("host")):
            code = generate_room_code()

            GAMES[code] = Bingo(code)

        elif code := str(form.get("room", "")):
            pass

        else:
            return RedirectResponse(request.url_for("index"))

    else:
        code = request.query_params.get("room")
        host = request.query_params.get("host") == "True"

    if code not in GAMES.keys() or not code:
        return templates.TemplateResponse(
            name="index.html", context={"request": request, "errors": "That's not the room code!"}
        )

    game = GAMES[code.strip().upper()]

    return templates.TemplateResponse(name="play.html", context={"request": request, "game": game, "host": host})


@sio.on("join")
async def join(sid: str, room: str) -> None:
    sio.enter_room(sid, room=room)


@sio.on("call")
@with_room
async def call(sid: str, room: str) -> None:
    await sio.emit("call", {"callout": GAMES[room].call_number()}, to=room)


@sio.on("check")
@with_room
async def check(sid: str, room: str) -> None:
    await sio.emit("check", {"numbers": GAMES[room].check_answers()}, to=room)


@sio.on("new")
@with_room
async def new(sid: str, room: str) -> None:
    GAMES[room] = Bingo(room)
    await sio.emit("new", to=room)


def generate_room_code() -> str:
    letters = "".join(random.sample(population=string.ascii_uppercase, k=4))
    while letters in GAMES.keys():
        return generate_room_code()

    return letters


starlette_app = Starlette(
    debug=bool(os.getenv("DEBUG", False)),
    routes=[
        Route("/", index),
        Route("/play", play, methods=["GET", "POST"]),
        Mount("/static", StaticFiles(directory=pathlib.Path("bingo", "static")), name="static"),
    ],
)

app = ASGIApp(sio, starlette_app, socketio_path="/ws")

templates = Jinja2Templates(directory=pathlib.Path("bingo", "templates"))
