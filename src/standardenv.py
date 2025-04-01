from lispval import *
from evaluator import evalExpr
from environment import Environment
import operator
from math import prod

def asNum(x):
    if isinstance(x, Num):
        return x.val
    else:
        raise Exception("Expected a Num")

def displayFunc(args):
    for arg in args:
        print(arg.to_string(), end='')
    return ListVal()

def standardEnvironment():
    env = Environment()
    env.define("+", Func("+", lambda args, env: Num(sum(asNum(arg) for arg in args))))
    env.define("-", Func("-", lambda args, env: Num(-asNum(args[0])) if len(args)==1 
                              else Num(operator.sub(asNum(args[0]), sum(asNum(arg) for arg in args[1:])))))
    env.define("*", Func("*", lambda args, env:Num(prod(asNum(arg) for arg in args))))
    env.define("/", Func("/", lambda args, env:Num(1/asNum(args[0])) if len(args)==0 
                              else Num(operator.truediv(asNum(args[0]), prod(asNum(arg) for arg in args)))))

    env.define("=", Func("=", lambda args, env: Num(1) if all(asNum(args[0]) == asNum(arg) for arg in args[1:]) else Num(0)))
    #env.define(">", Func(">", lambda args, env: )) TODO