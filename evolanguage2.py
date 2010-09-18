#!/usr/bin/python

import random
#import psyco
#psyco.full()

class t(set,object):
    def __init__(self,name,*attr):
        set.__init__(self)
        self.name = name
        
    def gimme(self):
        if self:
            return random.choice(list(self))
        else:
            print self.name,": I'm empty, I can't give you anything"
            return undefined

    def showset(self):
        return set.__repr__(self)
    
    def __repr__(self):
        return self.name + " type"


boolean = t('boolean')
integer = t('integer')
undefined = t('undefined')
type_ender = t('ender')
context = t('context')
ender = t('ender')
type_any = t('any')


class e(object):    
    def __init__(self):
        self._search = False
        self.parent = None
        self.children = []

#        self.transparent = True
#        self.needs = [boolean,undefined,undefined]
#        self.output = undefined
#        self.operation = lambda x: x

        if hasattr(self,"_init"):
            self._init()
    
#    def __repr__(self):
#        if self.has_attr("_repr"):
#            return str(self._repr()) + " " +  str(self) 
#        else:
#            return str(self)
         

    def __setattr__(self,name,value):
#        print ">> setattr",self,name,value
        self.__dict__[name] = value

    def expects(self,child):
        if child in self.children:
            return self.needs[self.children.index(child)]


    def needs_fun(self):
        if object.__getattribute__(self, "output") == undefined:
            if self.parent:
                if not self._search:
                    self._search = True
                    _needs = map(lambda x: self.parent.expects(self) if x == undefined else x,object.__getattribute__(self, "needs"))
                    self._search = False
#                    print "RETURNING ",_needs
                    return _needs
                else:
                    self._search = False                    
                    raise AttributeError ("unable to define my need, I'm pulling my leg, wtf.")

        return object.__getattribute__(self,"needs")
    
    def output_fun(self):
        if object.__getattribute__(self, "output") == undefined:
            if self.parent:
                return self.parent.expects(self)
                
    def __getattribute__(self,name):
#        print "getattr",self,name

#        if name[:2] != "__":
#            print ">> getattr",self,name
        
        if name[:2] != "__" and name + "_fun" in dir(self):
#            print "WIN " + name
            fun = object.__getattribute__(self,name + "_fun")
            if callable(fun):
#                print "CALL", fun, fun()
                return fun()
        return object.__getattribute__(self, name)


    def evaluate(self,*argv):
        print "evaluate " + str(self)
        return self.operation(*self.children)

    def env(self):
        return []

    def grow(self):
        if not self.needs:
            return []
        self.children = map (lambda typ: typ.gimme().__call__() , self.needs)
        map (lambda child: child.__dict__.__setitem__( "parent", self), self.children)
        return self.children




conditional_if = type('conditional_if',(e,object),{'output':undefined, 'needs':[boolean,undefined,undefined], 'operation': (lambda test,e1,e2: e1.evaluate() if test.evaluate() else e2.evaluate())})

bool_constant_true = type('boolean_true',(e,object),{'output':boolean, 'operation': lambda self: True, '_repr': lambda self: True})

bool_constant_false = type('boolean_false',(e,object),{'output':boolean, 'operation': lambda self: False, '_repr': lambda self: False})


bool_larger = type('boolean_larger',(e,object),{'output':boolean, 'needs':[integer,integer], 'operation': lambda self,x,y: True if x > y else False , '_repr': lambda self: ">"})
bool_smaller = type('boolean_smaller',(e,object),{'output':boolean, 'needs':[integer,integer], 'operation': lambda self,x,y: True if x < y else False , '_repr': lambda self: "<"})

bool_equals = type('boolean_equals',(e,object),{'output':boolean, 'needs':[integer,integer], 'operation': lambda self,x,y: True if x == y else False , '_repr': lambda self: "="})




int_constant = type('int_constant',(e,object),{'output':integer,'_init': lambda self: self.__dict__.__setitem__('value',random.randrange(-100,100)), 'operation': lambda self: self.value, '_repr': lambda self: str(self.value)})


class def_int_variable(e,object):
    def __init__(self):
        self.output = undefined
        self.needs = [ender,undefined]
        
    def operation(self):
        return self.value

    def _repr(self):
        return "var " + str(self) + " " + str(self.value)
    
    def env(self):
        env = []
#        env.append( type ('set_int_variable',(e,object),{'output':undefined, 'needs':[undefined,integer], 'operation': lambda s,x,y: self.value = y and x , '_repr': lambda self: "set int var" + str(self) + " " + str(self.value) } ))
#        env.append( type ('call_int_variable',(e,object),{'output':integer, 'operation': lambda s: self.evaluate(), '_repr': lambda self: "call int var" + str(self) + " " + str(self.value) } ))

        return env

class def_fun(e,object):
    def __init__(self):
        self.output = undefined
        self.needs = [ type_any, undefined]
        
    def operation(self):
        return self.value

    def _repr(self):
        return "var " + str(self) + " " + str(self.value)
    
    def env(self):
        env = []
        env.append( type ('call_fun',(e,object),{'output':integer, 'operation': lambda s: self.evaluate(), '_repr': lambda self: "call int var" + str(self) + " " + str(self.value)}))
        
        return env

    



function_def = type('function_def',(e,object),{'output':undefined,'_init': lambda self: self.__dict__.__setitem__('value',random.randrange(-100,100)), 'operation': lambda self: self.value, '_repr': lambda self: str(self.value)})


int_abs = type('int_abs', (e,object), {'needs' : [integer], 'output' : integer, 'operation' : lambda self,x: abs(x.evaluate()), '_repr': lambda self: 'abs'})
int_plus = type('int_plus', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() + y.evaluate(), '_repr': lambda self: '+'})
int_minus = type('int_minus', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() - y.evaluate(), '_repr': lambda self: '-'})
int_divide = type('int_divide', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() / y.evaluate() if (y.evaluate() != 0) else 0, '_repr': lambda self: ':'})
int_multi = type('int_multi', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() * y.evaluate(), '_repr': lambda self: '*'})


root = type('root', (e,object),{'needs': [type_any], 'output' : undefined, 'operation' : lambda self,x: x.evaluate(),'_repr': lambda self: "root"})

map (lambda o: integer.add(o),[int_abs,int_plus,int_minus,int_divide,int_multi,int_constant,conditional_if])
map (lambda o: boolean.add(o),[bool_constant_true,bool_constant_false,bool_larger,bool_smaller,bool_equals,conditional_if])

type_any.update(boolean)
type_any.update(integer)


typesorter = {}
typesorter[lambda (x): True if not x.needs else False] = type_ender

# win
map (lambda o: o.output.add(o) and map(lambda check: typesorter[check].add(o) if check(o) else False, typesorter), type_any)


a = int_abs()
b = conditional_if()


a.children = [b]
b.parent = a

print b.needs

b.grow()

print b.children

