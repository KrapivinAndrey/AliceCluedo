import json
import copy
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

        self._images = []

    def __str__(self) -> str:
        return self.dumps()

    def get(self, path):
        result = self.body
        for a in path.split('.'):
            result = result[a]
        return result

    def dumps(self):
        return json.dumps(
            self._response_dict,
            ensure_ascii=False,
            indent=2
        )

    @staticmethod
    def __button(text: str, url: str, payload: str, hide: bool) -> dict:
        button = {
            'text': text[:64]
        }
        if url:
            button["url"] = url[:1024]
        if payload:
            button["payload"] = payload
        if hide:
            button["hide"] = hide

        return button

    def __prepare_card(self):
        if not self._images:
            raise Exception("No images for card")
        elif len(self._images) == 1:
            result = {
                "type": "BigImage"
            }
            result.update(self._images[0])
        elif len(self._images) <= 5:
            result = {
                "type": "ItemList",
                "items": copy.deepcopy(self._images)
            }
        elif len(self._images) <= 7:
            result = {
                "type": "ImageGallery",
                "items": copy.deepcopy(self._images)
            }
        else:
            raise Exception("Too many images")

        return result

    def text(self, text: str):
        """Установить выводимый текст на экран"""
        self._response_dict['response']['text'] = text[:1024]
        self._response_dict['response']['tts'] = text[:1024]  # по умолчанию произношение совпадает с текстом

    def tts(self, tts: str):
        """Установить произносимую Алисой фразу"""
        self._response_dict['response']['tts'] = tts  # tts может быть длиннее за счет дополнительных звуков

    def setButtons(self, buttons: list):
        """Вывести несколько кнопок

        Параметры:
            buttons -- массив заголовков
        """
        for title in buttons:
            self.button(title)

    def button(self, text: str, url="", payload="", hide=False):
        """Добавить кнопку

        Параметры:
            title -- Текст кнопки, возвращается как выполненная команда request.command
            url -- URL, который должна открывать кнопка
            payload -- Произвольный JSON, который Яндекс.Диалоги должны отправить обработчику,
                        если данная кнопка будет нажата.
            hide -- ризнак того, что кнопку нужно убрать после следующей реплики пользователя.
        """
        button = self.__button(text, url, payload, hide)
        self._response_dict['response']['buttons'].append(button)

    def image(self, image_id: str, title="", description=""):
        self._images.append({
            "image_id": image_id,
            "title": title,
            "description": description
        })

    def withButton(self, title: str, url="", payload=""):
        if not self._images:
            raise Exception("No images")
        self._images[-1]['button'] = self.__button(title, url, payload, False)

    def end(self):
        """Признак конца разговора"""
        self._response_dict["response"]["end_session"] = True

    @property
    def body(self):
        if self._images:
            self._response_dict['card'] = self.__prepare_card()
        return self._response_dict.copy()