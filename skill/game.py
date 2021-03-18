import copy
import random
import logging

SUSPECTS = [
    "Миссис Пикок",
    "Мисс Скарлет",
    "Полковник Мастард",
    "Профессор Плам",
    "Преподобный Грин",
]

WEAPONS = [
    "Гаечный ключ",
    "Подсвечник",
    "Нож",
    "Свинцовая труба",
    "Пистолет",
    "Веревка",
]

ROOMS = [
    "Бильярдная",
    "Библиотека",
    "Вестибюль",
    "Кабинет",
    "Кухня",
    "Гостиная",
    "Столовая",
    "Бальный зал",
]


class GameEngine:
    def __init__(self):
        self._secret = tuple()
        self.num_players = 6  # 5 игроков и детектив
        self._playerCards = [[], [], [], [], [], []]

    def dump(self):
        return {"cards": copy.deepcopy(self._playerCards), "secret": self._secret}

    def restore(self, state: list):
        self._playerCards = copy.deepcopy(state["cards"])
        self._secret = copy.deepcopy(state["secret"])

    @staticmethod
    def suspects():
        return SUSPECTS.copy()

    @staticmethod
    def players():
        return (["Детектив"] + SUSPECTS).copy()

    @staticmethod
    def weapons():
        return WEAPONS.copy()

    @staticmethod
    def rooms():
        return ROOMS.copy()

    @property
    def playerCards(self):
        return self._playerCards[0]

    def new_game(self):
        weapons = self.weapons()
        rooms = self.rooms()
        suspects = self.suspects()

        random.shuffle(suspects)
        random.shuffle(rooms)
        random.shuffle(weapons)

        logging.debug(f"shuffle suspects: {suspects}")
        logging.debug(f"shuffle rooms: {rooms}")
        logging.debug(f"shuffle weapons: {weapons}")

        self._secret = {
            "suspect": suspects.pop(),
            "room": rooms.pop(),
            "weapon": weapons.pop(),
        }

        logging.debug(f"shuffle suspects after secret: {suspects}")
        logging.debug(f"shuffle rooms after secret: {rooms}")
        logging.debug(f"shuffle weapons after secret: {weapons}")

        #  Ради цельной истоии игроку тоже дадим по одной из каждой колоды
        self._playerCards[0] = [suspects.pop(), rooms.pop(), weapons.pop()]

        all_cards = weapons + rooms + suspects
        logging.debug(f"all cards before shuffle: {all_cards}")
        random.shuffle(all_cards)
        logging.debug(f"all cards after shuffle: {all_cards}")

        self._playerCards[1] = [all_cards[0], all_cards[5], all_cards[10]]
        self._playerCards[2] = [all_cards[1], all_cards[6], all_cards[11]]
        self._playerCards[3] = [all_cards[2], all_cards[7], all_cards[12]]
        self._playerCards[4] = [all_cards[3], all_cards[8]]
        self._playerCards[5] = [all_cards[4], all_cards[9]]

    def game_turn(self, suspect, room, weapon):
        def randomCards(index):
            def get_random_card(cards, exclude_cards):
                return random.choice(tuple(set(cards) - set(exclude_cards)))

            # Случайный ход, исключая имеющиеся карты
            my_cards = self._playerCards[index]
            my_cards.append(self.suspects()[index - 1])

            while True:

                s = get_random_card(self.suspects(), my_cards)
                r = get_random_card(self.rooms(), my_cards)
                w = get_random_card(self.weapons(), my_cards)
                if not (s, r, w) == self._secret:
                    break

            return s, r, w

        def make_suggestion(suggestion, index):
            # Обработчик предположения игрока
            turn = (index + 1) % self.num_players
            while turn != index:
                cross = set(self._playerCards[turn]) & suggestion
                if cross:
                    return self.players()[turn], random.choice(tuple(cross))
                turn = (turn + 1) % self.num_players

            return None, None

        def move(suggestion: tuple, index: int) -> dict:
            denial = make_suggestion(set(suggestion), index)
            return {
                "player": self.players()[index],
                "move": suggestion,
                "player_stop": denial[0],
                "card": denial[1],
            }

        # Расчет раунда. Передается ход игрока. Возвращается набор ответов
        # Ответ - массив: Ход, Кто опроверг, Какую карту показал(только для игрока)

        # Сначала наш ход
        my_suggestion = (suspect, room, weapon)

        result = {"win": my_suggestion == self._secret}

        if not result["win"]:
            result["moves"] = [move(my_suggestion, 0)]
            for i in range(1, self.num_players):
                result["moves"].append(move(randomCards(i), i))

        return result
