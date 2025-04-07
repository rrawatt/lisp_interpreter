from __future__ import annotations
from typing import Dict, List
from .lispval import LispValue, ListValue

class Environment:
    def __init__(self, outer: Environment | None = None) -> None:
        self.bindings: Dict[str, LispValue] = {}
        self.outer: Environment | None = outer

    def get(self, name: str) -> LispValue:
        if name in self.bindings:
            return self.bindings[name]
        elif self.outer is not None:
            return self.outer.get(name)
        else:
            raise Exception("Undefined symbol: " + name)

    def define(self, name: str, value: LispValue) -> None:
        self.bindings[name] = value

    def set(self, name: str, value: LispValue) -> None:
        if name in self.bindings:
            self.bindings[name] = value
        elif self.outer is not None:
            self.outer.set(name, value)
        else:
            raise Exception("Undefined symbol: " + name)

    def extend(self, parameters: List[str], arguments: List[LispValue]) -> Environment:
        new_env = Environment(outer=self)
        for index, param in enumerate(parameters):
            if index < len(arguments):
                new_env.define(param, arguments[index])
            else:
                new_env.define(param, ListValue())
        return new_env
