import copy


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
        import random
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
