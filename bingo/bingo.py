import random

BoardList = dict[str, list[int]]


class Bingo(object):
    def __init__(self, code: str, title: str = "BINGO") -> None:
        self.code = code
        self.title = title.upper()

        self.history: BoardList = {letter: list() for letter in self.title}

        self.boards: BoardList = {l: list(range((i * 15) + 1, ((i + 1) * 15) + 1)) for i, l in enumerate(self.title)}

        self.call_order = [(l, n) for l in self.boards.keys() for n in self.boards[l]]
        random.shuffle(self.call_order)

        self.players_boards: set[tuple[tuple[int]]] = set()

    def generate_board(self) -> tuple[tuple[int]]:
        while True:
            gen = tuple(zip(*(random.sample(v, 5) for v in self.boards.values())))

            if gen not in self.players_boards:
                break

        self.players_boards.add(gen)  # type: ignore

        return gen  # type: ignore

    def call_number(self) -> str:
        letter, number = self.call_order.pop()

        self.history[letter].append(number)

        return f"{letter}-{number}"

    def check_answers(self) -> dict[str, str]:
        return {letter: "<br>".join(map(str, sorted(numbers))) for letter, numbers in self.history.items()}
