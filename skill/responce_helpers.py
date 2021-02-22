GEOLOCATION_ALLOWED = "Geolocation.Allowed"
GEOLOCATION_REJECTED = "Geolocation.Rejected"


def big_image(image_id: list, title=None, description=None):
    big_image = {"type": "BigImage", "image_id": image_id}
    if title:
        big_image["title"] = title
    if description:
        big_image["description"] = description

    return big_image


def image_list(
    image_ids: list,
    header="",
    footer="",
    button_text="",
    button_url="",
    button_payload="",
):
    card = {
        "type": "ItemsList",
        "items": image_ids,
    }
    if header:
        card["header"] = {"text": header}
    if footer or button_text or button_url or button_payload:
        card["footer"] = {}
        if footer:
            card["footer"]["text"] = footer
        if button_text or button_url or button_payload:
            card["footer"]["button"] = {}
            if button_text:
                card["footer"]["button"]["text"] = button_text
            if button_url:
                card["footer"]["button"]["url"] = button_url
            if button_payload:
                card["footer"]["button"]["payload"] = button_payload

    return card


def image_gallery(image_ids: list):
    if image_ids and image_ids[0] != "":

        items = [{"image_id": image_id} for image_id in image_ids]
        return {
            "type": "ImageGallery",
            "items": items,
        }
    else:
        return {}


def image_button(
    image_id: str,
    title="",
    description="",
    button_text="",
    button_url="",
    button_payload="",
):
    image = {
        "image_id": image_id,
    }
    if title:
        image["title"] = title
    if description:
        image["description"] = description
    if button_text or button_url or button_payload:
        button = {}
        if button_text:
            button["text"] = button_text
        if button_url:
            button["url"] = button_url
        if button_payload:
            button["payload"] = button_payload
        image["button"] = button

    return image


def button(title, payload=None, url=None, hide=False):
    button = {
        "title": title,
        "hide": hide,
    }
    if payload is not None:
        button["payload"] = payload
    if url is not None:
        button["url"] = url
    return button


def has_location(event):
    return event["session"].get("location") is not None
