import pytest
from skill.game import GameEngine


@pytest.fixture()
def gameState():
    return {
        "secret": ("Преподобный Грин", "Бильярдная", "Нож"),
        "cards": [
            ["Мисс Скарлет", "Библиотека", "Пистолет"],
            ["Кабинет", "Холл", "Веревка"],
            ["Кабинет", "Бальный зал", "Миссис Пикок"],
            ["Кухня", "Гаечный ключ", "Полковник Мастард"],
            ["Гостиная", "Подсвечник", "Порофессор Плам"],
            ["Столовая", "Свинцовая труба"],
        ],
    }


def test_init():
    game = GameEngine()
    assert game is not None


def test_new_game():
    game = GameEngine()
    game.new_game()

    assert len(game._secret) == 3
    assert game._secret["suspect"] in game.suspects()
    assert game._secret["room"] in game.rooms()
    assert game._secret["weapon"] in game.weapons()

    assert len(game._playerCards) == 6
    assert game._playerCards[0][0] in game.suspects()
    assert game._playerCards[0][1] in game.rooms()
    assert game._playerCards[0][2] in game.weapons()


def test_restore(gameState):
    game = GameEngine()
    game.restore(gameState)

    assert len(game._secret) == 3
    assert game._secret[0] in game.suspects()
    assert game._secret[1] in game.rooms()
    assert game._secret[2] in game.weapons()

    assert len(game._playerCards) == 6


def test_game_turn(gameState):
    game = GameEngine()
    game.restore(gameState)

    result = game.game_turn("Преподобный Грин", "Гостиная", "Подсвечник")

    assert not result["win"]

    moves = result["moves"]
    assert len(moves) == 6  # Должны быть ответы для каждого игрока
    assert moves[0]["player"] == "Детектив"
    assert moves[0]["player_stop"] == "Профессор Плам"  # Остановились на данном игроке
    assert moves[0]["card"] in ("Гостиная", "Подсвечник")  # Показал одну из карт


def test_game_win(gameState):
    game = GameEngine()
    game.restore(gameState)

    result = game.game_turn("Преподобный Грин", "Бильярдная", "Нож")
    assert result["win"]
