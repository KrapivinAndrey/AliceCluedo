import os
import sys
import inspect
import pytest
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import main


@pytest.fixture()
def start_session():
    start = {
        "meta": {
            "locale": "ru-RU",
            "timezone": "UTC",
            "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
            "interfaces": {
                "screen": {},
                "payments": {},
                "account_linking": {}
            }
        },
        "session": {
            "message_id": 0,
            "session_id": "f243ae6c-a923-4f64-9662-1511067c8897",
            "skill_id": "3308dc06-b901-4f7e-8882-beb1b84c0753",
            "user": {
                "user_id": "2D3566FF6B2A05868FE43CDCE5D5E167F13EEDCA13DD4B5BD0F656065D0350E9"
            },
            "application": {
                "application_id": "EFFF6BDD6A2D661526BB262D095D4789DE7F86EC6AA1C1A7480FB94CD9FB6544"
            },
            "user_id": "EFFF6BDD6A2D661526BB262D095D4789DE7F86EC6AA1C1A7480FB94CD9FB6544",
            "new": True
        },
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
        "meta": {
            "locale": "ru-RU",
            "timezone": "UTC",
            "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
            "interfaces": {
                "screen": {},
                "payments": {},
                "account_linking": {}
            }
        },
        "session": {
            "message_id": 0,
            "session_id": "f243ae6c-a923-4f64-9662-1511067c8897",
            "skill_id": "3308dc06-b901-4f7e-8882-beb1b84c0753",
            "user": {
                "user_id": "2D3566FF6B2A05868FE43CDCE5D5E167F13EEDCA13DD4B5BD0F656065D0350E9"
            },
            "application": {
                "application_id": "EFFF6BDD6A2D661526BB262D095D4789DE7F86EC6AA1C1A7480FB94CD9FB6544"
            },
            "user_id": "EFFF6BDD6A2D661526BB262D095D4789DE7F86EC6AA1C1A7480FB94CD9FB6544",
            "new": False
        },
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
        "version": "1.0"
    }

    return start


@pytest.fixture()
def start_game():
    return {
          "meta": {
            "locale": "ru-RU",
            "timezone": "UTC",
            "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
            "interfaces": {
              "screen": {},
              "payments": {},
              "account_linking": {}
            }
          },
          "session": {
            "message_id": 1,
            "session_id": "ad9f580b-9582-4873-93d4-2fa5ed79b606",
            "skill_id": "3308dc06-b901-4f7e-8882-beb1b84c0753",
            "user": {
              "user_id": "2D3566FF6B2A05868FE43CDCE5D5E167F13EEDCA13DD4B5BD0F656065D0350E9"
            },
            "application": {
              "application_id": "EFFF6BDD6A2D661526BB262D095D4789DE7F86EC6AA1C1A7480FB94CD9FB6544"
            },
            "user_id": "EFFF6BDD6A2D661526BB262D095D4789DE7F86EC6AA1C1A7480FB94CD9FB6544",
            "new": False
          },
          "request": {
            "command": "начать игру",
            "original_utterance": "Начать игру",
            "nlu": {
              "tokens": [
                "начать",
                "игру"
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
            "session": {},
            "user": {},
            "application": {}
          },
          "version": "1.0"
}


@pytest.fixture()
def full_player_answer():
    return {
      "meta": {
        "locale": "ru-RU",
        "timezone": "UTC",
        "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
        "interfaces": {
          "screen": {},
          "payments": {},
          "account_linking": {}
        }
      },
      "session": {
        "message_id": 5,
        "session_id": "7354f508-2296-4b6b-abfa-b019a26e1d3a",
        "skill_id": "3308dc06-b901-4f7e-8882-beb1b84c0753",
        "user": {
          "user_id": "2D3566FF6B2A05868FE43CDCE5D5E167F13EEDCA13DD4B5BD0F656065D0350E9"
        },
        "application": {
          "application_id": "EFFF6BDD6A2D661526BB262D095D4789DE7F86EC6AA1C1A7480FB94CD9FB6544"
        },
        "user_id": "EFFF6BDD6A2D661526BB262D095D4789DE7F86EC6AA1C1A7480FB94CD9FB6544",
        "new": False
      },
      "request": {
        "command": "кубок",
        "original_utterance": "Кубок",
        "nlu": {
          "tokens": [
            "кубок"
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
          "state": "weapon"
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
    assert len(ans['response']['buttons']) == 1


def test_new_game(start_game):
    ans = main.handler(start_game)

    assert ans is not None


def test_full_answer(full_player_answer):
    ans = main.handler(full_player_answer)

    assert ans is not None
