import inspect
import sys

import skill.gallery as gallery
import skill.texts as texts
from skill import intents, state
from skill.alice import Request
from skill.game import ROOMS, SUSPECTS, WEAPONS, GameEngine
from skill.responce_helpers import (
    big_image,
    button,
    image_button,
    image_gallery,
    image_list,
)
from skill.scenes_util import Scene

game = GameEngine()

# region Базовые классы

# класс общая сцена
class GlobalScene(Scene):
    def reply(self, request: Request):
        pass

    def handle_global_intents(self, request):
        if (
            intents.HELP in request.intents
            or intents.WHAT_CAN_YOU_DO in request.intents
        ):
            return HelpMenu(self.id())

    def handle_local_intents(self, request: Request):
        pass

    def fallback(self, request: Request):
        for_save = {}
        # Сохраним важные состояние
        for save in state.MUST_BE_SAVE:
            if save in request.session:
                for_save.update({save: request.session[save]})
        return self.make_response(
            request=request,
            text="Извините, я вас не понял. Пожалуйста, повторите что Вы сказали",
            state=for_save,
        )


# класс игровой шаг
class GameTurn(Scene):
    def __init__(self, move=None):
        if move:
            self.player_choose = {k: v for k, v in move.items() if v is not None}
        else:
            self.player_choose = {}

    def reply(self, request: Request):
        pass

    def fallback(self, request: Request):

        text, tts = texts.wrong_answer()

        if request.session.get("scene", "") == state.SUSPECT:
            buttons = [button(x) for x in SUSPECTS]
            text_, tts_ = texts.who_do_you_suspect()
        elif request.session.get("scene", "") == state.ROOM:
            buttons = [button(x) for x in ROOMS]
            text_, tts_ = texts.in_which_room()
        elif request.session.get("scene", "") == state.WEAPON:
            buttons = [button(x) for x in WEAPONS]
            text_, tts_ = texts.what_weapon()

        return self.make_response(
            request,
            text + "\n" + text_,
            tts + "sil <[1000]>" + text_,
            buttons=buttons,
            state=self.player_choose,
        )

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
                return suspect(player_move)
            elif player_move[state.ROOM] is None:
                return room(player_move)
            elif player_move[state.WEAPON] is None:
                return weapon(player_move)

    def handle_global_intents(self, request):
        if (
            intents.HELP in request.intents
            or intents.WHAT_CAN_YOU_DO in request.intents
        ):
            return HelpMenu()


# класс меню помощи
class HelpMenuItem(Scene):
    def reply(self, request: Request, text: str, tts: str):
        text = (
            text
            + "\n"
            + """Скажите ""Помощь"", чтобы снова получить подсказки.
        Скажите "Продолжить", чтобы вернуться откуда начали"""
        )
        tts = (
            tts
            + "\n"
            + """Скажите ""Помощь"", чтобы снова получить подсказки. sil <[500]>
        Скажите "Продолжить", чтобы вернуться откуда начали"""
        )

        return self.make_response(
            request,
            text,
            tts,
            buttons=[button("Помощь"), button("Продолжить")],
            state={state.PREVIOUS_STATE: self.id()},
        )

    def handle_local_intents(self, request: Request):
        if (
            intents.HELP in request.intents
            or intents.WHAT_CAN_YOU_DO in request.intents
        ):
            return HelpMenu()

    def handle_global_intents(self, request: Request):
        pass

    def fallback(self, request: Request):
        return self.make_response(
            request=request,
            text="Извините, я вас не понял. Пожалуйста, повторите что Вы сказали",
        )

    @staticmethod
    def go_back(request: Request):
        previous_state = request.session[state.PREVIOUS_STATE]
        return eval(f"{previous_state}()")


# endregion


class Welcome(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.hello()

        return self.make_response(
            request,
            text,
            tts,
            buttons=[
                button("Начать игру"),
                button("Помощь"),
            ],
        )

    def handle_local_intents(self, request: Request):
        if intents.RULES in request.intents:
            return Rules()
        elif intents.NEW_GAME in request.intents:
            return NewGame()


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
            return suspect()


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
            return suspect()


# endregion

# region Game turn


class suspect(GameTurn):
    def reply(self, request: Request):
        text, tts = texts.who_do_you_suspect()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[button(x) for x in SUSPECTS],
            card=image_gallery(gallery.SUSPECTS),
            state=self.player_choose,
        )


class room(GameTurn):
    def reply(self, request: Request):
        text, tts = texts.in_which_room()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[button(x) for x in ROOMS],
            card=image_gallery(gallery.ROOMS),
            state=self.player_choose,
        )


class weapon(GameTurn):
    def reply(self, request: Request):
        text, tts = texts.what_weapon()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[button(x) for x in WEAPONS],
            card=image_gallery(gallery.WEAPONS),
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


# region Меню помощи


class HelpMenu(GlobalScene):
    def __init__(self, save_scene=""):
        self.__save_scene = save_scene

    def reply(self, request: Request):
        text, tts = texts.help_menu()
        return self.make_response(
            request,
            text,
            tts,
            card=image_list(
                [
                    image_button(
                        gallery.MENU_RULE, "Правила", "Правила игры", "Правила"
                    ),
                    image_button(
                        gallery.MENU_SUSPECT,
                        "Подозреваемые",
                        "Карты подозреваемых, кто мог бы убить",
                        "Подозреваемые",
                    ),
                    image_button(
                        gallery.MENU_WEAPON,
                        "Орудия",
                        "Карты орудий преступления, чем могли убить",
                        "Орудия",
                    ),
                    image_button(
                        gallery.MENU_ROOM,
                        "Комнаты",
                        "Карты комнат, где могли убить",
                        "Комнаты",
                    ),
                    image_button(
                        gallery.MENU_NEXT,
                        "Продолжить",
                        "",
                        "Продолжить",
                    ),
                ]
            ),
            state={state.PREVIOUS_SITE: self.__save_scene},
        )

    def handle_local_intents(self, request: Request):
        if intents.RULES in request.intents:
            return Rules()
        elif intents.MENU_SUSPECT in request.intents:
            return tell_cards("suspects")
        elif intents.MENU_ROOMS in request.intents:
            return tell_cards("rooms")
        elif intents.MENU_WEAPONS in request.intents:
            return tell_cards("weapons")
        if intents.CONTINUE in request.intents:
            return eval(f"{request.session[state.PREVIOUS_SITE]}()")


class Rules(HelpMenuItem):
    def reply(self, request: Request):
        text, tts = texts.rules()
        return super().reply(request, text, tts)


class DetectiveList(HelpMenuItem):
    def reply(self, request: Request):
        text, tts = texts.detective_list()
        return super().reply(request, text, tts)

    def handle_local_intents(self, request: Request):
        if intents.REPEAT in request.intents:
            return DetectiveList()
        else:
            return super().handle_local_intents(request)


class tell_cards(HelpMenuItem):
    def __init__(self, type_of_cards: str):
        self.type_of_cards = type_of_cards

    def reply(self, request: Request):
        text, tts = texts.cards(self.type_of_cards)
        return super().reply(request, text, tts)


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
