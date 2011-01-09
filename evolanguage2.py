#!/usr/bin/python

import random
#import psyco
#psyco.full()

ubi = True

if ubi:
    import ubigraph

#    G = ubigraph.Ubigraph('http://10.0.0.5:20738/RPC2')
    G = ubigraph.Ubigraph('http://localhost:20738/RPC2')
    G.clear()

    normalvertex = G.newVertexStyle(fontcolor="#809c21", fontfamily="Fixed",color="#405c71", size="1.5")
#    normaledge = G.newEdgeStyle(arrow="true",color="#cccccc",arrow_radius="0.3",arrow_position="0.0")
    normaledge = G.newEdgeStyle(fontcolor="#ffffff", fontfamily="Fixed")

#normalvertex = G.newVertexStyle(fontcolor="#809c21", fontfamily="terminus", size="0.5", shape="sphere")
#normalvertex = G.newVertexStyle(fontcolor="#809c21", shape="sphere")

#normaledge = G.newEdgeStyle(spline="true")



class node(object):
    def __init__(self):
        self.parent = None
        self.id = None
        self.breadchrumb = False
        self.children = []

    def depthfirst_reduce(self,f,d):
        if self.breadchrumb:
            return d
        else:
            self.breadchrumb = True
            res = reduce ( lambda d, child: child.depthfirst_reduce(f,d), self.children, d)
            self.breadchrumb = False
            return res


    def addchild(self,child):
        self.children.append(child)
        child.parent = self

        
    def draw(self):
        if self.breadchrumb:
            return None        
        self.breadchrumb = True
        
        if not self.id:
            self.id = G.newVertex(style=normalvertex, label=str(self._repr()))
        map (lambda vertexid: G.newEdge(self.id,vertexid,style=normaledge  ) if vertexid != None else None ,map(lambda child: child.draw(),self.children))
        
        self.breadchrumb = False
        return self.id
    

class t(node,object):
    def __init__(self,name):
        self.name = name
        node.__init__(self)

    def _repr(self):
        return self.name
    def __repr__(self):
        return "type " + self.name

    def getset(self):
        return self.depthfirst_reduce(lambda d, n: d.union([n]) if (n.__class__ == t) else d,set())

    def add(self,child):
        self.addchild(child)

    def gimme(self):
        return random.choice(self.getset())



class Env(object):
    # environment je takodjer.. svijet u kojem evoluiram kod. kod direktno vezan za grow() funkciju..
    # isti taj kod utjece i na vlastitu evoluciiju (ili da imam jedan korak ovoga? odluku cu ostaviti evoluciji.)
    # njegovi pozivi su nesto tipa "howfar" i neighbor i "parent" i slicno. slicno celularnom automatu
    # rezultati nisu nuzno fiksni nego probabilisticki.

    # dal je taj kod vezan za jedinku? rekel bi da da? ali to je potencijalni fail (ovisi o populaciji?) jer jedinka velikog fitnessa moze imati crippleing error u metaevolucijskom kodu, i cijeli gene pool moze umrjeti u dead endu.

    # dakle metaevolucijski kod i evolucijski kod evoluiraju odvojeno, fitness funkcija metaevolucijskog koda je koliko cesto prouzroci fitness jump evolucijskom kodu. i stvar mora biti arbitrarno chainabilna. neznam ja parametre metaevolucijskog koda. pretpostavio bi da meta-metaevolucijski kod moze pricati i sam o sebi, i o meta-evolucijskom kodu? I GUESS I GUESS.
    
    def __init__(self,):
        self.stuff = {}
        self.expression = None
        
    def gimme(self,typ):
        if typ in self.stuff:
            return random.choice(list(self.stuff[typ]))
        else:
            if self.stuff == {}:
                raise BaseException("my environment is empty.")
            raise BaseException("expression of this type found in my environment :(")
        
    def push (self,expression):
        typ = expression.output
        if not self.stuff.has_key(typ):
            self.stuff[typ] = set()
            
        self.stuff[typ].add(expression)

    def __add__(self,alienenv):
        res = Env()
        res.stuff = self.stuff
        for typ in alienenv.stuff.keys():
            if res.stuff.has_key(typ):
                res.stuff[typ] = res.stuff[typ].union(alienenv.stuff[typ])
            else:
                res.stuff[typ] = alienenv.stuff[typ]
                
        res.expression = self.expression
        return res


class e(node,object):
    def __init__(self):
        self.parent = None
        self.types = []
        self.env = Env()
        node.__init__(self)

#        self.transparent = True
#        self.needs = [boolean,undefined,undefined]
#        self.output = undefined
#        self.operation = lambda x: x

        if hasattr(self,"_init"):
            self._init()
            

    def __setattr__(self,name,value):
