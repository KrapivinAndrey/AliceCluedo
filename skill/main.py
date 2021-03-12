import json
import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from skill.alice import Request
from skill.scenes import DEFAULT_SCENE, SCENES
from skill.state import STATE_REQUEST_KEY

# All of this is already happening by default!
sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)
sentry_sdk.init(
    dsn="https://5514871307bc406499d1c9fe4b088b52@o241410.ingest.sentry.io/5653975",
    integrations=[sentry_logging],
)

logger = logging.getLogger(__name__)


def handler(event, context):

    print(context)

    logger.info(f"REQUEST: {json.dumps(event, ensure_ascii=False)}")
    logger.info(f"COMMAND: {event.get('command')}")
    current_scene_id = event.get("state", {}).get(STATE_REQUEST_KEY, {}).get("scene")

    logger.info(f"Current scene: {current_scene_id}")
    request = Request(event)

    if current_scene_id is None:
        return DEFAULT_SCENE().reply(request)

    current_scene = SCENES.get(current_scene_id, DEFAULT_SCENE)()
    next_scene = current_scene.move(request)

    if next_scene is not None:
        logger.info(f"Moving from scene {current_scene.id()} to {next_scene.id()}")
        return next_scene.reply(request)
    else:
        logger.info(f"Failed to parse user request at scene {current_scene.id()}")
        return current_scene.fallback(request)
