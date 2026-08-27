import json


def encode_event(event) -> bytes:
    return json.dumps(
        event.model_dump(mode="json"),
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")


def decode_event(payload: bytes, model):
    return model.model_validate(json.loads(payload.decode("utf-8")))
