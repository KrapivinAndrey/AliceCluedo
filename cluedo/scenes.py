import inspect
import sys

import cluedo.texts as texts
from cluedo import intents, state
from cluedo.alice import Request
from cluedo.game import ROOMS, SUSPECTS, WEAPONS, GameEngine
from cluedo.responce_helpers import big_image, button, image_gallery
from cluedo.scenes_util import Scene

game = GameEngine()


class GlobalScene(Scene):
    def reply(self, request: Request):
        pass

    def handle_global_intents(self, request):
        pass

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


# region Начало игры


class Welcome(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.hello()

        return self.make_response(
            request,
            text,
            tts,
            buttons=[
                button("Начать игру"),
                button("Правила"),
            ],
        )

    def handle_local_intents(self, request: Request):
        if intents.RULES in request.intents:
            return Rules()
        elif intents.NEW_GAME in request.intents:
            return NewGame()


class Rules(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.rules()
        return self.make_response(request, text, tts, buttons=YES_NO)

    def handle_local_intents(self, request: Request):
        if intents.CONFIRM in request.intents:
            return DetectiveList()
        elif intents.REJECT in request.intents:
            return NewGame()


class DetectiveList(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.detective_list()
        return self.make_response(
            request, text, tts, buttons=[button("Начать игру"), button("Повторить")]
        )

    def handle_local_intents(self, request: Request):
        if intents.NewGame in request.intents:
            return NewGame()
        elif intents.REPEAT in request.intents:
            return DetectiveList()


# endregion

# region Start new game


class NewGame(GlobalScene):
    def reply(self, request: Request):
        game.new_game()
        text, tts = texts.start_game(
            game.playerCards[0], game.playerCards[1], game.playerCards[2]
        )
        return self.make_response(
            request, text, tts, buttons=YES_NO, state={state.GAME: game.dump()}
        )

    def handle_local_intents(self, request: Request):
        if intents.CONFIRM in request.intents:
            return NewGameLite()
        elif intents.REJECT in request.intents:
            return ChooseSuspect()


class NewGameLite(GlobalScene):
    def reply(self, request: Request):
        game_state = request.state_session[state.GAME]
        game.restore(game_state)
        text, tts = texts.start_game_lite(
            game.playerCards[0], game.playerCards[1], game.playerCards[2]
        )
        return self.make_response(
            request, text, tts, buttons=YES_NO, state={state.GAME: game.dump()}
        )

    def handle_local_intents(self, request: Request):
        if intents.CONFIRM in request.intents:
            return NewGameLite()
        elif intents.REJECT in request.intents:
            return ChooseSuspect()


# endregion

# region Game turn


class ChooseSuspect(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.who_do_you_suspect()
        return self.make_response(
            request, text, tts, buttons=[button(x) for x in SUSPECTS]
        )

    def handle_local_intents(self, request: Request):
        if intents.SUSPECT in request.intents:
            return ChooseRoom(request.slots(intents.Suspect)[0])

    def fallback(self, request: Request):
        pass


class ChooseRoom(GlobalScene):
    def __init__(self, suspect: str):
        super.__init__()
        self.suspect = suspect

    def reply(self, request: Request):
        text, tts = texts.in_which_room()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[button(x) for x in ROOMS],
            state={state.SUSPECT: self.suspect},
        )

    def handle_local_intents(self, request: Request):
        if intents.Room in request.intents:
            return ChooseWeapon(request.slots(intents.Room)[0])


class ChooseWeapon(GlobalScene):
    def __init__(self, room: str):
        super.__init__()
        self.room = room

    def reply(self, request: Request):
        text, tts = texts.what_weapon()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[button(x) for x in WEAPONS],
            state={state.WEAPON: self.weapon},
        )

    def handle_local_intents(self, request: Request):
        pass


# endregion


def _list_scenes():
    current_module = sys.modules[__name__]
    scenes = []
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and issubclass(obj, Scene):
            scenes.append(obj)
    return scenes


SCENES = {scene.id(): scene for scene in _list_scenes()}

DEFAULT_SCENE = Welcome
YES_NO = [button("Да"), button("Нет")]
