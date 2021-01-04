import os
import sys
import inspect
import pytest

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import alice


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


def test_alice_init(start_session):
    ans = alice.AliceResponse(start_session)
    assert ans is not None
    assert ans.get('session.session_id') == 'f243ae6c-a923-4f64-9662-1511067c8897'


def test_set_text(start_session):
    ans = alice.AliceResponse(start_session)
    ans.set_text('Hello')

    assert ans.get('response.text') == 'Hello'
    assert ans.get('response.tts') == 'Hello'


def test_set_tts(start_session):
    ans = alice.AliceResponse(start_session)
    ans.set_text('Hello').set_tts('Goodbye')
    assert ans.get('response.tts') == 'Goodbye'


def test_add_button(start_session):
    ans = alice.AliceResponse(start_session)
    assert len(ans.get('response.buttons')) == 0
    ans.add_button('test')
    assert len(ans.get('response.buttons')) == 1
    assert ans.get('response.buttons')[0]['title'] == "test"


def test_set_buttons(start_session):
    ans = alice.AliceResponse(start_session)
    buttons = ['Ok', 'Cancel']

    ans.set_buttons(buttons)
    assert len(ans.get('response.buttons')) == 2
    assert ans.get('response.buttons')[0]['title'] == "Ok"
    assert ans.get('response.buttons')[1]['title'] == "Cancel"


