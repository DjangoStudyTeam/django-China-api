from actstream.actions import action_handler as actstream_action_handler


def action_handler(verb, **kwargs):
    if hasattr(verb, "_proxy____args"):
        verb: str = verb._proxy____args[0]

    if verb.startswith("started "):
        verb = verb[8:]

    return actstream_action_handler(verb, **kwargs)
