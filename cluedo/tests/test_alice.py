import os
import sys
import inspect
from unittest import TestCase

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
    ans = alice.AliceResponse(start_session).body
    assert ans is not None
    assert ans['session']['session_id'] == 'f243ae6c-a923-4f64-9662-1511067c8897'


def test_set_text(start_session):
    ans = alice.AliceResponse(start_session).text('Hello').body

    assert ans['response']['text'] == 'Hello'
    assert ans['response']['tts'] == 'Hello'


def test_set_tts(start_session):
    ans = alice.AliceResponse(start_session).text('Hello').tts('Goodbye').body
    assert ans['response']['tts'] == 'Goodbye'


def test_add_button(start_session):
    ans = alice.AliceResponse(start_session).button('test').body

    assert len(ans['response']['buttons']) == 1
    assert ans['response']['buttons'][0]['text'] == "test"


def test_set_buttons(start_session):
    buttons = ['Ok', 'Cancel']
    ans = alice.AliceResponse(start_session).setButtons(buttons).body

    assert len(ans['response']['buttons']) == 2
    assert ans['response']['buttons'][0]['text'] == "Ok"
    assert ans['response']['buttons'][1]['text'] == "Cancel"


def test_add_one_image(start_session):
    ans = alice.AliceResponse(start_session). \
        image('111', 'test', 'test image').withButton('button').body

    assert ans['card']['type'] == 'BigImage'

    assert ans['card']['image_id'] == '111'
    assert ans['card']['title'] == 'test'
    assert ans['card']['description'] == 'test image'
    assert ans['card']['button']['text'] == 'button'
    assert 'items' not in ans['card']


def test_add_two_images(start_session):
    ans = alice.AliceResponse(start_session). \
        image('111', 'test', 'test image').withButton('button1'). \
        image('222', 'test2', 'test image').withButton('button2').body

    assert ans['card']['type'] == 'ItemList'

    assert 'image_id' not in ans['card']
    assert 'title' not in ans['card']
    assert 'description' not in ans['card']
    assert 'button' not in ans['card']

    assert len(ans['card']['items']) == 2


def test_add_five_images(start_session):
    ans = alice.AliceResponse(start_session). \
        image('111', 'test1', 'test image').withButton('button1'). \
        image('222', 'test2', 'test image').withButton('button2'). \
        image('333', 'test3', 'test image').withButton('button3'). \
        image('444', 'test4', 'test image').withButton('button4'). \
        image('555', 'test5', 'test image').withButton('button5').body

    assert ans['card']['type'] == 'ItemList'

    assert 'image_id' not in ans['card']
    assert 'title' not in ans['card']
    assert 'description' not in ans['card']
    assert 'button' not in ans['card']

    assert len(ans['card']['items']) == 5


def test_add_seven_images(start_session):
    ans = alice.AliceResponse(start_session). \
        image('111', 'test1', 'test image').withButton('button1'). \
        image('222', 'test2', 'test image').withButton('button2'). \
        image('333', 'test3', 'test image').withButton('button3'). \
        image('444', 'test4', 'test image').withButton('button4'). \
        image('555', 'test5', 'test image').withButton('button5'). \
        image('666', 'test6', 'test image').withButton('button6'). \
        image('777', 'test7', 'test image').withButton('button7').body

    assert ans['card']['type'] == 'ImageGallery'

    assert 'image_id' not in ans['card']
    assert 'title' not in ans['card']
    assert 'description' not in ans['card']
    assert 'button' not in ans['card']

    assert len(ans['card']['items']) == 7


def test_header(start_session):
    ans = alice.AliceResponse(start_session).\
        image('111', 'test1', 'test image').withButton('button1').\
        header('test').body

    assert ans['card']['header'] == 'test'
    assert 'footer' not in ans['card']


def test_footer(start_session):
    ans = alice.AliceResponse(start_session).\
        image('111', 'test1', 'test image').withButton('button1').\
        footer('test').body

    assert ans['card']['footer'] == 'test'
    assert 'header' not in ans['card']


def test_header_footer(start_session):
    ans = alice.AliceResponse(start_session).\
        image('111', 'test1', 'test image').withButton('button1').\
        header('up').footer('down').body

    assert ans['card']['header'] == 'up'
    assert ans['card']['footer'] == 'down'
