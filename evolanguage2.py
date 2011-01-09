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

    #normalvertex = G.newVertexStyle(fontcolor="#809c21", fontfamily="terminus", size="0.5", shape="sphere")
    #normalvertex = G.newVertexStyle(fontcolor="#809c21", shape="sphere")
    #normalvertex = G.newVertexStyle(fontcolor="#809c21", fontfamily="Fixed",color="#405c71", size="0.1")
    normalvertex = G.newVertexStyle(fontcolor="#809c21", fontfamily="Fixed",color="#405c71", size="1.0")
#    normalvertex = G.newVertexStyle(fontcolor="#a0bc41", fontfamily="Fixed",color="#405c71", size="1.0")
#    normalvertex = G.newVertexStyle(fontcolor="#a0bc41", fontfamily="Fixed",color="#777777", size="1.0")

#    normaledge = G.newEdgeStyle(arrow="true",color="#cccccc",arrow_radius="0.3",arrow_position="0.0")
    blueedge = G.newEdgeStyle(color="#0000ff", fontfamily="Fixed")    
    rededge = G.newEdgeStyle(color="#ff0000", fontfamily="Fixed")
    greenedge = G.newEdgeStyle(color="#00ff00", fontfamily="Fixed")
    normaledge = G.newEdgeStyle(fontcolor="#ffffff", fontfamily="Fixed")
    defedge = G.newEdgeStyle(color="#ffff00")
    calledge = G.newEdgeStyle(spline="true", color="#00ffff",stroke="dashed",strength=0.2)







class node(object):
    def __init__(self):
        self.parent = None
        self.id = None
        self.breadchrumbs = []
        self.children = []
        if not hasattr(self,"linkdata"):
            self.linkdata = {}


    def has_breadchrumb(self,breadchrumb):
        return breadchrumb in self.breadchrumbs
    
    def get_breadchrumb(self):
        return random.random()

    def add_breadchrumb(self,breadchrumb):
        self.breadchrumbs.append(breadchrumb)

    def del_breadchrumb(self,breadchrumb):
        self.breadchrumbs.remove(breadchrumb)

        
    def depthfirst_reduce(self,f,d,breadchrumb = None):
        if not breadchrumb:
            breadchrumb = self.get_breadchrumb()
            
        if self.has_breadchrumb(breadchrumb):
            return d
        else:
            self.add_breadchrumb(breadchrumb)
            res = reduce ( lambda d, child: child.depthfirst_reduce(f,d,breadchrumb), self.children, d)
            self.del_breadchrumb(breadchrumb)
            return res

    def addchild(self,child,linkdata = {}):
        self.children.append(child)
        self.linkdata[self.children.index(child)] = linkdata
        child.parent = self

    def setlink(self,child,linkdata):
        self.linkdata[child] = linkdata

    def getlink(self,child):
        try:
            return self.linkdata[self.children.index(child)]
        except:
            return {}
            
    def draw(self,breadchrumb=None):
        if not breadchrumb:
            breadchrumb = self.get_breadchrumb()
            
        if self.has_breadchrumb(breadchrumb):
            return None
        self.add_breadchrumb(breadchrumb)

        if not self.id:
            self.id = G.newVertex(style=normalvertex, label=str(self._repr()))

        x = map(lambda child: {"childvertex" : child.draw(breadchrumb), "edge": (self.getlink(child)["edge"] if self.getlink(child).has_key("edge") else normaledge)}, self.children)
        map(lambda link: G.newEdge(self.id, link["childvertex"], style=link["edge"]) if link["childvertex"] else None,x)

        if hasattr(self,"drawpatch"):
            self.drawpatch()
            
        self.del_breadchrumb(breadchrumb)
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
    
    def __init__(self):
        self.stuff = {}
        self.expression = None

    def gimme_list(self,typ):
        if typ in self.stuff.keys():
            res = list(self.stuff[typ])

        if undefined in self.stuff.keys():
            res = res + list(self.stuff[undefined])
        if res:
            return res
        
        else:
            if self.stuff == {}:
                raise BaseException("my environment is empty.")
            raise BaseException("expression of this type found in my environment :(")

    def gimme(self,typ):
        print "growing",typ

        if typ == type_any:
            res = []
            for t in self.stuff.keys():
                res = res + list(self.stuff[t])
            return random.choice(res)

        
        if typ in self.stuff.keys():
            res = list(self.stuff[typ])

        if undefined in self.stuff.keys():
            res = res + list(self.stuff[undefined])
        if res:
            return random.choice(res)
        
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
    
    def expects(self,child):
        if child in self.children:
            return self.needs[self.children.index(child)]


    def needs_fun(self,breadchrumb = None):
        
        if object.__getattribute__(self, "output") == undefined:
            if self.parent:
                if not breadchrumb:
                    breadchrumb = self.get_breadchrumb()
                    
                if not self.has_breadchrumb(breadchrumb):
                    self.add_breadchrumb(breadchrumb)
                    _needs = map(lambda x: self.parent.expects(self) if x == undefined else x, object.__getattribute__(self, "needs"))
                    self.del_breadchrumb(breadchrumb)
                    return _needs
                else:
                    self.del_breadchrumb(breadchrumb)
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
        print ("eval: " + self._repr())
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


    def showcode(self):
        if not self.children:
            print self._repr(),
        else:
            print "("  + self._repr(),
            map(lambda child: child.showcode(), self.children)
            print  ")",

    def showcode_nice(self,distance=0,First=False):
        if not self.children:
            if not First:
                print  " " * distance,
            print self._repr()
        else:
            if not First:
                print " " * distance,
            print "("  + self._repr(),

            First = True
            for child in self.children:
                child.showcode_nice(distance + 2 + len(self._repr()),First)
                if First:
                    First = False

            print  " " * distance + " )"
                              

        
        

    

        
