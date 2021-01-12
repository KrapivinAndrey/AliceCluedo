def hello():
    text = """Привет! Почувствуй себя настроящим сыщиком.
        Выдвигай версии, собирай факты и найди виновного.
        Чтобы узнать как играть скажи "Правила".
        Или "Начать", чтобы начать расследование"""
    tts = text
    return text, tts


def rules():
    text = """Правила игры.
            В игре есть несколько карт подозреваемых, мест преступления и орудий.
            В начале игры вы получите карты, которые точно не являются ответом.
            Каждый ход Вы должны сформулировать версию:
            Кто? Где? Чем?
            Если у игрока есть одна из названных карт - он опровергнет вашу версию, показав Вам карту.
            Следующий игрок так же выдвигает версию и может получить опровержение.
            Но какую карту ему показали - Вы не узнаете.
            Ваша задача узнать какие карты были скрыты ото всех.
            Это и будет ответ на загадку.
            Очень удобно отмечать версии в Листе детектива.
            Хотите узнать, как нарисовать Лист детектива? Задодно познакомитесь с картами"""
    tts = """Правила игры.
            В игре есть несколько карт подозреваемых, мест преступления и орудий.
            В начале игры вы получите карты, которые т+очно не являются ответом.
            Каждый ход Вы должны сформулировать версию:
            Кто? Где? Чем?
            Если у игрока есть одна из названных карт - он опровергнет вашу версию, показав Вам карту.
            Следующий игрок так же выдвигает версию и может получить опровержение.
            Но какую карту ему показали - Вы не узнаете.
            Ваша задача узнать какие карты были скрыты ото всех.
            <sil 500>
            Это и будет ответ на загадку.
            Очень удобно отмечать версии в Листе детектива.
            Хот+ите узнать. к+ак нарисов+ать Лист детектива? 
            Заодно познакомитесь с картами"""
    return text, tts


def detective_list(suspects, rooms, weapons):
    text = """Возьмите лист бумаги. Лучше в клеточку, чтобы было удобно рисовать.
            Нарисуйте один широкий столбец.
            Сначала выпишите карты подозреваемых. Запишите следующих:
            {}
            Теперь выпишите карты комнат.
            {}
            И последними выпишите карты орудий преступления.
            {}
            Теперь нарисуйте узкие столбцы по количеству подозреваемых.
            Так вы сможете отмечать у кого какие карты.
            Или "Начать", чтобы начать расследование.
            Или "Повторить", чтобы прослушать еще раз""".format("\n".join(suspects),
                                                                "\n".join(rooms),
                                                                "\n".join(weapons)
                                                                )

    return text, text


def start_game(suspect, room, weapon):
    text = ' '.join([suspect, room, weapon])
    tts = text
    return text, tts


def who_do_you_suspect():
    text = """Кого Вы подозреваете?
    Скажите "Варианты", чтобы узнать возможные варианты"""
    tts = text
    return text, tts


def in_which_room():
    text = """Где произошло преступление?
    Скажите "Варианты", чтобы узнать возможные варианты"""
    tts = text
    return text, tts


def what_weapon():
    text = """Чем был убит?
    Скажите "Варианты", чтобы узнать возможные варианты"""
    tts = text
    return text, tts


def cards(state: str, list_of_cards: list):
    text = ''
    if state == 'suspect':  # Подсказать подозреваемых
        text = "Вы подозреваете следующих: \n"
    elif state == 'room':  # Подсказать комнату
        text = "В доме есть следующие комнаты: \n"
    elif state == 'weapon':  # Подсказать подозреваемых
        text = "Возможные орудия убийства: \n"

    text += '\n'.join(list_of_cards)
    tts = text

    return text, tts


def wrong_answer():
    text = """Нет такого варианта ответа.
    Попробуйте еще раз или скажите "Варианты" чтобы получить подсказку"""
    tts = text
    return text, tts


def gossip(moves):
    texts = []

    # 1. Сначала ход игрока
    player_move = moves[0]
    for move in moves:
        texts.append(
            "{} предположил: {} убил в {} использовав {}, но {} опроверг".format(
                move['player'],
                move['move'][0],
                move['move'][1],
                move['move'][2],
                move['player_stop']
            )
        )

    texts.insert(1, "Показал карту: {}".format(player_move['card']))
    text = '\n'.join(texts)
    tts = text

    return text, tts


def win_game():
    text = tts = "Поздравляю"
    return text, tts
