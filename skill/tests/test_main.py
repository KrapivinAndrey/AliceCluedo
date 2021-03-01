import pytest
from fluentcheck import Check

import skill.intents as intents
import skill.main as main


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
        "secret": {
            "suspect": "Профессор Плам",
            "room": "Гостиная",
            "weapon": "Веревка",
        },
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


def prepare_request(new=False, intents=None, state_session=None, state_user=None):
    if intents is None:
        intents = {}
    if state_session is None:
        state_session = {}
    if state_user is None:
        state_user = {}
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


def intent(name, slots=None):
    if slots is None:
        slots = []
    return {name: {"slots": slots}}


def get_next_scene(answer):
    return answer["session_state"].get("scene", None)


# region Fixture


@pytest.fixture()
def new_session():
    return prepare_request(new=True)


@pytest.fixture()
def help_session():
    return prepare_request(
        intents=intent(intents.HELP), state_session={"scene": "Welcome"}
    )


@pytest.fixture()
def start_session():
    return prepare_request(
        intents=intent(intents.NEW_GAME), state_session={"scene": "Welcome"}
    )


@pytest.fixture()
def need_help_welcome():
    return prepare_request(
        intents=intent(intents.HELP), state_session={"scene": "Welcome"}
    )


# endregion

# region start


def test_hello(new_session):
    ans = main.handler(new_session, None)
    Check(ans).is_not_none().is_dict().has_keys("response")
    Check(ans.get("response", {})).is_not_none().is_dict().has_keys("text", "tts")
    Check(ans["response"]["text"]).is_not_none().is_string().matches("^Привет!.*")
    Check(get_next_scene(ans)).is_not_none().is_string().matches("Welcome")


def test_help(help_session):
    ans = main.handler(help_session, None)
    Check(ans).is_not_none().is_dict().has_keys("response")
    Check(ans.get("response", {})).is_not_none().is_dict().has_keys("text", "tts")
    Check(get_next_scene(ans)).is_not_none().is_string().matches("HelpMenu")


def test_start(start_session):
    ans = main.handler(start_session, None)
    Check(ans).is_not_none().is_dict().has_keys("response")
    Check(ans.get("response", {})).is_not_none().is_dict().has_keys("text", "tts")
    Check(get_next_scene(ans)).is_not_none().is_string().matches("NewGame")

# endregion

# region Меню помощью


# endregion
