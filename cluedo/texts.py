def hello():
    text = """Привет! Вы находитесь в приватном навыке "Детектив".
        Можете узнать правила
        Или начать играть"""
    tts = text
    return text, tts


def rules():
    text = """Правила игры"""
    tts = text
    return text, tts


def start_game(suspect, room, weapon):
    text = ' '.join([suspect, room, weapon])
    tts = text
    return text, tts


def who_do_you_suspect():
    text = """Кого Вы подозреваете?
    Скажите "Варианты" чтобы узнать варианты"""
    tts = text
    return text, tts


def in_which_room():
    text = """Где произошло преступление?
    Скажите "Варианты" чтобы узнать варианты"""
    tts = text
    return text, tts


def what_weapon():
    text = """Чем был убит?
    Скажите "Варианты" чтобы узнать варианты"""
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
