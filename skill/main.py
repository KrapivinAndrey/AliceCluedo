import json
import logging
import sys
import os

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from skill.alice import Request
from skill.scenes import DEFAULT_SCENE, SCENES
from skill.state import GAME, PREVIOUS_MOVES, STATE_REQUEST_KEY, TURN
from ga4mp import Ga4mp


root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
root.addHandler(handler)


def handler(event, context):

    # если контекст пустой - это отладка или тесты
    if context is not None:
        sentry_logging = LoggingIntegration(
            level=logging.INFO, event_level=logging.ERROR
        )
        sentry_sdk.init(
            dsn="https://5514871307bc406499d1c9fe4b088b52@o241410.ingest.sentry.io/5653975",
            integrations=[sentry_logging],
            environment="development"
            if os.environ["DEBUG"] == "True"
            else "production",
        )
        ga = Ga4mp(
            measurement_id="2394357485",
            api_secret="c9V4oYkMT6Wk9Ff9fyYq_w",
            client_id="1023363587073-bmd57tv3q01u4ksgis2j3303dmlo3nrc.apps.googleusercontent.com",
        )

    logging.debug(f"REQUEST: {json.dumps(event, ensure_ascii=False)}")
    logging.debug(f"COMMAND: {event['request']['command']}")
    current_scene_id = event.get("state", {}).get(STATE_REQUEST_KEY, {}).get("scene")

    logging.info(f"Current scene: {current_scene_id}")
    request = Request(event)

    try:

        if current_scene_id is None:
            return DEFAULT_SCENE().reply(request)

        current_scene = SCENES.get(current_scene_id, DEFAULT_SCENE)()
        next_scene = current_scene.move(request)

        if next_scene is not None:
            logging.info(f"Moving from scene {current_scene.id()} to {next_scene.id()}")
            return next_scene.reply(request)
        else:
            logging.warning(
                f"Failed to parse user request at scene {current_scene.id()}"
            )
            return current_scene.fallback(request)

    except Exception as e:
        game = request.session.get(GAME, {})
        turn = request.session.get(TURN, {})
        moves = request.session.get(PREVIOUS_MOVES, [])
        logging.exception(e, extra={"game": game, "turn": turn, "moves": moves})
        message = SCENES.get("HaveMistake")()
        return message.reply(request)