#        print ">> setattr",self,name,value
        self.__dict__[name] = value


    def who(self):
        return self.types
    
    def expects(self,child):
        if child in self.children:
            return self.needs[self.children.index(child)]


    def needs_fun(self):
        if object.__getattribute__(self, "output") == undefined:
            if self.parent:
                if not self.breadchrumb:
                    self.breadchrumb = True
                    _needs = map(lambda x: self.parent.expects(self) if x == undefined else x, object.__getattribute__(self, "needs"))
                    self.breadchrumb = False
                    return _needs
                else:
                    self.breadchrumb = False
                    raise AttributeError ("unable to define my need, I'm pulling my leg, wtf.")

        try:
            return object.__getattribute__(self,"needs")
        except:
            return []
        
    
    def output_fun(self):
        if object.__getattribute__(self, "output") == undefined:
            if self.parent:
                return self.parent.expects(self)
            else:
                return undefined

        return  object.__getattribute__(self, "output")
                
    def __getattribute__(self,name):
        if name[:2] != "__" and name + "_fun" in dir(self):
            fun = object.__getattribute__(self,name + "_fun")
            if callable(fun):
                return fun()
        return object.__getattribute__(self, name)


    def evaluate(self,*argv):
        print ("evaluate " + str(self))
        if len(self.children) < len(self.needs):

            raise BaseException("my children are missing.")

        return self.operation(*self.children)

    def env_fun(self):
        env = object.__getattribute__(self,'env')
        if self.parent:
            env = env + self.parent.env
        return env


    def grow(self):
        if not hasattr( self,"needs"):
            return []

        self.children = map (lambda typ: self.env.gimme(typ).__call__(), self.needs)
        map (lambda child: child.__dict__.__setitem__( "parent", self), self.children)       
        return self.children


    def growdepth(self,depth=3):
        if depth > 0:
            self.grow()
            map(lambda child: child.growdepth(depth - 1), self.children)


    def t(self):
        res = [self.output]
        if not self.needs:
            res.append(ender)
        return res

        
boolean = t('boolean')
integer = t('integer')
undefined = t('undefined')
context = t('context')
ender = t('ender')
type_any = t('any')



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
#        env.append( type ('set_int_variable',(e,object),{'output':undefined, 'needs':[undefined,integer], 'operation': lambda s,x,y: self.value = y and x , '_repr': lambda self: "set int var" + str(self)}))

#        env.append( type ('call_int_variable',(e,object),{'output':integer, 'operation': lambda s: self.evaluate(), '_repr': lambda self: "call int var" + str(self) + " " + str(self.value) } ))

        return env


conditional_if = type('conditional_if',(e,object),{'output':undefined, '_repr': lambda self: "if", 'needs':[boolean,undefined,undefined], 'operation': (lambda self,test,e1,e2: e1.evaluate() if test.evaluate() else e2.evaluate())})




class def_fun(e,object):
    output = undefined
    needs = [ type_any, undefined ]

    def __init__(self):
        self.output = undefined
        self.needs = [ type_any, undefined ]
#        self.env = Env()
        self.env.push( type ('call_fun',(e,object),{'output': undefined,'output_fun': lambda s: self.children[1].output , 'operation': lambda s: self.evaluate(), '_repr': lambda self: "call int var" + str(self) + " " + str(self.value)}))

    def operation(self):
        self.children[0].evaluate()

    def _repr(self):
        return "var " + str(self) + " " + str(self.value)


bool_constant_true = type('boolean_true',(e,object),{'output':boolean, 'operation': lambda self: True, '_repr': lambda self: "t"})
bool_constant_false = type('boolean_false',(e,object),{'output':boolean, 'operation': lambda self: False, '_repr': lambda self: "f"})

bool_larger = type('boolean_larger',(e,object),{'output':boolean, 'needs':[integer,integer], 'operation': lambda self,x,y: True if x > y else False , '_repr': lambda self: ">"})
bool_smaller = type('boolean_smaller',(e,object),{'output':boolean, 'needs':[integer,integer], 'operation': lambda self,x,y: True if x < y else False , '_repr': lambda self: "<"})
bool_equals = type('boolean_equals',(e,object),{'output':boolean, 'needs':[integer,integer], 'operation': lambda self,x,y: True if x == y else False , '_repr': lambda self: "="})

int_constant = type('int_constant',(e,object),{'output':integer,'_init': lambda self: self.__dict__.__setitem__('value',random.randrange(-100,100)), 'operation': lambda self: self.value, '_repr': lambda self: str(self.value)})

    


int_abs = type('int_abs', (e,object), {'needs' : [integer], 'output' : integer, 'operation' : lambda self,x: abs(x.evaluate()), '_repr': lambda self: 'abs'})
int_plus = type('int_plus', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() + y.evaluate(), '_repr': lambda self: '+'})
int_minus = type('int_minus', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() - y.evaluate(), '_repr': lambda self: '-'})
int_divide = type('int_divide', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() / y.evaluate() if (y.evaluate() != 0) else 0, '_repr': lambda self: ':'})
int_multi = type('int_multi', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() * y.evaluate(), '_repr': lambda self: '*'})


map (lambda o: integer.add(o),[int_abs,int_plus,int_minus,int_divide,int_multi,int_constant,conditional_if])
map (lambda o: boolean.add(o),[bool_constant_true,bool_constant_false,bool_larger,bool_smaller,bool_equals,conditional_if])



rootenv = Env()

undefined.add(boolean)
undefined.add(integer)


#map(lambda x: rootenv.push(x),[int_abs,int_plus,int_minus,int_divide,int_multi,int_constant,bool_constant_true,bool_constant_false,bool_larger,bool_smaller,bool_equals,conditional_if,def_fun])

map(lambda x: rootenv.push(x),[int_minus,int_constant,bool_constant_false,bool_larger,conditional_if,def_fun])

a = int_abs()
a.env = rootenv


b = conditional_if()
a.children.append(b)
b.parent = a

b.grow()
b.growdepth(6)


if ubi:
    a.draw()


#print (b.needs)
print (b.children)

#print a.evaluate()
