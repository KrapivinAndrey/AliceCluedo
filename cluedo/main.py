import texts
from alice import AliceResponse
from game import GameEngine
import logging


def response(text, tts, event):

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'tts': tts,
            'end_session': False
        },
        'session_state': {'last_phrase': text}
    }


def handler(event: dict, context=None):
    game = GameEngine()
    answer = AliceResponse(event)

    command = event.get('request', {}).get('command', {})
    state = event.get('state', {}).get('session', {}).get('state', '')
    itIsNewGame = event.get('session', {}).get('new', False)
    logging.info('command %s', command)
    logging.info('state %s', state)

    if itIsNewGame:
        text, tts = texts.hello()
        answer.text(text).tts(tts).\
            button("Начать игру").button("Правила")
    elif command == 'правила':
        text, tts = texts.rules()
        answer.text(text).tts(tts). \
            button("Начать игру")
    elif command == 'начать игру':
        game.new_game()
        text, tts = texts.start_game(game.playerCards[0], game.playerCards[1], game.playerCards[2])
        answer.text(text).tts(tts).\
            saveState("game", game.dump()).\
            saveState("player_answer", []).\
            saveState("text", text).\
            saveState("tts", tts).\
            setButtons(['Продолжить', 'Повторить'])
    elif command == 'продолжить':
        # Продолжить вызывается после начала игры и после оглашения хода
        # После этого надо назвать подозреваемого
        text, tts = texts.suspect()
        answer.text(text).tts(tts).\
            saveState("state", "suspect").button("Варианты")
        for suspect in game.suspects():
            answer.button(suspect)
    elif command == 'варианты':
        text, tts = texts.cards(state, game)
        answer.text(text).tts(tts). \
            saveState("state", "suspect")
        for suspect in game.suspects():
            answer.button(suspect)

    return answer.body
