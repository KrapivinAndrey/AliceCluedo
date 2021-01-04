import json
from types import MethodType


class Chain(object):
    def __getattribute__(self, item):
        fn = object.__getattribute__(self, item)
        if fn and type(fn) == MethodType:
            def chained(*args, **kwargs):
                ans = fn(*args, **kwargs)
                return ans if ans is not None else self
            return chained
        return fn


class AliceResponse(Chain):

    def __init__(self, request):

        self._response_dict = {
            'version': '1.0',
            'session': request['session'],  # для отладки
            'response': {
                'end_session': False,
                'buttons': []
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
        for title in buttons:
            self.add_button(title)

    def add_button(self, title: str, url="", payload="", hide=False):

        button = {
            'title': title,
            'hide': hide
        }
        if url != "":
            button["url"] = url
        if payload != "":
            button["payload"] = payload

        self._response_dict['response']['buttons'].append(button)

    def end(self):
        self._response_dict["response"]["end_session"] = True

    def __str__(self) -> str:
        return self.dumps()

    def get(self, path):
        result = self.body
        for a in path.split('.'):
            result = result[a]
        return result

    @property
    def body(self):
        return self._response_dict.copy()
