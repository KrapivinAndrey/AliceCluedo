import texts
from alice import AliceResponse


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


def handler(event, context=None):

    answer = AliceResponse(event)

    if event['session']['new']:
        text, tts = texts.hello()
        answer.set_text(text).set_tts(tts).\
            add_button("Начать игру").add_button("Правила")

    return answer.body
