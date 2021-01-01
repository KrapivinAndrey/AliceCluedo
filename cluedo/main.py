INTRO_TEXT = 'Привет! Вы находитесь в приватном навыке "Детектив". ' \
    'Играем в клюэдо.' \
    'Чтобы выйти, скажите "Хватит".'


def handler(event, context):

    text = INTRO_TEXT
    end_session = False

    response = {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': end_session
        },
        'session_state': {'last_phrase': text}
    }

    return response
