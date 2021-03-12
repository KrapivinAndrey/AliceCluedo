import inspect
import logging
import sys

import skill.gallery as gallery
import skill.texts as texts
from skill import intents, state
from skill.alice import Request, big_image, button, image_button, image_gallery, image_list
from skill.game import ROOMS, SUSPECTS, WEAPONS, GameEngine
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
            if self.id() == "Welcome":
                button_name = "Начать игру"
            else:
                button_name = "Продолжить"
            return HelpMenu(self.id(), button_name)

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

        if request.session.get("scene", "") == "Suspect":
            buttons = [button(x) for x in SUSPECTS]
            text_, tts_ = texts.who_do_you_suspect()
        elif request.session.get("scene", "") == "Room":
            buttons = [button(x) for x in ROOMS]
            text_, tts_ = texts.in_which_room()
        elif request.session.get("scene", "") == "Weapon":
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
                return Suspect(player_move)
            elif player_move[state.ROOM] is None:
                return Room(player_move)
            elif player_move[state.WEAPON] is None:
                return Weapon(player_move)

    def handle_global_intents(self, request):
        if (
            intents.HELP in request.intents
            or intents.WHAT_CAN_YOU_DO in request.intents
        ):
            return HelpMenu(self.id(), "Продолжить")


# класс меню помощи
class HelpMenuItem(Scene):
    def reply(self, request: Request, text: str, tts: str):
        next_button = request.session[state.NEXT_BUTTON]
        text = (
            text
            + "\n"
            + f"""Скажите "Помощь", чтобы снова получить подсказки.
        Скажите "{next_button}", чтобы вернуться откуда начали"""
        )
        tts = (
            tts
            + "\n"
            + f"""Скажите "Помощь", чтобы снова получить подсказки. sil <[500]>
        Скажите "{next_button}", чтобы вернуться откуда начали"""
        )

        return self.make_response(
            request,
            text,
            tts,
            buttons=[button("Помощь"), button(next_button)],
            state={
                state.PREVIOUS_STATE: request.session[state.PREVIOUS_STATE],
                state.NEXT_BUTTON: next_button,
            },
        )

    def handle_local_intents(self, request: Request):
        if intents.CONTINUE in request.intents:
            return eval(f"{request.session[state.PREVIOUS_STATE]}()")
        elif intents.NEW_GAME in request.intents:
            return NewGame()

    def handle_global_intents(self, request):
        if (
            intents.HELP in request.intents
            or intents.WHAT_CAN_YOU_DO in request.intents
        ):
            return HelpMenu(
                request.session[state.PREVIOUS_STATE],
                request.session[state.NEXT_BUTTON],
            )

    def fallback(self, request: Request):
        next_button = request.session[state.NEXT_BUTTON]
        for_save = {}
        # Сохраним важные состояние
        for save in state.MUST_BE_SAVE:
            if save in request.session:
                for_save.update({save: request.session[save]})
        return self.make_response(
            request=request,
            text=texts.help_menu_fallback(next_button),
            state=for_save,
        )


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


class HaveMistake(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.mistake()

        return self.make_response(
            request,
            text,
            tts,
            end_session=True
        )

# region Start new game


class NewGame(GlobalScene):
    def reply(self, request: Request):
        game.new_game()
        text, tts = texts.start_game(
            game.playerCards[0], game.playerCards[1], game.playerCards[2]
        )
        a = 1/0
        return self.make_response(
            request, text, tts, buttons=YES_NO, state={state.GAME: game.dump()}
        )

    def handle_local_intents(self, request: Request):
        if intents.CONFIRM in request.intents:
            return NewGameLite()
        elif intents.REJECT in request.intents:
            return Suspect()


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
            return Suspect()


# endregion

# region Game turn


class Suspect(GameTurn):
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


class Room(GameTurn):
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


class Weapon(GameTurn):
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
        turn = self.turn if self.turn is not None else request.session[state.TURN]

        text, tts = texts.gossip(turn)
        return self.make_response(
            request, text, tts, buttons=YES_NO, state={state.TURN: self.turn}
        )

    def handle_local_intents(self, request: Request):
        if intents.CONFIRM in request.intents or intents.REPEAT in request.intents:
            return EndTour()
        elif intents.REJECT in request.intents:
            return Suspect()


# region Меню помощи


class HelpMenu(GlobalScene):
    def __init__(self, save_state="", next_button=""):
        self.save_state = save_state
        self.next_button = next_button

    def reply(self, request: Request):
        text, tts = texts.help_menu(self.next_button)
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
                        gallery.MENU_LIST,
                        "Лист детектива",
                        "Удобная форма для того, чтобы записывать свои догадки",
                        "Лист",
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
                        "Оружие",
                    ),
                    image_button(
                        gallery.MENU_ROOM,
                        "Комнаты",
                        "Карты комнат, где могли убить",
                        "Комнаты",
                    ),
                ],
            ),
            buttons=[button(self.next_button)],
            state={
                state.PREVIOUS_STATE: self.save_state,
                state.NEXT_BUTTON: self.next_button,
            },
        )

    def handle_local_intents(self, request: Request):
        if intents.RULES in request.intents:
            return Rules()
        elif intents.MENU_LIST in request.intents:
            return DetectiveList()
        elif intents.MENU_SUSPECT in request.intents:
            return AboutCards("suspects")
        elif intents.MENU_ROOMS in request.intents:
            return AboutCards("rooms")
        elif intents.MENU_WEAPONS in request.intents:
            return AboutCards("weapons")
        elif intents.NEW_GAME in request.intents:
            return NewGame()
        elif intents.CONTINUE in request.intents:
            return eval(f"{request.session[state.PREVIOUS_STATE]}()")


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


class AboutCards(HelpMenuItem):
    def __init__(self, type_of_cards=""):
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
