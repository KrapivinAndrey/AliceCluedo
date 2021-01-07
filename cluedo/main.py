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


def startGame(aliceAnswer):
    game = GameEngine()
    game.new_game()
    aliceAnswer.saveState(game.dump)


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
