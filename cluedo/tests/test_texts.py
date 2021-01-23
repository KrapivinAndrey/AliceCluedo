import os
import sys
import inspect
import pytest

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import texts


cases = {
        (("Миссис Пикок", "Мисс Скарлет", "Бильярдная", "Веревка", "Преподобный Грин", 0, 0, 0),
        "МИССИС ПИКОК предположила: МИСС СКАРЛЕТ убила в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПРЕПОДОБНЫЙ ГРИН сказал, что это чушь.")
    }


@pytest.mark.parametrize("params,expected", cases)
def test_text_gossip(params, expected):
    assert texts.text_gossip(*params) == expected
