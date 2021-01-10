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
                Скажите "Помощь" чтобы узнать варианты"""
    tts = text
    return text, tts


def room():
    text = """Где произошло преступление?
                Скажите "Помощь" чтобы узнать варианты"""
    tts = text
    return text, tts


def weapon():
    text = """Чем был убит?
                Скажите "Помощь" чтобы узнать варианты"""
    tts = text
    return text, tts
