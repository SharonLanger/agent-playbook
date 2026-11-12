"""Regression checks for the typed example's observable behavior."""

from examples.typing_example import Greeter, greeting


def test_named_greeting() -> None:
    assert Greeter().greet("Sharon") == "Hello, Sharon!"


def test_optional_greeting() -> None:
    assert greeting(None) == "Hello, guest!"
    assert greeting("Sharon") == "Hello, Sharon!"
