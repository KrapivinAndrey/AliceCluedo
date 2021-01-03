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


def handler(event, context):

    answer = AliceResponse(event)

    if event['session']['new']:
        text, tts = texts.hello()
        answer.set_text(text)
        answer.set_tts(tts)

    return str(answer)
