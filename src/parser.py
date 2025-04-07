from __future__ import annotations
from typing import List
from .lispval import LispValue, Symbol, Number, ListValue

def tokenize(source: str) -> List[str]:
    source = source.replace("(", " ( ").replace(")", " ) ")
    return source.split()

def parse(tokens: List[str]) -> LispValue:
    if not tokens:
        raise Exception("Unexpected EOF while reading")
    token: str = tokens.pop(0)
    if token == "(":
        elements: List[LispValue] = []
        while tokens[0] != ")":
            elements.append(parse(tokens))
        tokens.pop(0)  # remove ')'
        return ListValue(elements)
    elif token == ")":
        raise Exception("Unexpected )")
    elif token.startswith('"') and token.endswith('"'):
        # Treat quoted strings as symbols.
        return Symbol(token[1:-1])
    else:
        try:
            number_value: float = float(token)
            return Number(number_value)
        except ValueError:
            return Symbol(token)

def parse_program(source: str) -> List[LispValue]:
    tokens: List[str] = tokenize(source)
    expressions: List[LispValue] = []
    while tokens:
        expressions.append(parse(tokens))
    return expressions
