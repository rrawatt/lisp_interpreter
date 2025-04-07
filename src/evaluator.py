from __future__ import annotations
from typing import List
from .lispval import LispValue, Symbol, Number, ListValue, Function, Lambda
from .environment import Environment

def eval_lisp(expression: LispValue, env: Environment) -> LispValue:
    if isinstance(expression, Symbol):
        return env.get(expression.name)
    elif isinstance(expression, Number):
        return expression
    elif isinstance(expression, ListValue):
        if not expression.elements:
            return expression  # Empty list.
        first_expr: LispValue = expression.elements[0]
        if isinstance(first_expr, Symbol):
            operator_name: str = first_expr.name
            if operator_name in ("quote", "'"):
                if len(expression.elements) != 2:
                    raise Exception("quote requires exactly one argument")
                return expression.elements[1]
            elif operator_name == "if":
                if not (3 <= len(expression.elements) <= 4):
                    raise Exception("if requires 2 or 3 arguments")
                condition_result = eval_lisp(expression.elements[1], env)
                is_true: bool = True
                if isinstance(condition_result, ListValue) and not condition_result.elements:
                    is_true = False
                elif isinstance(condition_result, Number) and condition_result.value == 0:
                    is_true = False
                if is_true:
                    return eval_lisp(expression.elements[2], env)
                elif len(expression.elements) > 3:
                    return eval_lisp(expression.elements[3], env)
                else:
                    return ListValue()
            elif operator_name == "define":
                if len(expression.elements) != 3:
                    raise Exception("define requires exactly 2 arguments")
                second_expr = expression.elements[1]
                if isinstance(second_expr, Symbol):
                    value = eval_lisp(expression.elements[2], env)
                    env.define(second_expr.name, value)
                    return value
                elif isinstance(second_expr, ListValue):
                    func_list = second_expr.elements
                    if not func_list or not isinstance(func_list[0], Symbol):
                        raise Exception("Invalid function definition")
                    func_name: str = func_list[0].name
                    parameters: List[str] = []
                    for param in func_list[1:]:
                        if not isinstance(param, Symbol):
                            raise Exception("Function parameters must be symbols")
                        parameters.append(param.name)
                    lambda_value = Lambda(parameters, expression.elements[2], env)
                    env.define(func_name, lambda_value)
                    return lambda_value
                else:
                    raise Exception("First argument to define must be a symbol or a list")
            elif operator_name == "set!":
                if len(expression.elements) != 3:
                    raise Exception("set! requires exactly 2 arguments")
                if not isinstance(expression.elements[1], Symbol):
                    raise Exception("First argument to set! must be a symbol")
                value = eval_lisp(expression.elements[2], env)
                env.set(expression.elements[1].name, value)
                return value
            elif operator_name == "lambda":
                if len(expression.elements) != 3:
                    raise Exception("lambda requires exactly 2 arguments")
                if not isinstance(expression.elements[1], ListValue):
                    raise Exception("First argument to lambda must be a list")
                parameters: List[str] = []
                for param in expression.elements[1].elements:
                    if not isinstance(param, Symbol):
                        raise Exception("Lambda parameters must be symbols")
                    parameters.append(param.name)
                return Lambda(parameters, expression.elements[2], env)
            elif operator_name == "begin":
                result: LispValue = ListValue()
                for expr in expression.elements[1:]:
                    result = eval_lisp(expr, env)
                return result

        procedure = eval_lisp(expression.elements[0], env)
        args: List[LispValue] = [eval_lisp(arg, env) for arg in expression.elements[1:]]
        if isinstance(procedure, Function):
            return procedure.call(args, env)
        elif isinstance(procedure, Lambda):
            new_env = procedure.env.extend(procedure.parameters, args)
            return eval_lisp(procedure.body, new_env)
        else:
            raise Exception("First element of list must be a function")
    else:
        raise Exception("Unknown expression type")
