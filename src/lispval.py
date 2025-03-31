class LispValue:
    def __init__(self, type_):
        self.type=type
    def to_string(self):
        raise NotImplementedError

class Nil(LispValue):
    def __init__(self, val):
        super.__init__('nil')
        self.val=None

class Symbol(LispValue):
    def __init__(self, val):
        super().__init__('symbol')
        self.val=val

    def to_string(self):
        return self.value

class Num(LispValue):
    def __init__(self, val):
        super().__init__('num')
        self.val=val
    
    def to_string(self):
        s=str(self.val)
        if s.endswith('.0'):
            s=s[:-2]
        return s

class ListVal(LispValue):
    def __init__(self, val):
        super().__init__('list')
        self.val=val if val is not None else []
    def add(self, i):
        self.val.append(i)
    def to_string(self):
        return "(" + " ".join(i.to_string() for i in self.val) + ")"

class Func(LispValue):
    def __init__(self, name, func):
        super().__init__('func')
        self.name=name
        self.func=func
    
    def call(self, args, env):
        return self.func(args, env)

    def to_string(self):
        return "#<function:" + self.name + ">"

class Lambda(LispValue):
    def __init__(self, parameters, body, env):
        super().__init__('lambda')
        self.parameters=parameters
        self.body=body
        self.env=env
    
    def to_string(self):
        return "#<lambda>"