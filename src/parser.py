from lispval import ListVal
from lispval import Symbol
from lispval import Num

def tokenize(exp):
    exp=exp.replace("(", " ( ". replace(")", " ) "))
    return exp.split()

def parse(tokens):
    if len(tokens)==0:
        raise Exception("Unexpected EOF while parsing")
    tok=tokens.pop(0)
    if tok=='(':
        out=[]
        while(tokens[0]!=')'):
            out.append(parse(tokens))
        tokens.pop(0)
        return ListVal(out)
    elif tok==')':
        raise Exception("Unexpected '('")
    elif (tok[0]=='"' and tok[-1]=='"') or (tok[0]=="'" and tok[-1]=="'"):
        return Symbol(tok[1:-1])
    else:
        try:
            num=float(tok)
            return Num(num)
        except:
            return Symbol(tok)
