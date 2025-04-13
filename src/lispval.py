from __future__ import annotations
from typing import List, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Environment


class LispValue:
    def __init__(self, value_type: str) -> None:
        self.value_type: str = value_type

    def to_string(self) -> str:
        raise NotImplementedError

class Symbol(LispValue):
    def __init__(self, name: str) -> None:
        super().__init__('symbol')
        self.name: str = name

    def to_string(self) -> str:
        return self.name


class Number(LispValue):
    def __init__(self, value: float) -> None:
        super().__init__('number')
        self.value: float = value

    def to_string(self) -> str:
        s: str = str(self.value)
        if s.endswith('.0'):
            s = s[:-2]
        return s


class ListValue(LispValue):
    def __init__(self, elements: List[LispValue] = None) -> None:
        super().__init__('list')
        self.elements: List[LispValue] = elements if elements is not None else []

    def add(self, element: LispValue) -> None:
        self.elements.append(element)

    def to_string(self) -> str:
        return "(" + " ".join(item.to_string() for item in self.elements) + ")"

class Function(LispValue):
    def __init__(self, name: str, func: Callable[[List[LispValue], Environment], LispValue]) -> None:
        super().__init__('function')
        self.name: str = name
        self.func: Callable[[List[LispValue], Environment], LispValue] = func

    def call(self, arguments: List[LispValue], env: Environment) -> LispValue:
        return self.func(arguments, env)

    def to_string(self) -> str:
        return "#<function:" + self.name + ">"

class Lambda(LispValue):
    def __init__(self, parameters: List[str], body: LispValue, env: Environment) -> None:
        super().__init__('lambda')
        self.parameters: List[str] = parameters
        self.body: LispValue = body
        self.env: Environment = env

    def to_string(self) -> str:
        return "#<lambda>"
