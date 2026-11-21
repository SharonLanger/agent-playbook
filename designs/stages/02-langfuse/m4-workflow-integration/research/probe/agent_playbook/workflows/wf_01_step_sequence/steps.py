"""String operations; no framework or CLI dependency."""


def make_message() -> str:
    return "Hello, workflow!"


def decorate_message(message: str) -> str:
    return f"[{message}]"

