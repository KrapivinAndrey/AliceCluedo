import copy
import random


class GameEngine:

    def __init__(self):
        self._secret = tuple()
        self.num_players = 6  # 5 игроков и детектив
        self._playerCards = [[] for i in range(self.num_players)]

    def dump(self):
        return {
            'cards': copy.deepcopy(self._playerCards),
            'secret': self._secret
        }

    def restore(self, state: list):
        self._playerCards = copy.deepcopy(state['cards'])
        self._secret = copy.deepcopy(state['secret'])

    @staticmethod
    def suspects():
        return [
            "Миссис Пикок",
            "Мисс Скарлет",
            "Полковник Мастард",
            "Профессор Плам",
            "Преподобный Грин"
        ]

    @staticmethod
    def players():
        return [
            "Детектив",
            "Миссис Пикок",
            "Мисс Скарлет",
            "Полковник Мастард",
            "Профессор Плам",
            "Преподобный Грин"
        ]

    @staticmethod
    def weapons():
        return [
            "Гаечный ключ",
            "Подсвечник",
            "Кинжал",
            "Кубок",
            "Револьвер",
            "Веревка"
        ]

    @staticmethod
    def rooms():
        return [
            "Бильярдная",
            "Библиотека",
            "Мастерская",
            "Холл",
            "Кабинет",
            "Кухня",
            "Гостиная",
            "Столовая",
            "Бальный зал"
        ]

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

        self._secret = (suspects.pop(), rooms.pop(), weapons.pop())

        #  Ради цельной истоии игруку тоже дадим по одной из каждой колоды
        self._playerCards[0] = [suspects.pop(), rooms.pop(), weapons.pop()]

        all_cards = weapons + rooms + suspects
        random.shuffle(all_cards)

        i = 1
        while all_cards:
            self._playerCards[i].append(all_cards.pop())
            if i == 5:
                i = 1
            else:
                i += 1

    def game_turn(self, suspect, room, weapon):

        def randomCards(index):

            def get_random_card(cards, exclude_cards):
                return random.choice(tuple(set(cards) - set(exclude_cards)))

            # Случайный ход, исключая имеющиеся карты
            myCards = self._playerCards[index]
            myCards.append(self.suspects()[index-1])

            suspect = get_random_card(self.suspects(), myCards)
            room = get_random_card(self.rooms(), myCards)
            weapon = get_random_card(self.weapons(), myCards)

            return suspect, room, weapon

        def make_suggestion(suggestion, index):
            # Обработчик предположения игрока
            i = (index + 1) % self.num_players
            while i != index:
                cross = set(self._playerCards[i]) & suggestion
                if cross:
                    return self.players()[i], random.choice(tuple(cross))
                i = (i + 1) % self.num_players

            return None, None

        def move(suggestion: tuple, index: int) -> dict:
            denial = make_suggestion(set(suggestion), index)
            return {
                'player': self.players()[index],
                'move': suggestion,
                'player_stop': denial[0],
                'card': denial[1]
            }

        # Расчет раунда. Передается ход игрока. Возвращается набор ответов
        # Ответ - массив: Ход, Кто опроверг, Какую карту показал(только для игрока)

        # Сначала наш ход
        mySuggestion = (suspect, room, weapon)

        result = {"win": mySuggestion == self._secret}

        if not result['win']:
            result['moves'] = [move(mySuggestion, 0)]
            for i in range(1, self.num_players):
                result['moves'].append(move(randomCards(i), i))

        return result

    def it_is_suspect(self, suspect: str) -> str:
        for x in self.suspects():
            if suspect == x.lower():
                return x
        return ''

    def it_is_room(self, room: str) -> str:
        for x in self.rooms():
            if room == x.lower():
                return x
        return ''

    def it_is_weapon(self, weapon: str) -> str:
        for x in self.weapons():
            if weapon == x.lower():
                return x
        return ''
