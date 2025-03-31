from environment import Environment
from lispval import Symbol
from lispval import Num
from lispval import ListVal

def eval(x, env):
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
            elif operation == 'if':
                if(len(x.vals)) < 3 or len(x.elements)>4:
                    raise Exception("if requires 2 or 3 args")
                condition=eval(x.vals[1], env)
                condition_val=True
                if isinstance(condition, ListVal) and len(condition.vals)==0:
                    condition_val=False
                #TODO