boolean = t('boolean')
integer = t('integer')
undefined = t('undefined')
context = t('context')
ender = t('ender')
type_any = t('any')



class def_var(e,object):
    output = undefined
    needs = [ ender, undefined ]
    linkdata = {0:{"edge": defedge}}
    
    def __init__(self):
        e.__init__(self)
        
        self.output = undefined
        self.needs = [ type_any, undefined ]


        def drawpatch (s):                
            G.newEdge(s.id, self.id, style=calledge)

        
        self.env.push( type ('get_var',(e,object),{'output': undefined, "needs": [], 'output_fun': lambda s: self.children[1].output , 'drawpatch': drawpatch,  'operation': lambda s: self.evaluate(), '_repr': lambda self: "call" }))


    def operation(self,body,nextexp):
        return nextexp.evaluate()

    def _repr(self):
        return "def"



class def_fun(e,object):
    output = undefined
    needs = [ type_any, undefined ]
    linkdata = {0:{"edge": defedge}}
    
    def __init__(self):
        e.__init__(self)
        
        self.output = undefined
        self.needs = [ type_any, undefined ]


        def drawpatch (s):                
            G.newEdge(s.id, self.id, style=calledge)
        
        self.env.push( type ('call_fun',(e,object),{'output': undefined, "needs": [], 'output_fun': lambda s: self.children[1].output , 'drawpatch': drawpatch,  'operation': lambda s: self.evaluate(), '_repr': lambda self: "call" }))


    def operation(self,body,nextexp):
        return nextexp.evaluate()

    def _repr(self):
        return "def"



conditional_if = type('conditional_if',(e,object),{'output':undefined, '_repr': lambda self: "if", 'needs':[boolean,undefined,undefined], 'linkdata': {0:{"edge":blueedge},1:{"edge":greenedge},2:{"edge":rededge}}, 'operation': (lambda self,test,e1,e2: e1.evaluate() if test.evaluate() else e2.evaluate())})



