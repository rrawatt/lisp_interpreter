from __future__ import annotations
from .standardenv import standard_env
from .parser import parse_program
from .evaluator import eval_lisp

def repl() -> None:
    env = standard_env()
    print("Lisp Interpreter (type 'exit' to quit)")
    while True:
        try:
            user_input: str = input("lisp>> ")
            if user_input.strip() == "exit":
                break
            expressions = parse_program(user_input)
            for expr in expressions:
                result = eval_lisp(expr, env)
                if result is not None:
                    print(">>", result.to_string())
        except Exception as err:
            print("Error:", err)