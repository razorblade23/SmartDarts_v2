import pytest


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    from flask import Flask

    from src.routes.api import api_router

    app = Flask(__name__)
    app.config["TESTING"] = True
    app.secret_key = "test_secret_key"
    app.register_blueprint(api_router, url_prefix="/api")

    with app.test_client() as client:
        yield client


def test_create_game(client):
    """Test game creation."""
    response = client.post("/api/game/create", json={"game_type": "X01"})
    data = response.get_json()

    assert response.status_code == 201
    assert "game_id" in data
    assert data["message"] == "Game created successfully!"


def test_add_player(client):
    """Test adding a player to a game."""
    # Create a game first
    create_response = client.post("/api/game/create", json={"game_type": "X01"})
    game_id = create_response.get_json()["game_id"]

    # Add player
    response = client.get(
        f"/api/game/{game_id}/add_player", json={"player_name": "Alice"}
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == f"Player Alice added to game {game_id}."


def test_start_game(client):
    """Test starting a game."""
    create_response = client.post("/api/game/create", json={"game_type": "X01"})
    game_id = create_response.get_json()["game_id"]

    response = client.post(f"/api/game/{game_id}/start")
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == f"Game {game_id} started."


def test_throw_darts(client):
    """Test throwing darts."""
    create_response = client.post("/api/game/create", json={"game_type": "X01"})
    game_id = create_response.get_json()["game_id"]

    client.get(f"/api/game/{game_id}/add_player", json={"player_name": "Alice"})

    response = client.post(
        f"/game/{game_id}/throw",
        json={"player_name": "Alice", "darts": [{"score": 20, "multiplier": 2}]},
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Player Alice threw darts."
    assert "states" in data


def test_get_game_state(client):
    """Test retrieving game state."""
    create_response = client.post("/api/game/create", json={"game_type": "X01"})
    game_id = create_response.get_json()["game_id"]

    response = client.get(f"/api/game/{game_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert "states" in data


def test_invalid_game_id(client):
    """Test accessing an invalid game ID."""
    response = client.get("/api/game/invalid_id")
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Game with game_id='invalid_id' not found"
