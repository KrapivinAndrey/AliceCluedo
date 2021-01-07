import texts
from alice import AliceResponse
from game import GameEngine


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


def startGame(answer):
    game = GameEngine()
    game.new_game()
    answer.text(game.playerCards[0] + game.playerCards[1] + game.playerCards[2]).saveState("game", game.dump())
    for weapon in game.rooms():
        answer.button(weapon)


def handler(event, context=None):

    answer = AliceResponse(event)

    if event['session']['new']:
        text, tts = texts.hello()
        answer.text(text).tts(tts).\
            button("Начать игру").button("Правила")
    elif event['request']['command'] == 'правила':
        text, tts = texts.rules()
        answer.text(text).tts(tts). \
            button("Начать игру")
    elif event['request']['command'] == 'начать игру':
        startGame(answer)

    return answer.body
