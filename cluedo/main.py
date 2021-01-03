import texts


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

    if event['session']['new']:
        text, tts = texts.hello()

    return response(text, tts, event)
