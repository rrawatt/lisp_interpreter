from lispval import Nil

class Environment:
    def __init__(self, outer=None):
        self.bindings={}
        self.outer=outer

    def get(self, name):
        if name in self.bindings:
            return self.bindings[name]
        elif self.outer:
            return self.outer.get(name)
        else:
            raise Exception("Undefined:", name)
        
    
    def define(self, name, val):
        self.bindings[name]=val
    
    def set(self, name, val):
        if name in self.bindings:
            self.bindings[name]=val
        elif self.outer:
            return self.outer.get(name,val)
        else:
            raise Exception("Undefined:", name)
    
    def extend(self, parameters, args):
        env=Environment(outer=self)
        for i, parameter in enumerate(parameters):
            if i<len(args):
                env.define(parameter, args[i])
            else:
                env.define(parameter, Nil())
        return env
    