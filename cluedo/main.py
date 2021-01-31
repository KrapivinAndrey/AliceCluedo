import json
import logging
import sys

from cluedo.alice import Request
from cluedo.scenes import DEFAULT_SCENE, SCENES
from cluedo.state import STATE_REQUEST_KEY

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


def handler(event, context):

    request = Request(event)

    current_scene_id = event.get("state", {}).get(STATE_REQUEST_KEY, {}).get("scene")
    logging.debug(f"Current scene: {current_scene_id}")
    if current_scene_id is None:
        return DEFAULT_SCENE().reply(request)
    current_scene = SCENES.get(current_scene_id, DEFAULT_SCENE)()
    next_scene = current_scene.move(request)
    logging.debug(f"Next scene: {next_scene}")
    if next_scene is not None:
        logging.info(f"Moving from scene {current_scene.id()} to {next_scene.id()}")
        return next_scene.reply(request)
    else:
        logging.info(f"Failed to parse user request at scene {current_scene.id()}")
        return current_scene.fallback(request)
