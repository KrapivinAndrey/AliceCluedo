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


def suspect():
    text = """Кого Вы подозреваете?
                Скажите "Варианты" чтобы узнать варианты"""
    tts = text
    return text, tts


def room():
    text = """Где произошло преступление?
                Скажите "Варианты" чтобы узнать варианты"""
    tts = text
    return text, tts


def weapon():
    text = """Чем был убит?
                Скажите "Варианты" чтобы узнать варианты"""
    tts = text
    return text, tts


def cards(state: str, game):
    text = tts = ''
    if state == 'suspect':  # Подсказать подозреваемых
        text = "Вы подозреваете следующих: \n"
        text += '\n'.join(game.suspects())
        tts = text

    return text, tts
