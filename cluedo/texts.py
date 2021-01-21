import random
import pymorphy2


morph = pymorphy2.MorphAnalyzer()


def hello():
    text = """Привет! Почувствуй себя настоящим сыщиком.
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
    Кто убил? В какой комнате? Чем совершено преступление?
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
    Кто убил? В какой комнате? Чем совершено преступление?
    Если у игрока есть одна из названных карт - он опровергнет вашу версию, показав Вам карту.
    Следующий игрок так же выдвигает версию и может получить опровержение.
    Но какую карту ему показали - Вы не узнаете.
    Ваша задача узнать какие карты были скрыты ото всех.
    sil <[500]>
    Это и будет ответ на загадку.
    Очень удобно отмечать версии в Листе детектива.
    Хот+ите узнать. к+ак нарисов+ать Лист детектива?
    Заодно познакомитесь с картами"""
    return text, tts


def detective_list(suspects, rooms, weapons):
    text = """Возьмите лист бумаги. Лучше в клетку, чтобы было удобно рисовать.
    Нарисуйте один широкий столбец.
    Сначала выпишите карты подозреваемых. Запишите следующих:
    {}
    Теперь выпишите карты комнат:
    {}
    И последними выпишите карты орудий преступления:
    {}
    Теперь нарисуйте узкие столбцы по количеству подозреваемых.
    Так вы сможете отмечать у кого какие карты.
    Скажите "Начать", чтобы начать расследование.
    Или "Повторить", чтобы прослушать еще раз""".format("\n".join(suspects),
                                                        "\n".join(rooms),
                                                        "\n".join(weapons)
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
    Скажите "Начать", чтобы начать расследование.
    Или "Повторить", чтобы прослушать еще раз""".format("\n sil <[500]>".join(suspects),
                                                        "\n sil <[500]>".join(rooms),
                                                        "\n sil <[500]>".join(weapons)
                                                        )

    return text, tts


def start_game(suspect: str, room: str, weapon: str):

    room_text = morph.parse(room)[0].inflect({'loct'})[0]
    weapon_text = morph.parse(weapon)[0].inflect({'ablt'})[0]

    text = """Черт! Знал же, что не надо было идти на эту вечеринку.
            Будет весело, говорили они. Отдохнешь, развеешься.
            В самый разгар мы нашли тело мистера Блэк в подвале.
            Убийца явно один из тех, кто был в доме. Так что за работу!
            Это явно не {}, мы были вместе почти весь вечер.
            Похоже тело перенесли в подвал. Откуда?
            Большую часть вечеринки я просидел в {}, но тут еще полно комнат.
            И судя по следам, мистера Блэк не могли убить {}.
            Кто же тогда? Где он убил его? И чем?
            Повторить?""".format(suspect.upper(), room_text.upper(), weapon_text.upper())
    tts = """Черт! Знал же, что не надо было идти на эту вечеринку.
                Будет весело, говорили они. Отдохнешь, развеешься.
                <speaker audio="alice-sounds-human-crowd-2.opus">
                В самый разгар мы нашли тело мистера Блэк в подвале.
                Убийца явно один из тех, кто был в доме. Так что за работу!
                Это явно не {}, мы были вместе почти весь вечер.
                Похоже тело перенесли в подвал. Откуда?
                Большую часть вечеринки я просидел в {}, но тут еще полно комнат.
                И судя по следам, мистера Блэк не могли убить {}.
                Кто же тогда? Где он убил его? И чем?
                sil <[500]>
                Повторить?""".format(suspect, room_text, weapon_text)
    return text, tts


def who_do_you_suspect():

    texts = [
        'Кого вы подозреваете?',
        'Кто же убийца, по вашему?',
        'Кто же мог совершить это преступление?'
    ]

    text = """{}
    Скажите "Варианты", чтобы узнать какие есть подозреваемые""".format(random.choice(texts))
    tts = text
    return text, tts


def in_which_room():

    texts = [
        'Где произошло преступление?',
        'А в какой комнате мистер Блэк мог быть убит?',
        'Но в какой же комнате?'
    ]

    text = """{}
    Скажите "Варианты", чтобы узнать какие есть комнаты""".format(random.choice(texts))
    tts = text
    return text, tts


def what_weapon():

    texts = [
        'Чем был убит мистер Блэк?',
        'Что использовал убийца?',
        'Что послужило орудием преступления?'
    ]

    text = """{}
    Скажите "Варианты", чтобы узнать возможные предметы""".format(random.choice(texts))
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

    for move in moves:

        suspect = move['move'][0]
        room = move['move'][1]
        weapon = move['move'][2]

        texts.append(text_gossip(move['player'], suspect, room, weapon, move['player_stop']))

    texts.insert(1, "Показал карту: {}".format(moves[0]['card'].upper()))
    text = '\n'.join(texts)
    tts = '\nsil <[1000]>'.join(texts)

    return text, tts


def text_gossip(player: str, suspect: str, room: str, weapon: str, player_stop: str,
                think_num=None,
                use_num=None,
                denial_num=None) -> str:

    think_list = [
        'предположить',
        'заявить',
        'допустить',
        'решить',
        'сказать',
        'обвинить'
    ]

    use_list = [
        ('использовав', 'accs'),
        ('с помощью', 'gent')
    ]

    denial_list1 = [
        'сказать',
        'заявить',
        'крикнуть'
    ]

    denial_list2 = [
        ', что это чушь.',
        ', чтобы словами не бросались',
        ', что это бред.',
        ', что этого не может быть.'
    ]

    sex = str(morph.parse(player)[0].tag.gender)
    if think_num is None:
        think_text = random.choice(think_list)
    else:
        think_text = think_list[think_num]
    think = morph.parse(think_text)[0].inflect({sex, 'VERB'}).word

    sex = str(morph.parse(suspect.split()[0])[0].tag.gender)
    kill = morph.parse('убить')[0].inflect({sex, 'VERB'}).word

    room_text = ' '.join([morph.parse(x)[0].inflect({'loct'})[0] for x in room.split()])

    if use_num is None:
        use_text = random.choice(use_list)
    else:
        use_text = use_list[use_num]
    weapon_text = ' '.join([morph.parse(x)[0].inflect({use_text[1]})[0] for x in weapon.split()])

    use = use_text[0]

    sex = str(morph.parse(player_stop)[0].tag.gender)
    if denial_num is None:
        denial_text1 = random.choice(denial_list1)
        denial_text2 = random.choice(denial_list2)
    else:
        denial_text1 = denial_list1[denial_num]
        denial_text2 = denial_list2[denial_num]
    denial = morph.parse(denial_text1)[0].inflect({sex, 'VERB'}).word + denial_text2

    text = f'{player.upper()} {think}: {suspect.upper()} {kill} в {room_text.upper()}, ' \
           f'{use} {weapon_text.upper()}. Но {player_stop.upper()} {denial}'
    return text


def win_game():
    text = tts = "Поздравляю"
    return text, tts
