"""Small, editable exercise for Stage 00.3 static type checking."""


class Greeter:
    def greet(self, name: str) -> str:
        return f"Hello, {name}!"


def greeting(name: str | None) -> str:
    if name is None:
        return "Hello, guest!"
    return Greeter().greet(name)
