import pytest
from fluentcheck import Check

import skill.intents as intents
import skill.main as main
import skill.state as state


def game_for_test():
    return {
        "cards": [
            ["Мисс Скарлет", "Кухня", "Свинцовая труба"],
            ["Полковник Мастард", "Холл", "Столовая"],
            ["Бальный зал", "Кабинет", "Пистолет"],
            ["Библиотека", "Гаечный ключ", "Зимний сад"],
            ["Нож", "Подсвечник", "Бильярдная"],
            ["Миссис Пикок", "Преподобный Грин"],
        ],
        "secret": ("Профессор Плам", "Гостиная", "Веревка"),
    }


def meta():
    return {
        "locale": "ru-RU",
        "timezone": "UTC",
        "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
        "interfaces": {"screen": {}, "payments": {}, "account_linking": {}},
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
        "new": new,
    }


def prepare_request(new=False, intents={}, state_session={}, state_user={}):
    req = {
        "meta": meta(),
        "session": session(new),
        "request": {
            "command": "",
            "original_utterance": "",
            "nlu": {"tokens": [], "entities": [], "intents": intents},
            "markup": {"dangerous_context": False},
            "type": "SimpleUtterance",
        },
        "version": "1.0",
        "state": {"session": state_session, "user": state_user},
    }

    return req


def intent(name, slots=[]):
    return {name: {"slots": slots}}


# region Fixture


@pytest.fixture()
def start_session():
    return prepare_request(new=True)


@pytest.fixture()
def need_rules():
    return prepare_request(
        intents=intent(intents.RULES), state_session={"scene": state.WELCOME}
    )


@pytest.fixture()
def list_detective():
    return prepare_request(
        intents=intent(intents.CONFIRM), state_session={"scene": state.RULES}
    )


@pytest.fixture()
def start_game():
    return {
        "meta": meta(),
        "session": session(),
        "request": {
            "command": "начать",
            "original_utterance": "Начать",
            "nlu": {"tokens": ["начать"], "entities": [], "intents": {}},
            "markup": {"dangerous_context": False},
            "type": "SimpleUtterance",
        },
        "state": {"session": {"GameState": "new_game"}, "user": {}, "application": {}},
        "version": "1.0",
    }


# endregion

# region start


def test_hello(start_session):
    ans = main.handler(start_session, None)
    Check(ans).is_dict().has_keys("response")
    Check(ans.get("response", {})).is_dict().has_keys("text", "tts")
    Check(ans["response"]["text"]).is_string().matches("^Привет!.*")


def test_rule(need_rules):
    ans = main.handler(need_rules, None)
    Check(ans).is_dict().has_keys("response")
    Check(ans.get("response", {})).is_dict().has_keys("text", "tts")
    Check(ans["response"]["text"]).is_string().matches("^Правила игры")


def test_list(list_detective):
    ans = main.handler(list_detective, None)
    Check(ans).is_dict().has_keys("response")
    Check(ans.get("response", {})).is_dict().has_keys("text", "tts")
    Check(ans["response"]["text"]).is_string().matches("^Возьмите лист бумаги")


def test_new_game(start_game):
    ans = main.handler(start_game, None)
    assert ans


# endregion
