import texts
from alice import AliceResponse
from game import GameEngine
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
game = GameEngine()


def handler(event: dict, context=None):

    answer = AliceResponse(event)

    command = event.get('request', {}).get('command', {})
    state = event.get('state', {}).get('session', {}).get('GameState', '')
    it_is_new_game = event.get('session', {}).get('new', False)

# region Dialog

    if it_is_new_game:
        dialog = 'New Game'
    elif state == 'new_game':
        if command == 'правила':
            dialog = 'Rules'
        elif command == 'начать':
            dialog = 'Start'
        else:
            dialog = 'not_understand'
    elif state == 'rules':
        if command == 'да':
            dialog = 'List'
        elif command == 'нет':
            dialog = 'Start'
    elif state == 'list':
        if command == 'повторить':
            dialog = 'List'
        elif command == 'начать':
            dialog = 'Start'
    elif state == 'new_turn':
        if command == 'да':
            dialog = 'Repeat'
        elif command == 'нет':
            dialog = 'Choose suspect'
    elif state == 'suspect':
        player_answer = game.it_is_suspect(command)
        if player_answer:
            dialog = 'Choice room'
        else:
            dialog = 'Wrong_choice_suspect'
    elif state == 'room':
        player_answer = game.it_is_room(command)
        if player_answer:
            dialog = 'Choice weapon'
        else:
            dialog = 'Wrong_choice_room'
    elif state == 'weapon':
        player_answer = game.it_is_weapon(command)
        if player_answer:
            dialog = 'Game turn'
        else:
            dialog = 'Wrong_choice_weapon'

# endregion


# Новая сессия

    if dialog == 'New Game':
        text, tts = texts.hello()
        answer.text(text).tts(tts).\
            saveState('GameState', 'new_game').\
            button("Начать").button("Правила")

# Переход из состояния Новая игра

    elif dialog == 'Rules':
        text, tts = texts.rules()
        answer.text(text).tts(tts).\
            saveState("GameState", "rules").\
            setButtons(['Да', 'Нет'])
    elif dialog == 'List':
        text, tts = texts.detective_list(game.suspects(), game.rooms(), game.weapons())
        answer.text(text).tts(tts). \
            saveState("GameState", 'list').\
            saveState("previous", [text, tts, ['Начать']]). \
            button('Начать').button('Повторить')
    elif dialog == 'Start':
        game.new_game()
        text, tts = texts.start_game(game.playerCards[0], game.playerCards[1], game.playerCards[2])
        answer.text(text).tts(tts). \
            saveState("game", game.dump()). \
            saveState("GameState", 'new_turn').\
            saveState("previous", [text, tts]). \
            button('Да').button('Нет')
    elif dialog == 'Choose suspect':
        text, tts = texts.who_do_you_suspect()
        answer.text(text).tts(tts).\
            saveState("GameState", "suspect").\
            setButtons(game.suspects())
    elif dialog == 'Choice room':
        text, tts = texts.in_which_room()
        answer.text(text).tts(tts). \
            saveState("GameState", "room"). \
            saveState("suspect", player_answer). \
            setButtons(game.rooms())
    elif dialog == 'Choice weapon':
        text, tts = texts.what_weapon()
        answer.text(text).tts(tts). \
            saveState("GameState", "weapon"). \
            saveState("room", player_answer). \
            setButtons(game.weapons())
    elif dialog == 'Wrong_choice_suspect':
        text, tts = texts.wrong_answer()
        answer.text(text).tts(tts). \
            setButtons(game.suspects())
    elif dialog == 'Wrong_choice_room':
        text, tts = texts.wrong_answer()
        answer.text(text).tts(tts). \
            setButtons(game.rooms())
    elif dialog == 'Wrong_choice_weapon':
        text, tts = texts.wrong_answer()
        answer.text(text).tts(tts). \
            setButtons(game.weapons())
    elif dialog == 'Game turn':
        game_state = event.get('state', {}).get('session', {}).get('game', {})
        suspect = event.get('state', {}).get('session', {}).get('suspect')
        room = event.get('state', {}).get('session', {}).get('room', {})
        weapon = player_answer
        game.restore(game_state)
        turn = game.game_turn(suspect, room, weapon)

        if turn['win']:
            text, tts = texts.win_game()
            answer.text(text).tts(tts). \
                end()
        else:
            text, tts = texts.gossip(turn['moves'])
            answer.text(text).tts(tts). \
                saveState("GameState", 'new_turn'). \
                saveState("previous", [text, tts]). \
                button('Да').button('Нет')
    elif command == 'варианты':
        if state == 'suspect':
            text, tts = texts.cards(state, game.suspects())
            buttons = game.suspects()
        elif state == 'room':
            text, tts = texts.cards(state, game.rooms())
            buttons = game.suspects()
        elif state == 'weapon':
            text, tts = texts.cards(state, game.weapons())
            buttons = game.weapons()
        answer.text(text).tts(tts).\
            setButtons(buttons)
    elif dialog == 'Repeat':
        previous = event.get('state', {}).get('session', {}).get('previous', {})
        answer.text(previous[0]).tts(previous[1]).\
            button('Да').button('Нет')

    return answer.body
