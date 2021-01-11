import texts
from alice import AliceResponse
from game import GameEngine
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def handler(event: dict, context=None):
    game = GameEngine()
    answer = AliceResponse(event)

    command = event.get('request', {}).get('command', {})
    wait = event.get('state', {}).get('session', {}).get('wait', '')
    it_is_new_game = event.get('session', {}).get('new', False)
    logging.info('command %s', command)
    logging.info('state %s', wait)

    if it_is_new_game:
        text, tts = texts.hello()
        answer.text(text).tts(tts).\
            button("Начать игру").button("Правила")

# Обработчики ПОМОЩЬ

    elif command == 'правила':
        text, tts = texts.rules()
        answer.text(text).tts(tts). \
            button("Начать игру")
    elif command == 'варианты':
        if wait == 'suspect':
            text, tts = texts.cards(wait, game.suspects())
            buttons = game.suspects()
        elif wait == 'room':
            text, tts = texts.cards(wait, game.rooms())
            buttons = game.suspects()
        elif wait == 'weapon':
            text, tts = texts.cards(wait, game.weapons())
            buttons = game.weapons()
        answer.text(text).tts(tts).\
            setButtons(buttons)

    elif command == 'начать игру':
        game.new_game()
        text, tts = texts.start_game(game.playerCards[0], game.playerCards[1], game.playerCards[2])
        answer.text(text).tts(tts).\
            saveState("game", game.dump()).\
            saveState("text", text).\
            saveState("tts", tts).\
            setButtons(['Продолжить', 'Повторить'])
    elif command == 'продолжить':
        # Продолжить вызывается после начала игры и после оглашения хода
        # После этого надо назвать подозреваемого
        text, tts = texts.who_do_you_suspect()
        answer.text(text).tts(tts).\
            saveState("wait", "suspect").\
            setButtons(game.suspects())
    elif wait == 'suspect':  # Ожидали ввод подозреваемых
        player_answer = game.it_is_suspect(command)
        if player_answer:
            text, tts = texts.in_which_room()
            answer.text(text).tts(tts). \
                saveState("wait", "room").\
                saveState('suspect', player_answer).\
                setButtons(game.rooms())
        else:
            text, tts = texts.wrong_answer()
            answer.text(text).tts(tts).\
                setButtons(game.suspects())
    elif wait == 'room':
        player_answer = game.it_is_room(command)
        if player_answer:
            text, tts = texts.what_weapon()
            answer.text(text).tts(tts). \
                saveState("wait", "weapon"). \
                saveState('room', player_answer). \
                setButtons(game.weapons())
        else:
            text, tts = texts.wrong_answer()
            answer.text(text).tts(tts).\
                setButtons(game.rooms())
    elif wait == 'weapon':
        player_answer = game.it_is_weapon(command)
        if player_answer:
            game_state = event.get('state', {}).get('session', {}).get('game', {})
            suspect = event.get('state', {}).get('session', {}).get('suspect')
            room = event.get('state', {}).get('session', {}).get('room', {})
            weapon = player_answer
            game.restore(game_state)
            turn = game.game_turn(suspect, room, weapon)

            if turn.win:
                text, tts = texts.win_game()
                answer.text(text).tts(tts).\
                    end()
            else:
                text, tts = texts.gossip(turn.moves)
                answer.text(text).tts(tts). \
                    saveState("text", text). \
                    saveState("tts", tts). \
                    setButtons(['Продолжить', 'Повторить'])

        else:
            text, tts = texts.wrong_answer()
            answer.text(text).tts(tts). \
                setButtons(game.weapons())

    return answer.body
