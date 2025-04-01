from environment import Environment
from lispval import *

def evalExpr(x, env):
    if isinstance(x, Symbol):
        return env.get(x.vals)
    elif isinstance(x, Num):
        return x
    elif isinstance(x, ListVal):
        if len(x)==0:
            return x
        first = x.vals[0]
        if isinstance(first, Symbol):
            operation=first.vals
            if operation in ("quote", "'", '"'):
                if len(x.vals)!=2:
                    raise Exception("quote requires exactly one argument")
                else:
                    return x.vals[1]
            elif operation=='if':
                if(len(x.vals)) < 3 or len(x.elements)>4:
                    raise Exception("if requires 2 or 3 args")
                condition=evalExpr(x.vals[1], env)
                condition_val=True
                if isinstance(condition, ListVal) and len(condition.vals)==0:
                    condition_val=False
                elif isinstance(condition, Num) and condition.val==0:
                    condition_val=False

                if condition_val:
                    return evalExpr(x.vals[2], env)
                elif len(x.vals)>3:
                    return evalExpr(x.elements[3], env)
                else:
                    return ListVal()
            elif operation=='define':
                if (x.vals)!=3:
                    raise Exception("Define requires exactly 2 args")
                if isinstance(x.element[1], Symbol):
                    value=evalExpr(x.vals[2], env)
                    env.define(x.vals[1].val, value)
                    return value
            elif isinstance(x.elements[1], ListVal):
                funcLis=x.vals[1]
                if len(funcLis.vals)==0 or not isinstance(funcLis.vals[0], Symbol):
                    raise Exception("Incorrect Function Declaration")
                funcName=funcLis.vals[0].val
                parameters=[]
                for parameter in funcLis.vals[:-1]:
                    if not isinstance(parameter, Symbol):
                        raise Exception("Function parameters must be symbols")
                    parameters.append(parameter.val)
                lam=Lambda(parameters, x.vals[2], env)
                env.define(funcName, lam)
                return lam
            elif operation=='set!':
                if len(x.vals)!=3:
                    raise Exception("set! requries exactly 2 args")
                if not isinstance(x.vals[1], Symbol):
                    raise Exception("First arg of set! must be a symbol")
                value=evalExpr(x.vals[2], env)
                env.set(x.vals[1].val, value)
                return value
            elif operation=='lambda':
                if len(x.vals) != 3:
                    raise Exception("lambda requires exactly 2 arguments")
                if not isinstance(x.vals[1], ListVal):
                    raise Exception("First argument to lambda must be a list")
                parameters=[]
                for parameter in x.vals[1].vals:
                    if not isinstance(parameter, Symbol):
                        raise Exception("Lambda parameters must be symbols")
                    parameters.append(parameter.val)
                return Lambda(parameters, x.vals[2], env)
            elif operation=='begin':
                result = None 
                for expr in x.vals[1:]:
                    result=evalExpr(expr, env)
                return result
        proc=evalExpr(x.vals, env)
        args=[evalExpr(x.vals(arg,env)) for arg in x.vals[1:]]
        if isinstance(proc, Func):
            return proc.call(args, env)
        elif isinstance(proc, Lambda):
            newEnv=proc.env.extend(proc.parameters, args)
            return evalExpr(proc.body, newEnv)
        else:
            raise Exception("First element of list must be a function")
    else:
        raise Exception("Unknown Expression Type")
                
                
