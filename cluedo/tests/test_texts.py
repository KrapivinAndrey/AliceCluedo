import os
import sys
import inspect
import pytest
import re

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import texts


def test_text_gossip_1():
    result = texts.text_gossip('Детектив', 'Профессор Плам', 'Бальный зал', 'Кинжал', 'Миссис Пикок')

    assert re.match('ДЕТЕКТИВ (предположил|заявил|допустил|решил): ПРОФЕССОР ПЛАМ убил в БАЛЬНОМ ЗАЛЕ (использовав|с помощью) КИНЖАЛ, но МИССИС ПИКОК опроверг', result)


def test_text_gossip_2():
    result = texts.text_gossip('Детектив', 'Мисс Скарлет', 'Мастерская', 'Веревка', 'Преподобный Грин')

    assert re.match('ДЕТЕКТИВ (предположил|заявил|допустил|решил): МИСС СКАРЛЕТ убила в МАСТЕРСКОЙ (использовав|с помощью) ВЕРЁВКУ, но ПРЕПОДОБНЫЙ ГРИН опроверг', result)
