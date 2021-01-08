import copy
import random


class GameEngine:

    def __init__(self):
        self._secret = []
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

    def __randomCards(self, num):

        def get_random_card(cards, except_cards):
            random.shuffle(cards)
            while cards[0] in except_cards:
                cards.pop(0)

            return cards[0]

        # Случайный ход, исключая имеющиеся карты
        myCards = self._playerCards[num]
        myCards.append(self.suspects()[num])

        suspect = get_random_card(self.suspects(), myCards)
        room = get_random_card(self.rooms(), myCards)
        weapon = get_random_card(self.weapons(), myCards)

        return suspect, room, weapon

    @staticmethod
    def suspects(full=False):
        result = [
            "Миссис Пикок",
            "Мисс Скарлет",
            "Полковник Мастард",
            "Профессор Плам",
            "Преподобный Грин"
        ]
        if full:
            result.insert(0, "Вы")
        return result

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
            "Зимний сад",
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

        self._secret.append(suspects.pop())
        self._secret.append(rooms.pop())
        self._secret.append(weapons.pop())

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

        def make_suggestion(suspect, room, weapon, index):
            # Обработчик предположения игрока
            suggestion = {suspect, room, weapon}
            i = index + 1
            while i != index:
                cross = set(self._playerCards[i]) & suggestion
                if cross:
                    return self.suspects(True)[i], random.choice(tuple(cross))
                i = (i + 1) % self.num_players

            return None, None

        # Расчет раунда. Передается ход игрока. Возвращается набор ответов
        # Ответ - массив: Ход, Кто опроверг, Какую карту показал(только для игрока)

        # Сначала наш ход
        result = [{
            'player': "Вы",
            'move': (suspect, room, weapon)
        }]

        myMove = make_suggestion(suspect, room, weapon, 0)
        result[0]['player_stop'] = myMove[0]
        result[0]['card'] = myMove[1]
        for i in range(self.num_players-1):
            bot = self.suspects()[i]
            result.append({
                    'player': bot,
                    'move': self.__randomCards(i)
                })



        return result
