import random

import pymorphy2

from skill.game import ROOMS, SUSPECTS, WEAPONS

morph = pymorphy2.MorphAnalyzer()


def __get_sex(name_player):
    return str(morph.parse(name_player.split(" ")[0])[0].tag.gender)


def __inflect(word, case):
    return " ".join([morph.parse(x)[-1].inflect(case).word for x in word.split(" ")])


def hello():
    text = """Привет! Почувствуй себя настоящим сыщиком.
    Выдвигай версии, собирай факты и найди виновного.
    Чтобы узнать как играть скажи "Правила".
    Или "Начать", чтобы начать расследование"""
    tts = (
        '<speaker audio="dialogs-upload/'
        "3308dc06-b901-4f7e-8882-beb1b84c0753/"
        '988b4c6d-88dd-4082-8487-1fc587e19311.opus">'
    )
    return text, tts


def start_game(suspect: str, room: str, weapon: str):

    room_text = __inflect(room, {"loct"})
    weapon_text = __inflect(weapon, {"ablt"})

    text = f"""Черт! Знал же, что не надо было идти на эту вечеринку.
            Будет весело, говорили они. Отдохнешь, развеешься.
            В самый разгар мы нашли тело мистера Блэк в подвале.
            Убийца явно один из тех, кто был в доме. Так что за работу!
            Это явно не {suspect.upper()}, мы были вместе почти весь вечер.
            Похоже тело перенесли в подвал. Откуда?
            Большую часть вечеринки я просидел в {room_text.upper()}, но тут еще полно комнат.
            И судя по следам, мистера Блэк не могли убить {weapon_text.upper()}.
            Кто же тогда? Где он убил его? И чем?
            Повторить еще раз, если не успели всех отметить?"""

    tts = """Черт! Знал же, что не надо было идти на эту вечеринку.
                Будет весело, говорили они. Отдохнешь, развеешься.
                <speaker audio="alice-sounds-human-crowd-2.opus">
                В самый разгар мы нашли тело мистера Блэк в подвале.
                Убийца явно один из тех, кто был в доме. Так что за работу!
                Это явно не {suspect}, мы были вместе почти весь вечер.
                Похоже тело перенесли в подвал. Откуда?
                Большую часть вечеринки я просидел в {room_text}, но тут еще полно комнат.
                И судя по следам, мистера Блэк не могли убить {weapon_text}.
                Кто же тогда? Где он убил его? И чем?
                sil <[1500]>
                Повторить еще раз, если не успели всех отметить?"""
    return text, tts


def start_game_lite(suspect: str, room: str, weapon: str):
    text = f"""Вот карты, которые точно не являются загадкой:
    {suspect.upper()}.
    {room.upper()}.
    {weapon.upper()}.
    Повторить еще раз, если не успели всех отметить?"""

    tts = f"""Вот карты, которые точно не являются загадкой:
    {suspect}. sil <[1000]>
    {room}. sil <[1000]>
    {weapon}. sil <[1000]>
    Повторить еще раз, если не успели всех отметить?"""

    return text, tts


def who_do_you_suspect():

    texts = [
        "Кого вы подозреваете?",
        "Кто же убийца, по вашему?",
        "Кто же мог совершить это преступление?",
    ]

    text = random.choice(texts)
    tts = """{}
    Скажите "Варианты", чтобы узнать какие есть подозреваемые""".format(
        text
    )
    return text, tts


def in_which_room():

    texts = [
        "Где произошло преступление?",
        "А в какой комнате мистер Блэк мог быть убит?",
        "Но в какой же комнате?",
    ]

    text = random.choice(texts)

    tts = """{}
    Скажите "Варианты", чтобы узнать какие есть комнаты""".format(
        text
    )
    return text, tts


def what_weapon():

    texts = [
        "Чем был убит мистер Блэк?",
        "Что использовал убийца?",
        "Что послужило орудием преступления?",
    ]

    text = random.choice(texts)

    tts = """{}
    Скажите "Варианты", чтобы узнать возможные предметы""".format(
        text
    )
    return text, tts


def wrong_answer():
    text = """Кажется, вы сделали неверное предположение.
    Попробуйте еще раз или скажите "Помощь" чтобы получить подсказку"""
    tts = text
    return text, tts


def gossip(moves):

    texts = []

    for move in moves:

        suspect = move["move"][0]
        room = move["move"][1]
        weapon = move["move"][2]

        texts.append(
            text_gossip(move["player"], suspect, room, weapon, move["player_stop"])
        )

    texts.insert(1, "Карта: {}".format(moves[0]["card"].upper()))
    text = "\n".join(texts)
    tts = "\nsil <[1000]>".join(texts)

    return text, tts


