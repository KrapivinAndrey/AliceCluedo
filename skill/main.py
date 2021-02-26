import json

import sentry_sdk

from skill.alice import Request
from skill.scenes import DEFAULT_SCENE, SCENES
from skill.state import STATE_REQUEST_KEY

sentry_sdk.init(
    "https://5514871307bc406499d1c9fe4b088b52@o241410.ingest.sentry.io/5653975",
    traces_sample_rate=1.0,
)


def handler(event, context):

    print(f"REQUEST: {json.dumps(event, ensure_ascii=False)}")

    request = Request(event)
    current_scene_id = event.get("state", {}).get(STATE_REQUEST_KEY, {}).get("scene")
    print(f"Current scene: {current_scene_id}")
    if current_scene_id is None:
        return DEFAULT_SCENE().reply(request)
    current_scene = SCENES.get(current_scene_id, DEFAULT_SCENE)()
    next_scene = current_scene.move(request)
    if next_scene is not None:
        print(f"Moving from scene {current_scene.id()} to {next_scene.id()}")
        return next_scene.reply(request)
    else:
        print(f"Failed to parse user request at scene {current_scene.id()}")
        return current_scene.fallback(request)
