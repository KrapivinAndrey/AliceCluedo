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
        "message_id": 3,
        "session_id": "83121456-3020-40e3-b932-de95f3885117",
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
        "command": "миссис пикок",
        "original_utterance": "Миссис Пикок",
        "nlu": {
            "tokens": ["миссис", "пикок"],
            "entities": [],
            "intents": {
                "gossip": {
                    "slots": {
                        "suspect": {
                            "type": "Suspect",
                            "tokens": {"start": 0, "end": 2},
                            "value": "Peacock",
                        }
                    }
                }
            },
        },
        "markup": {"dangerous_context": false},
        "type": "SimpleUtterance",
    },
    "state": {
        "session": {
            "scene": "ChooseSuspect",
            "game": {
                "cards": [
                    ["Полковник Мастард", "Кабинет", "Гаечный ключ"],
                    ["Нож", "Преподобный Грин", "Бальный зал"],
                    ["Вестибюль", "Мисс Скарлет", "Подсвечник"],
                    ["Кухня", "Профессор Плам", "Веревка"],
                    ["Бильярдная", "Столовая"],
                    ["Свинцовая труба", "Библиотека"],
                ],
                "secret": {
                    "suspect": "Миссис Пикок",
                    "room": "Гостиная",
                    "weapon": "Пистолет",
                },
            },
        },
        "user": {},
        "application": {},
    },
    "version": "1.0",
}


def alice():
    result = main.handler(REQUEST, None)


if __name__ == "__main__":
    alice()
