import inspect
import sys

import skill.texts as texts
from skill import intents, state
from skill.alice import Request
from skill.game import ROOMS, SUSPECTS, WEAPONS, GameEngine
from skill.responce_helpers import big_image, button, image_gallery
from skill.scenes_util import Scene

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
            if save in request.session:
                save_state.update({save: request.session[save]})
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
        if intents.NEW_GAME in request.intents:
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
        game_state = request.session[state.GAME]
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


class GameTurn(Scene):
    def __init__(self, move=None):
        if move:
            self.player_choose = {k: v for k, v in move.items() if v is not None}
        else:
            self.player_choose = {}

    def reply(self, request: Request):
        pass

    def fallback(self, request):
        pass

    def handle_local_intents(self, request: Request):
        def check_suspect(move, req):
            temp = {
                "Plum": "Профессор Плам",
                "Mustard": "Полковник Мастард",
                "Green": "Преподобный Грин",
                "Peacock": "Миссис Пикок",
                "Scarlet": "Мисс Скарлет",
            }
            if (
                intents.SUSPECT in req.slots(intents.GOSSIP)
                and move[state.SUSPECT] is None
            ):
                move[state.SUSPECT] = temp[req.slot(intents.GOSSIP, intents.SUSPECT)]

        def check_room(move, req):
            temp = {
                "BilliardRoom": "Бильярдная",
                "Library": "Библиотека",
                "Lobby": "Вестибюль",
                "Cabinet": "Кабинет",
                "Kitchen": "Кухня",
                "LivingRoom": "Гостиная",
                "DiningRoom": "Столовая",
                "BallRoom": "Бальный зал",
            }
            if intents.ROOM in req.slots(intents.GOSSIP) and move[state.ROOM] is None:
                move[state.ROOM] = temp[req.slot(intents.GOSSIP, intents.ROOM)]

        def check_weapon(move, req):
            temp = {
                "Wrench": "Гаечный ключ",
                "Candlestick": "Подсвечник",
                "Knife": "Нож",
                "Pipe": "Свинцовая",
                "Gun": "Пистолет",
                "Rope": "Верервка",
            }
            if (
                intents.WEAPON in req.slots(intents.GOSSIP)
                and move[state.WEAPON] is None
            ):
                move[state.WEAPON] = temp[req.slot(intents.GOSSIP, intents.WEAPON)]

        def full_answer(move):
            return (
                move[state.SUSPECT] is not None
                and move[state.ROOM] is not None
                and move[state.WEAPON] is not None
            )

        player_move = {
            state.SUSPECT: request.session.get(state.SUSPECT, None),
            state.ROOM: request.session.get(state.ROOM, None),
            state.WEAPON: request.session.get(state.WEAPON, None),
        }
        if intents.GOSSIP in request.intents:
            check_suspect(player_move, request)
            check_room(player_move, request)
            check_weapon(player_move, request)
            if full_answer(player_move):
                game.restore(request.session.get("game", {}))
                turn = game.game_turn(
                    player_move["suspect"], player_move["room"], player_move["weapon"]
                )

                if turn["win"]:
                    return WinGame()
                else:
                    return EndTour(turn["moves"])
            elif player_move[state.SUSPECT] is None:
                return ChooseSuspect(player_move)
            elif player_move[state.ROOM] is None:
                return ChooseRoom(player_move)
            elif player_move[state.WEAPON] is None:
                return ChooseWeapon(player_move)

    def handle_global_intents(self, request: Request):
        pass


class ChooseSuspect(GameTurn):
    def reply(self, request: Request):
        text, tts = texts.who_do_you_suspect()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[button(x) for x in SUSPECTS],
            state=self.player_choose,
        )


class ChooseRoom(GameTurn):
    def reply(self, request: Request):
        text, tts = texts.in_which_room()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[button(x) for x in ROOMS],
            state=self.player_choose,
        )


class ChooseWeapon(GameTurn):
    def reply(self, request: Request):
        text, tts = texts.what_weapon()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[button(x) for x in WEAPONS],
            state=self.player_choose,
        )


# endregion


class WinGame(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.win_game()
        return self.make_response(request, text, tts, end_session=True)


class EndTour(GlobalScene):
    def __init__(self, turn=None):
        self.turn = turn

    def reply(self, request: Request):
        text, tts = texts.gossip(self.turn)
        return self.make_response(
            request, text, tts, buttons=YES_NO, state={"turn": self.turn}
        )


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
