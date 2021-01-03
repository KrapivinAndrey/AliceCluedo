import json


class AliceResponse:

    def __init__(self, request):

        self._response_dict = {
            'version': request['version'],
            'session': request['session'],
            'response': {
                'end_session': False
            }
        }

    def dumps(self):
        return json.dumps(
            self._response_dict,
            ensure_ascii=False,
            indent=2
        )

    def set_text(self, text):
        self._response_dict['response']['text'] = text[:1024]
        self._response_dict['response']['tts'] = text[:1024]  # по умолчанию произношение совпадает с текстом

    def set_tts(self, tts):
        self._response_dict['response']['tts'] = tts  # tts может быть длиннее за счет дополнительных звуков

    def set_buttons(self, buttons):
        self._response_dict['response']['buttons'] = buttons

    def end(self):
        self._response_dict["response"]["end_session"] = True

    def __str__(self) -> str:
        return self.dumps()

    def get(self, path):
        result = self._response_dict
        for a in path.split('.'):
            result = result[a]
        return result

    @property
    def body(self):
        return self._response_dict
