import texts
from alice import AliceResponse
from game import GameEngine
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


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
            saveState("text", text).\
            saveState("tts", tts).\
            setButtons(['Продолжить', 'Повторить'])
    elif command == 'продолжить':
        # Продолжить вызывается после начала игры и после оглашения хода
        # После этого надо назвать подозреваемого
        text, tts = texts.suspect()
        answer.text(text).tts(tts).\
            saveState("state", "suspect").\
            setButtons(game.suspects())
    elif command == 'варианты':
        if state == 'suspect':
            text, tts = texts.cards(state, game.suspects())
            buttons = game.suspects()
        elif state == 'room':
            text, tts = texts.cards(state, game.rooms())
            buttons = game.suspects()
        elif state == 'weapon':
            text, tts = texts.cards(state, game.weapons())
            buttons = game.weapons()
        answer.text(text).tts(tts).\
            saveState("state", state).\
            setButtons(buttons)
    elif state == 'suspect':  # Ожидали ввод подозреваемых
        if command not in [x.lower() for x in game.suspects()]:
            text, tts = texts.wrong_answer()
            answer.text(text).tts(tts).\
                setButtons(game.suspects())
        else:
            text, tts = texts.room()
            answer.text(text).tts(tts). \
                saveState("state", "room").\
                saveState('suspect', command).\
                setButtons(game.rooms())
    elif state == 'room':
        if command not in [x.lower() for x in game.rooms()]:
            text, tts = texts.wrong_answer()
            answer.text(text).tts(tts).\
                setButtons(game.rooms())
        else:
            text, tts = texts.weapon()
            answer.text(text).tts(tts). \
                saveState("state", "weapon").\
                setButtons(game.weapons())
    elif state == 'weapon':
        if command not in [x.lower() for x in game.weapons()]:
            text, tts = texts.wrong_answer()
            answer.text(text).tts(tts).\
                setButtons(game.weapons())
        else:
            pass

    return answer.body
