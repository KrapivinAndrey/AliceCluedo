import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def test_hello():
    import main

    start = {
        'version': 1,
        'session': {
            'new': True
        }
    }
    assert 'Привет!' in main.handler(start, '')['response']['text']
