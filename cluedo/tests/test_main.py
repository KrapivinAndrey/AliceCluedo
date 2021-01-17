import os
import sys
import inspect
import pytest
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import main


def game_for_test():
    return {
            "cards": [
              [
                "Мисс Скарлет",
                "Кухня",
                "Кубок"
              ],
              [
                "Полковник Мастард",
                "Холл",
                "Столовая"
              ],
              [
                "Бальный зал",
                "Кабинет",
                "Револьвер"
              ],
              [
                "Библиотека",
                "Гаечный ключ",
                "Зимний сад"
              ],
              [
                "Кинжал",
                "Подсвечник",
                "Бильярдная"
              ],
              [
                "Миссис Пикок",
                "Преподобный Грин"
              ]
            ],
            "secret": ("Профессор Плам", "Гостиная", "Веревка")
          }


def meta():
    return {
        "locale": "ru-RU",
        "timezone": "UTC",
        "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
        "interfaces": {
          "screen": {},
          "payments": {},
          "account_linking": {}
        }
      }


def session(new=False):
    return {
        "message_id": 3,
        "session_id": "d825cbef-e7d6-4af9-9810-3ff3f358ac16",
        "skill_id": "3308dc06-b901-4f7e-8882-beb1b84c0753",
        "user": {
          "user_id": "2D3566FF6B2A05868FE43CDCE5D5E167F13EEDCA13DD4B5BD0F656065D0350E9"
        },
        "application": {
          "application_id": "EFFF6BDD6A2D661526BB262D095D4789DE7F86EC6AA1C1A7480FB94CD9FB6544"
        },
        "user_id": "EFFF6BDD6A2D661526BB262D095D4789DE7F86EC6AA1C1A7480FB94CD9FB6544",
        "new": new
      }


@pytest.fixture()
def start_session():
    start = {
        "meta": meta(),
        "session": session(True),
        "request": {
            "command": "",
            "original_utterance": "",
            "nlu": {
                "tokens": [],
                "entities": [],
                "intents": {}
            },
            "markup": {
                "dangerous_context": False
            },
            "type": "SimpleUtterance"
        },
        "version": "1.0"
    }

    return start


@pytest.fixture()
def need_rules():
    start = {
        "meta": meta(),
        "session": session(),
        "request": {
            "command": "правила",
            "original_utterance": "Правила",
            "nlu": {
              "tokens": [
                "правила"
              ],
              "entities": [],
              "intents": {}
            },
            "markup": {
              "dangerous_context": False
            },
            "type": "SimpleUtterance"
          },
        "state": {
            "session": {
                "myState": "new_game"
            }
        },
        "version": "1.0"
    }

    return start


@pytest.fixture()
def start_game():
    return {
          "meta": meta(),
          "session": session(),
          "request": {
            "command": "начать",
            "original_utterance": "Начать",
            "nlu": {
              "tokens": [
                "начать"
              ],
              "entities": [],
              "intents": {}
            },
            "markup": {
              "dangerous_context": False
            },
            "type": "SimpleUtterance"
          },
          "state": {
            "session": {
                "myState": "new_game"
            },
            "user": {},
            "application": {}
          },
          "version": "1.0"
    }


@pytest.fixture()
def repeat():
    return {
            "meta": meta(),
            "session": session(),
            "request": {
                "command": "повторить",
                "original_utterance": "Повторить",
                "nlu": {
                  "tokens": [
                    "повторить"
                  ],
                  "entities": [],
                  "intents": {}
                },
                "markup": {
                  "dangerous_context": False
                },
                "type": "SimpleUtterance"
              },
            "state": {
                "session": {
                    "myState": "list",
                    "game": game_for_test(),
                    "previous": [
                        "test_text",
                        "test_tts",
                        [
                        "test_button"
                        ]
                    ]
                },
                "user": {},
                "application": {}
              },
            "version": "1.0"
        }