def text_gossip(
    player: str,
    suspect: str,
    room: str,
    weapon: str,
    player_stop: str,
    think_num=None,
    use_num=None,
    denial_num=None,
) -> str:

    think_list = [
        "предположить",
        "заявить",
        "допустить",
        "решить",
        "сказать",
        "обвинить",
    ]

    use_list = [("использовав", "accs"), ("с помощью", "gent")]

    denial_list1 = ["сказать", "заявить", "крикнуть", "возмутиться"]

    denial_list2 = [
        ", что это чушь.",
        ", чтобы словами зря не бросались.",
        ", что это бред.",
        ", что этого не может быть.",
    ]

    sex = __get_sex(player)
    if think_num is None:
        think_text = random.choice(think_list)
    else:
        think_text = think_list[think_num]
    think = __inflect(think_text, {sex, "VERB"})

    sex = __get_sex(suspect)
    kill = __inflect("убить", {sex, "VERB"})

    room_text = __inflect(room, {"loct", "sing"})

    if use_num is None:
        use_text = random.choice(use_list)
    else:
        use_text = use_list[use_num]
    weapon_text = __inflect(weapon, {use_text[1]})

    use = use_text[0]

    sex = __get_sex(player_stop)
    if denial_num is None:
        denial_text1 = random.choice(denial_list1)
        denial_text2 = random.choice(denial_list2)
    else:
        denial_text1 = denial_list1[denial_num]
        denial_text2 = denial_list2[denial_num]
    denial = __inflect(denial_text1, {sex, "VERB"}) + denial_text2

    text = (
        f"{player.upper()} {think}: {suspect.upper()} {kill} в {room_text.upper()}, "
        f"{use} {weapon_text.upper()}. Но {player_stop.upper()} {denial}"
    )
    return text


def win_game():
    text = tts = """Поздравляем! Вы вычислили убийцу.
    Правосудие восторжествовало.
    Это была сложная задача. Надеюсь Вам понравилось.
    Не забудьте поставить оценку навыку."""
    return text, tts


def goodbye():
    text = """Кажется игра у нас не клеится.
    Ладно. Возвращайтесь в любое время.
    До свидания!"""
    tts = "<speaker audio='alice-sounds-game-loss-3.opus'>" + text
    return text, tts


def help_menu():
    text = """Это меню помощи.
    Скажите "Продолжить", чтобы вернуться в игру."""
    tts = """Это меню помощи.
    Скажите "Правила", я напомню как играть.sil <[1000]>
    Если забыли какие есть карты, то назовите категорию sil <[1000]>
    Подозреваемые sil <[1000]>
    Комнаты sil <[1000]>
    Орудия sil <[1000]>
    Или скажите "Продолжить", чтобы вернуться в игру"""

    return text, tts


def rules():
    text = """Правила игры.
    В игре есть несколько карт подозреваемых, мест преступления и орудий убийства.
    В начале игры вы получите карты, которые точно не являются ответом.
    Каждый ход Вы должны сформулировать версию:
    Кто убил? В какой комнате? Чем совершено преступление?
    Например:
    "Я думаю полковник Мастард убил с помощью веревки в гостиной"
    Если у игрока есть одна из названных карт - он опровергнет вашу версию, показав Вам карту.
    Следующий игрок так же выдвигает версию и может получить опровержение.
    Но какую карту ему показали - Вы не узнаете.
    Ваша задача узнать какие карты были скрыты ото всех.
    Это и будет ответ на загадку.
    Очень удобно отмечать версии в Листе детектива.
    Как его нарисовать можете узнать в меню "Помощь"""

    tts = """Правила игры.
    В игре есть несколько карт подозреваемых, мест преступления и орудий убийства.
    В начале игры вы получите карты, которые т+очно не являются ответом.
    Каждый ход Вы должны сформулировать версию:
    Кто убил? В какой комнате? Чем совершено преступление?
    Например.sil <[500]>
    "Я думаю полковник Мастард убил с помощью веревки в гостиной"
    sil <[500]>
    Если у игрока есть одна из названных карт - он опровергнет вашу версию, показав Вам карту.
    Следующий игрок так же выдвигает версию и может получить опровержение.
    Но какую карту ему показали - Вы не узнаете.
    Ваша задача узнать какие карты были скрыты ото всех.
    sil <[500]>
    Это и будет ответ на загадку.
    Очень удобно отмечать версии в Листе детектива.
    Как его нарисовать можете узнать в меню "Помощь"""

    return text, tts


def detective_list():
    text = """Возьмите лист бумаги. Лучше в клетку, чтобы было удобно рисовать.
    Нарисуйте один широкий столбец.
    Сначала выпишите карты подозреваемых. Запишите следующих:
    {}
    Теперь выпишите карты комнат:
    {}
    И последними выпишите карты орудий преступления:
    {}
    Теперь нарисуйте узкие столбцы по количеству подозреваемых.
    Так вы сможете отмечать у кого какие карты.""".format(
        "\n".join(SUSPECTS), "\n".join(ROOMS), "\n".join(WEAPONS)
    )
    tts = """Возьмите лист бумаги. Лучше в клетку, чтобы было удобно рисовать.
    Нарисуйте один широкий столбец.
    Сначала выпишите карты подозреваемых. Запишите следующих:
    {}
    Теперь выпишите карты комнат:
    {}
    И последними выпишите карты орудий преступления:
    {}
    Теперь нарисуйте узкие столбцы по количеству подозреваемых.
    Так вы сможете отмечать у кого какие карты.
    Скажите "Повторить", чтобы прослушать еще раз""".format(
        "\n sil <[500]>".join(SUSPECTS),
        "\n sil <[500]>".join(ROOMS),
        "\n sil <[500]>".join(WEAPONS),
    )

    return text, tts


def cards(state: str):
    if state == "suspects":  # Подсказать подозреваемых
        head = "Вы подозреваете следующих: \n"
        list_of_cards = SUSPECTS
    elif state == "rooms":  # Подсказать комнату
        head = "В доме есть следующие комнаты: \n"
        list_of_cards = ROOMS
    elif state == "weapons":  # Подсказать подозреваемых
        head = "Возможные орудия убийства: \n"
        list_of_cards = WEAPONS

    text = head + "\n".join(list_of_cards) + "\nПродолжить?"
    tts = head + "\n sil <[500]>".join(list_of_cards) + "\nПродолжить?"

    return text, tts
