import skill.main as main
import json
import os

true = True
false = False

with open(os.path.dirname(__file__) + '/emulate_response.json') as json_file:
    REQUEST = json.load(json_file)


def alice():
    main.handler(REQUEST, None)


if __name__ == "__main__":
    alice()
