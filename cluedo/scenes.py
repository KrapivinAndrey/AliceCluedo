import inspect
import sys

from cluedo.alice import Request
from cluedo.responce_helpers import button, image_gallery, big_image
from cluedo.scenes_util import Scene
import cluedo.texts as texts


class GlobalScene(Scene):
    def reply(self, request: Request):
        pass

    def handle_global_intents(self, request):
        if intents.TELL_ABOUT in request.intents:
            return WhoIs()

    def handle_local_intents(self, request: Request):
        pass

    def fallback(self, request: Request):
        save_state = {}
        # Сохраним важные состояние
        for save in state.MUST_BE_SAVE:
            if save in request.state_session:
                save_state.update({save: request.state_session[save]})
        return self.make_response(
            request=request,
            text="Извините, я вас не поняла. Пожалуйста, попробуйте переформулировать вопрос.",
            state=save_state,
        )


class Welcome(GlobalScene):

    def reply(self, request: Request):
        text, tts = texts.hello()

        return self.make_response(
            request,
            text,
            tts,
            buttons=[
                button("Сыграть в викторину"),
                button("Расскажи экскурсию"),
            ],
        )

    def handle_local_intents(self, request: Request):
        pass


def _list_scenes():
    current_module = sys.modules[__name__]
    scenes = []
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and issubclass(obj, Scene):
            scenes.append(obj)
    return scenes


SCENES = {scene.id(): scene for scene in _list_scenes()}

DEFAULT_SCENE = Welcome
