from __future__ import annotations
import math
import operator
from typing import List
from .lispval import LispValue, ListValue, Number, Function, Symbol
from .environment import Environment

def as_number(value: LispValue) -> float:
    if isinstance(value, Number):
        return value.value
    else:
        raise Exception("Expected a number")

def display_function(arguments: List[LispValue]) -> LispValue:
    for arg in arguments:
        print(arg.to_string(), end='')
    return ListValue()

def standard_env() -> Environment:
    env = Environment()
    # Arithmetic operations.
    env.define("+", Function("+", lambda args, env: Number(sum(as_number(arg) for arg in args))))
    env.define("-", Function("-", lambda args, env: Number(-as_number(args[0])) if len(args) == 1
                                  else Number(operator.sub(as_number(args[0]), sum(as_number(arg) for arg in args[1:])))))
    env.define("*", Function("*", lambda args, env: Number(math.prod(as_number(arg) for arg in args))))
    env.define("/", Function("/", lambda args, env: Number(1 / as_number(args[0])) if len(args) == 1
                                  else Number(operator.truediv(as_number(args[0]), math.prod(as_number(arg) for arg in args[1:])))))
    # Comparison operations.
    env.define("=", Function("=", lambda args, env: Number(1) if all(as_number(args[0]) == as_number(arg) for arg in args[1:])
                                  else ListValue()))
    env.define("<", Function("<", lambda args, env: Number(1) if as_number(args[0]) < as_number(args[1])
                                  else ListValue()))
    env.define(">", Function(">", lambda args, env: Number(1) if as_number(args[0]) > as_number(args[1])
                                  else ListValue()))
    # List operations.
    env.define("cons", Function("cons", lambda args, env: ListValue([args[0]] +
                                  (args[1].elements if isinstance(args[1], ListValue) else [args[1]]))))
    env.define("car", Function("car", lambda args, env: args[0].elements[0]
                                  if (isinstance(args[0], ListValue) and args[0].elements) else Exception("car called on empty list")))
    env.define("cdr", Function("cdr", lambda args, env: ListValue(args[0].elements[1:])
                                  if (isinstance(args[0], ListValue) and args[0].elements) else Exception("cdr called on empty list")))
    env.define("list", Function("list", lambda args, env: ListValue(args)))
    env.define("length", Function("length", lambda args, env: Number(len(args[0].elements))
                                  if isinstance(args[0], ListValue) else Exception("length requires a list argument")))
    # Logic operations.
    env.define("not", Function("not", lambda args, env: Number(1)
                                  if (isinstance(args[0], ListValue) and not args[0].elements) or (isinstance(args[0], Number) and args[0].value == 0)
                                  else ListValue()))
    # Type predicates.
    env.define("number?", Function("number?", lambda args, env: Number(1)
                                  if isinstance(args[0], Number) else ListValue()))
    env.define("symbol?", Function("symbol?", lambda args, env: Number(1)
                                  if isinstance(args[0], Symbol) else ListValue()))
    env.define("list?", Function("list?", lambda args, env: Number(1)
                                  if isinstance(args[0], ListValue) else ListValue()))
    env.define("null?", Function("null?", lambda args, env: Number(1)
                                  if isinstance(args[0], ListValue) and not args[0].elements else ListValue()))
    # Display functions.
    env.define("display", Function("display", lambda args, env: display_function(args)))
    env.define("newline", Function("newline", lambda args, env: (print(), ListValue())[1]))
    return env
