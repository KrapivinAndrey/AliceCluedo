from abc import ABC, abstractmethod
from typing import Optional

from cluedo.alice import Request
from cluedo.state import STATE_SESSION_RESPONSE_KEY, PERMANENT_VALUES, STATE_REQUEST_KEY


class Scene(ABC):
    def __str__(self):
        return self.__name__

    def __repr__(self):
        return str(self)

    @classmethod
    def id(cls):
        return cls.__name__

    """Генерация ответа сцены"""

    @abstractmethod
    def reply(self, request):
        raise NotImplementedError()

    """Проверка перехода к новой сцене"""

    def move(self, request: Request):
        next_scene = self.handle_local_intents(request)
        if next_scene is None:
            next_scene = self.handle_global_intents(request)
        return next_scene

    @abstractmethod
    def handle_global_intents(self, request):
        raise NotImplementedError()

    @abstractmethod
    def handle_local_intents(self, request: Request) -> Optional[str]:
        raise NotImplementedError()

    @abstractmethod
    def fallback(self, request: Request):
        raise NotImplementedError()

    def make_response(
        self,
        request: Request,
        text,
        tts=None,
        card=None,
        state=None,
        buttons=None,
        directives=None,
        end_session=False,
    ):
        response = {
            "text": text,
            "tts": tts if tts is not None else text,
        }
        if card:
            response["card"] = card
        if buttons:
            response["buttons"] = buttons
        if directives is not None:
            response["directives"] = directives
        if end_session:
            response["end_session"] = end_session
        webhook_response = {
            "response": response,
            "version": "1.0",
            STATE_REQUEST_KEY: {
                "scene": self.id(),
            },
        }
        for key, value in request.session.items():
            if key in PERMANENT_VALUES:
                webhook_response[STATE_SESSION_RESPONSE_KEY][key] = value
        if state is not None:
            webhook_response[STATE_SESSION_RESPONSE_KEY].update(state)
        return webhook_response