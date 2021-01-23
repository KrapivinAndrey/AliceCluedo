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
        "МИССИС ПИКОК предположила: МИСС СКАРЛЕТ убила в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПРЕПОДОБНЫЙ ГРИН сказал, что это чушь."),
        (("Миссис Пикок", "Мисс Скарлет", "Бильярдная", "Веревка", "Преподобный Грин", 1, 0, 1),
        "МИССИС ПИКОК заявила: МИСС СКАРЛЕТ убила в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПРЕПОДОБНЫЙ ГРИН заявил, чтобы словами зря не бросались."),
        (("Миссис Пикок", "Мисс Скарлет", "Бильярдная", "Веревка", "Преподобный Грин", 2, 0, 2),
        "МИССИС ПИКОК допустила: МИСС СКАРЛЕТ убила в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПРЕПОДОБНЫЙ ГРИН крикнул, что это бред."),
        (("Миссис Пикок", "Мисс Скарлет", "Бильярдная", "Веревка", "Преподобный Грин", 3, 0, 3),
        "МИССИС ПИКОК решила: МИСС СКАРЛЕТ убила в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПРЕПОДОБНЫЙ ГРИН возмутился, что этого не может быть."),
        (("Миссис Пикок", "Мисс Скарлет", "Бильярдная", "Веревка", "Преподобный Грин", 4, 0, 0),
        "МИССИС ПИКОК сказала: МИСС СКАРЛЕТ убила в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПРЕПОДОБНЫЙ ГРИН сказал, что это чушь."),
        (("Миссис Пикок", "Мисс Скарлет", "Бильярдная", "Веревка", "Преподобный Грин", 5, 0, 0),
        "МИССИС ПИКОК обвинила: МИСС СКАРЛЕТ убила в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПРЕПОДОБНЫЙ ГРИН сказал, что это чушь."),

        (("Мисс Скарлет", "Полковник Мастард", "Бильярдная", "Веревка", "Профессор Плам", 0, 0, 0),
        "МИСС СКАРЛЕТ предположила: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПРОФЕССОР ПЛАМ сказал, что это чушь."),
        (("Мисс Скарлет", "Полковник Мастард", "Бильярдная", "Веревка", "Профессор Плам", 1, 0, 1),
        "МИСС СКАРЛЕТ заявила: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПРОФЕССОР ПЛАМ заявил, чтобы словами зря не бросались."),
        (("Мисс Скарлет", "Полковник Мастард", "Бильярдная", "Веревка", "Профессор Плам", 2, 0, 2),
        "МИСС СКАРЛЕТ допустила: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПРОФЕССОР ПЛАМ крикнул, что это бред."),
        (("Мисс Скарлет", "Полковник Мастард", "Бильярдная", "Веревка", "Профессор Плам", 3, 0, 3),
        "МИСС СКАРЛЕТ решила: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПРОФЕССОР ПЛАМ возмутился, что этого не может быть."),
        (("Мисс Скарлет", "Полковник Мастард", "Бильярдная", "Веревка", "Профессор Плам", 4, 0, 0),
        "МИСС СКАРЛЕТ сказала: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПРОФЕССОР ПЛАМ сказал, что это чушь."),
        (("Мисс Скарлет", "Полковник Мастард", "Бильярдная", "Веревка", "Профессор Плам", 5, 0, 0),
        "МИСС СКАРЛЕТ обвинила: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПРОФЕССОР ПЛАМ сказал, что это чушь."),
    
        (("Детектив", "Полковник Мастард", "Бильярдная", "Веревка", "Миссис Пикок", 0, 0, 0),
        "ДЕТЕКТИВ предположил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но МИССИС ПИКОК сказала, что это чушь."),
        (("Детектив", "Полковник Мастард", "Бильярдная", "Веревка", "Миссис Пикок", 1, 0, 1),
        "ДЕТЕКТИВ заявил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но МИССИС ПИКОК заявила, чтобы словами зря не бросались."),
        (("Детектив", "Полковник Мастард", "Бильярдная", "Веревка", "Миссис Пикок", 2, 0, 2),
        "ДЕТЕКТИВ допустил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но МИССИС ПИКОК крикнула, что это бред."),
        (("Детектив", "Полковник Мастард", "Бильярдная", "Веревка", "Миссис Пикок", 3, 0, 3),
        "ДЕТЕКТИВ решил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но МИССИС ПИКОК возмутилась, что этого не может быть."),
        (("Детектив", "Полковник Мастард", "Бильярдная", "Веревка", "Миссис Пикок", 4, 0, 0),
        "ДЕТЕКТИВ сказал: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но МИССИС ПИКОК сказала, что это чушь."),
        (("Детектив", "Полковник Мастард", "Бильярдная", "Веревка", "Миссис Пикок", 5, 0, 0),
        "ДЕТЕКТИВ обвинил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но МИССИС ПИКОК сказала, что это чушь."),
    
        (("Полковник Мастрад", "Полковник Мастард", "Бильярдная", "Веревка", "Детектив", 0, 0, 0),
        "ПОЛКОВНИК МАСТРАД предположил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ДЕТЕКТИВ сказал, что это чушь."),
        (("Полковник Мастрад", "Полковник Мастард", "Бильярдная", "Веревка", "Детектив", 1, 0, 1),
        "ПОЛКОВНИК МАСТРАД заявил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ДЕТЕКТИВ заявил, чтобы словами зря не бросались."),
        (("Полковник Мастрад", "Полковник Мастард", "Бильярдная", "Веревка", "Детектив", 2, 0, 2),
        "ПОЛКОВНИК МАСТРАД допустил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ДЕТЕКТИВ крикнул, что это бред."),
        (("Полковник Мастрад", "Полковник Мастард", "Бильярдная", "Веревка", "Детектив", 3, 0, 3),
        "ПОЛКОВНИК МАСТРАД решил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ДЕТЕКТИВ возмутился, что этого не может быть."),
        (("Полковник Мастрад", "Полковник Мастард", "Бильярдная", "Веревка", "Детектив", 4, 0, 0),
        "ПОЛКОВНИК МАСТРАД сказал: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ДЕТЕКТИВ сказал, что это чушь."),
        (("Полковник Мастрад", "Полковник Мастард", "Бальный зал", "Веревка", "Детектив", 5, 0, 0),
        "ПОЛКОВНИК МАСТРАД обвинил: ПОЛКОВНИК МАСТАРД убил в БАЛЬНОМ ЗАЛЕ, использовав ВЕРЁВКУ. Но ДЕТЕКТИВ сказал, что это чушь."),
    
        (("Профессор Плам", "Полковник Мастард", "Библиотека", "Веревка", "Мисс Скарлет", 0, 0, 0),
        "ПРОФЕССОР ПЛАМ предположил: ПОЛКОВНИК МАСТАРД убил в БИБЛИОТЕКЕ, использовав ВЕРЁВКУ. Но МИСС СКАРЛЕТ сказала, что это чушь."),
        (("Профессор Плам", "Полковник Мастард", "Вестибюль", "Веревка", "Мисс Скарлет", 1, 0, 1),
        "ПРОФЕССОР ПЛАМ заявил: ПОЛКОВНИК МАСТАРД убил в ВЕСТИБЮЛЕ, использовав ВЕРЁВКУ. Но МИСС СКАРЛЕТ заявила, чтобы словами зря не бросались."),
        (("Профессор Плам", "Полковник Мастард", "Кабинет", "Веревка", "Мисс Скарлет", 2, 0, 2),
        "ПРОФЕССОР ПЛАМ допустил: ПОЛКОВНИК МАСТАРД убил в КАБИНЕТЕ, использовав ВЕРЁВКУ. Но МИСС СКАРЛЕТ крикнула, что это бред."),
        (("Профессор Плам", "Полковник Мастард", "Кухня", "Веревка", "Мисс Скарлет", 3, 0, 3),
        "ПРОФЕССОР ПЛАМ решил: ПОЛКОВНИК МАСТАРД убил в КУХНЕ, использовав ВЕРЁВКУ. Но МИСС СКАРЛЕТ возмутилась, что этого не может быть."),
        (("Профессор Плам", "Полковник Мастард", "Гостиная", "Веревка", "Мисс Скарлет", 4, 0, 0),
        "ПРОФЕССОР ПЛАМ сказал: ПОЛКОВНИК МАСТАРД убил в ГОСТИНОЙ, использовав ВЕРЁВКУ. Но МИСС СКАРЛЕТ сказала, что это чушь."),
        (("Профессор Плам", "Полковник Мастард", "Столовая", "Веревка", "Мисс Скарлет", 5, 0, 0),
        "ПРОФЕССОР ПЛАМ обвинил: ПОЛКОВНИК МАСТАРД убил в СТОЛОВОЙ, использовав ВЕРЁВКУ. Но МИСС СКАРЛЕТ сказала, что это чушь."),
    
        (("Преподобный Грин", "Полковник Мастард", "Бильярдная", "Веревка", "Полковник Мастрад", 0, 0, 0),
        "ПРЕПОДОБНЫЙ ГРИН предположил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПОЛКОВНИК МАСТРАД сказал, что это чушь."),
        (("Преподобный Грин", "Полковник Мастард", "Бильярдная", "Веревка", "Полковник Мастрад", 1, 0, 1),
        "ПРЕПОДОБНЫЙ ГРИН заявил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПОЛКОВНИК МАСТРАД заявил, чтобы словами зря не бросались."),
        (("Преподобный Грин", "Полковник Мастард", "Бильярдная", "Веревка", "Полковник Мастрад", 2, 0, 2),
        "ПРЕПОДОБНЫЙ ГРИН допустил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПОЛКОВНИК МАСТРАД крикнул, что это бред."),
        (("Преподобный Грин", "Полковник Мастард", "Бильярдная", "Веревка", "Полковник Мастрад", 3, 0, 3),
        "ПРЕПОДОБНЫЙ ГРИН решил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПОЛКОВНИК МАСТРАД возмутился, что этого не может быть."),
        (("Преподобный Грин", "Полковник Мастард", "Бильярдная", "Веревка", "Полковник Мастрад", 4, 0, 0),
        "ПРЕПОДОБНЫЙ ГРИН сказал: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПОЛКОВНИК МАСТРАД сказал, что это чушь."),
        (("Преподобный Грин", "Полковник Мастард", "Бильярдная", "Веревка", "Полковник Мастрад", 5, 0, 0),
        "ПРЕПОДОБНЫЙ ГРИН обвинил: ПОЛКОВНИК МАСТАРД убил в БИЛЬЯРДНОЙ, использовав ВЕРЁВКУ. Но ПОЛКОВНИК МАСТРАД сказал, что это чушь.")

    }


@pytest.mark.parametrize("params,expected", cases)
def test_text_gossip(params, expected):
    assert texts.text_gossip(*params) == expected