bool_constant_true = type('boolean_true',(e,object),{'output':boolean, 'operation': lambda self: True, '_repr': lambda self: "T"})
bool_constant_false = type('boolean_false',(e,object),{'output':boolean, 'operation': lambda self: False, '_repr': lambda self: "F"})

bool_larger = type('boolean_larger',(e,object),{'output':boolean, 'needs':[integer,integer], 'operation': lambda self,x,y: True if x.evaluate() > y.evaluate() else False , '_repr': lambda self: ">"})
bool_smaller = type('boolean_smaller',(e,object),{'output':boolean, 'needs':[integer,integer], 'operation': lambda self,x,y: True if x.evaluate() < y.evaluate() else False , '_repr': lambda self: "<"})
bool_equals = type('boolean_equals',(e,object),{'output':boolean, 'needs':[integer,integer], 'operation': lambda self,x,y: True if x.evaluate() == y.evaluate() else False , '_repr': lambda self: "="})

int_constant = type('int_constant',(e,object),{'output':integer,'_init': lambda self: self.__dict__.__setitem__('value',random.randrange(-100,100)), 'operation': lambda self: self.value, '_repr': lambda self: str(self.value)})

bool_not = type('boolean_not',(e,object),{'output':boolean, 'needs':[boolean], 'linkdata' : {0:{"edge":blueedge}}, 'operation': lambda self,x: not x.evaluate() , '_repr': lambda self: "not"})
bool_or = type('boolean_or',(e,object),{'output':boolean, 'needs':[boolean,boolean], 'linkdata' : {0:{"edge":blueedge},1:{"edge":blueedge}}, 'operation': lambda self,x,y: x.evaluate() or y.evaluate() , '_repr': lambda self: "or"})
bool_and = type('boolean_or',(e,object),{'output':boolean, 'needs':[boolean,boolean], 'linkdata' : {0:{"edge":blueedge},1:{"edge":blueedge}},'operation': lambda self,x,y: x.evaluate() and y.evaluate() , '_repr': lambda self: "and"})


int_abs = type('int_abs', (e,object), {'needs' : [integer], 'output' : integer, 'operation' : lambda self,x: abs(x.evaluate()), '_repr': lambda self: 'abs'})
int_plus = type('int_plus', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() + y.evaluate(), '_repr': lambda self: '+'})
int_minus = type('int_minus', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() - y.evaluate(), '_repr': lambda self: '-'})
int_divide = type('int_divide', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() / y.evaluate() if (y.evaluate() != 0) else 0, '_repr': lambda self: ':'})
int_multi = type('int_multi', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() * y.evaluate(), '_repr': lambda self: '*'})


map (lambda o: integer.add(o),[int_abs,int_plus,int_minus,int_divide,int_multi,int_constant,conditional_if])
map (lambda o: boolean.add(o),[bool_constant_true,bool_constant_false,bool_larger,bool_smaller,bool_equals,conditional_if,bool_not,bool_or,bool_and])



rootenv = Env()

undefined.add(boolean)
undefined.add(integer)


map(lambda x: rootenv.push(x),[int_abs,int_plus,int_minus,int_divide,int_multi,int_constant,bool_constant_true,bool_constant_false,bool_larger,bool_smaller,bool_equals,conditional_if,def_fun])

#map(lambda x: rootenv.push(x),[conditional_if,int_plus,int_constant,bool_constant_false,bool_larger,bool_constant_true,bool_and,bool_or,bool_not,def_fun])
#map(lambda x: rootenv.push(x),[int_plus,int_constant,bool_constant_false,bool_larger,bool_constant_true,bool_and,bool_or,bool_not,def_fun])

#map(lambda x: rootenv.push(x),[int_plus,int_constant,bool_constant_false,bool_constant_true,bool_not,def_fun])

a = int_abs()
a.env = rootenv


b = conditional_if()
a.addchild(b)

b.grow()
b.growdepth(6)


if ubi:
    a.draw()


#print (b.needs)
print (b.children)

#print a.evaluate()