@pytest.fixture()
def first_answer_right():
    return {
      "meta": meta(),
      "session": session(),
      "request": {
        "command": "миссис пикок",
        "original_utterance": "Миссис Пикок",
        "nlu": {
          "tokens": [
            "миссис",
            "пикок"
          ],
          "entities": [],
          "intents": {}
        },
        "markup": {
          "dangerous_context": False
        },
        "type": "SimpleUtterance"
      },
      "state": {
        "session": {
          "game": game_for_test(),
          "text": "Мисс Скарлет Кухня Кубок",
          "tts": "Мисс Скарлет Кухня Кубок",
          "myState": "suspect"
        },
        "user": {},
        "application": {}
      },
      "version": "1.0"
    }


@pytest.fixture()
def first_answer_wrong():
    return {
      "meta": meta(),
      "session": session(),
      "request": {
        "command": "миссис грин",
        "original_utterance": "Миссис Грин",
        "nlu": {
          "tokens": [
            "миссис",
            "грин"
          ],
          "entities": [],
          "intents": {}
        },
        "markup": {
          "dangerous_context": False
        },
        "type": "SimpleUtterance"
      },
      "state": {
        "session": {
          "game": game_for_test(),
          "text": "Мисс Скарлет Кухня Кубок",
          "tts": "Мисс Скарлет Кухня Кубок",
          "myState": "suspect"
        },
        "user": {},
        "application": {}
      },
      "version": "1.0"
    }


@pytest.fixture()
def win_answer():
    return {
        "meta": meta(),
        "session": session(),
        "request": {
            "command": "веревка",
            "original_utterance": "Веревка",
            "nlu": {
                "tokens": [
                    "веревка"
                ],
                "entities": [],
                "intents": {}
            },
            "markup": {
                "dangerous_context": False
            },
            "type": "SimpleUtterance"
        },
        "state": {
            "session": {
                "game": game_for_test(),
                "suspect": "Профессор Плам",
                "room": "Гостиная",
                "myState": "weapon"
            },
            "user": {},
            "application": {}
        },
        "version": "1.0"
    }


@pytest.fixture()
def not_win_answer():
    return {
        "meta": meta(),
        "session": session(),
        "request": {
            "command": "подсвечник",
            "original_utterance": "Подсвечник",
            "nlu": {
                "tokens": [
                    "веревка"
                ],
                "entities": [],
                "intents": {}
            },
            "markup": {
                "dangerous_context": False
            },
            "type": "SimpleUtterance"
        },
        "state": {
            "session": {
                "game": game_for_test(),
                "suspect": "Профессор Плам",
                "room": "Гостиная",
                "myState": "weapon"
            },
            "user": {},
            "application": {}
        },
        "version": "1.0"
    }


def test_hello(start_session):
    ans = main.handler(start_session)
    assert 'Привет!' in ans['response']['text']
    assert 'Привет!' in ans['response']['tts']
    assert len(ans['response']['buttons']) == 2


def test_rule(need_rules):
    ans = main.handler(need_rules)

    assert 'Правила игры' in ans['response']['text']
    assert 'Правила игры' in ans['response']['tts']
    assert len(ans['response']['buttons']) == 2


def test_new_game(start_game):
    ans = main.handler(start_game)

    assert ans is not None


def test_answer_suspect_right(first_answer_right):
    ans = main.handler(first_answer_right)

    assert ans is not None
    assert ans['session_state']['myState'] == 'room'


def test_answer_suspect_wrong(first_answer_wrong):
    ans = main.handler(first_answer_wrong)

    assert ans is not None
    assert ans['session_state']['myState'] == 'suspect'


def test_win_answer(win_answer):
    ans = main.handler(win_answer)

    assert ans['response']['end_session']


def test_not_win_answer(not_win_answer):
    ans = main.handler(not_win_answer)

    assert len(ans['response']['buttons']) == 2


def test_try_repeat(repeat):
    ans = main.handler(repeat)

    assert ans['response']['text'] == 'test_text'
    assert ans['response']['tts'] == 'test_tts'
