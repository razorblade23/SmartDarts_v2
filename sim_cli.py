"""
This script is intended to be simulation CLI interface for throwing darts.
"""

from enum import Enum

import requests

BASE_URL = "http://localhost:5000"

players = []


class GameType(Enum):
    """Enum for different game types."""

    X01 = "X01"
    CRICKET = "Cricket"


class X01Score(Enum):
    X180 = "180"
    X301 = "301"
    X501 = "501"
    X701 = "701"
    X901 = "901"


class X01Multiplier(Enum):
    SINGLE = "S"
    DOUBLE = "D"
    TRIPLE = "T"


def req_create_game(gametype: GameType) -> str:
    response = requests.post(
        f"{BASE_URL}/game/create", json={"game_type": gametype.value}
    )
    data = response.json()

    if response.ok:
        return data["game_id"]


def req_add_player(game_id: str, player_name: str):
    response = requests.get(
        f"{BASE_URL}/game/{game_id}/add_player", json={"player_name": player_name}
    )
    if response.ok:
        return True


def req_start_game(game_id):
    response = requests.post(f"{BASE_URL}/game/{game_id}/start")
    if response.ok:
        return True


def req_throw_darts(game_id: str, dart: dict[str, int]) -> list:
    response = requests.post(
        f"{BASE_URL}/game/{game_id}/throw",
        json={"dart": dart},
    )
    if response.ok:
        data: dict = response.json()
        status = data.get("status")
        return status


def req_get_game_state(game_id: str):
    response = requests.get(f"{BASE_URL}/game/{game_id}")
    data: dict = response.json()
    states = data.get("states")
    return states


if __name__ == "__main__":
    darts = []

    print("Send darts data like they are thrown at the dartboard")
    print("Every dart is entered individualy just like in real game")
    print()
    print("Dart hit should be entered in format: multiplier:value")
    print("Examples: S:20 | D:15 | T:4 | Q:12")
    print()
    print("Press CTRL+C to quit ...")
    print("-" * 80)

    print(
        "Enter GAME ID fo started game or leave empty to create simulation (4 players -> 501 -> standard)"
    )
    game_id_input = input("Game ID: ")
    if not game_id_input:
        game_id = req_create_game(gametype=GameType.X01)
        req_add_player(game_id=game_id, player_name="Marko")
        req_add_player(game_id=game_id, player_name="Sime")
        req_add_player(game_id=game_id, player_name="Zoran")
        req_add_player(game_id=game_id, player_name="Klapan")
        req_start_game(game_id=game_id)
    else:
        game_id = game_id_input

    while True:
        print()
        dart_input = input("Enter dart to send: ").capitalize().split(":")
        try:
            multiplier = dart_input[0]
            score = dart_input[1]
        except IndexError:
            print("There was an error in proccessing your input, please try again.")
            continue

        if multiplier == "S":
            multiplier = 1
        if multiplier == "D":
            multiplier = 2
        if multiplier == "T":
            multiplier = 3
        if multiplier == "Q":
            multiplier = 4

        dart = {"score": score, "multiplier": multiplier}
        status = req_throw_darts(game_id=game_id, dart=dart)
        print(status)
        print("-" * 80)
