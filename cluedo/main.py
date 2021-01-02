INTRO_TEXT = 'Привет! Вы находитесь в приватном навыке "Детектив". ' \
    'Играем в клюэдо.' \
    'Чтобы выйти, скажите "Хватит".'


def response(text, end_session, event):

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': end_session
        },
        'session_state': {'last_phrase': text}
    }


def handler(event, context):

    end_session = False
    if event['session']['new']:
        text = INTRO_TEXT
    else:
        text = 'Давно не виделись'

    return response(text, end_session, event)
