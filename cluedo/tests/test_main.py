import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import main


def test_hello():
    start = {
        'version': 1,
        'session': {
            'new': True
        }
    }
    assert 'Привет!' in main.handler(start, '')
