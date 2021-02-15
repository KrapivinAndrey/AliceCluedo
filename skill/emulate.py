import skill.main as main

true = True
false = False

REQUEST = {
    "meta": {
        "locale": "ru-RU",
        "timezone": "UTC",
        "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
        "interfaces": {
            "screen": {},
            "payments": {},
            "account_linking": {},
            "geolocation_sharing": {},
        },
    },
    "session": {
        "message_id": 1,
        "session_id": "3d3ef0d4-a1d0-45fa-a528-f2b202146403",
        "skill_id": "3308dc06-b901-4f7e-8882-beb1b84c0753",
        "user": {
            "user_id": "2D3566FF6B2A05868FE43CDCE5D5E167F13EEDCA13DD4B5BD0F656065D0350E9"
        },
        "application": {
            "application_id": "EFFF6BDD6A2D661526BB262D095D4789DE7F86EC6AA1C1A7480FB94CD9FB6544"
        },
        "user_id": "EFFF6BDD6A2D661526BB262D095D4789DE7F86EC6AA1C1A7480FB94CD9FB6544",
        "new": false,
    },
    "request": {
        "command": "я думаю убил профессор в столовой",
        "original_utterance": "я думаю убил профессор в столовой",
        "nlu": {
            "tokens": ["я", "думаю", "убил", "профессор", "в", "столовой"],
            "entities": [],
            "intents": {
                "gossip": {
                    "slots": {
                        "suspect": {
                            "type": "Suspect",
                            "tokens": {"start": 3, "end": 4},
                            "value": "Plum",
                        },
                        "room": {
                            "type": "Room",
                            "tokens": {"start": 5, "end": 6},
                            "value": "DiningRoom",
                        },
                    }
                }
            },
        },
        "markup": {"dangerous_context": false},
        "type": "SimpleUtterance",
    },
    "state": {"session": {"scene": "GameTurn"}, "user": {}, "application": {}},
    "version": "1.0",
}


def alice():
    result = main.handler(REQUEST, None)


if __name__ == "__main__":
    alice()
