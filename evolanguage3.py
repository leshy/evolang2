#!/usr/bin/python2
import random
#import psyco
#psyco.full()
import types
import copy
import time


ubi = True
def logx(data):
    print "LOGX " + str(data)

if ubi:
    import ubigraph
    #G = ubigraph.Ubigraph('http://10.0.0.5:20738/RPC2')
    G = ubigraph.Ubigraph('http://localhost:20738/RPC2')
    G.clear()

    #normalvertex = G.newVertexStyle(fontcolor="#809c21", fontfamily="terminus", size="0.5", shape="sphere")
    #normalvertex = G.newVertexStyle(fontcolor="#809c21", shape="sphere")
    #normalvertex = G.newVertexStyle(fontcolor="#809c21", fontfamily="Fixed",color="#405c71", size="0.1")
    normalvertex = G.newVertexStyle(fontcolor="#809c21", fontfamily="Fixed",color="#405c71", size="1.0")
    #normalvertex = G.newVertexStyle(fontcolor="#809c21", fontfamily="Fixed",color="#405c71", size="1.0",shape="sphere")
    #normalvertex = G.newVertexStyle(fontcolor="#a0bc41", fontfamily="Fixed",color="#405c71", size="1.0")
    #normalvertex = G.newVertexStyle(fontcolor="#a0bc41", fontfamily="Fixed",color="#777777", size="1.0")
    #normaledge = G.newEdgeStyle(arrow="true",color="#cccccc",arrow_radius="0.3",arrow_position="0.0")
    
    blueedge = G.newEdgeStyle(color="#0000ff", fontfamily="Fixed")    
    rededge = G.newEdgeStyle(color="#ff0000", fontfamily="Fixed")
    greenedge = G.newEdgeStyle(color="#00ff00", fontfamily="Fixed")
    normaledge = G.newEdgeStyle(fontcolor="#ffffff", fontfamily="Fixed")
    defedge = G.newEdgeStyle(color="#ffff00",stroke="dashed")
    calledge = G.newEdgeStyle(spline="true", color="#00ffff",stroke="dashed",strength=0.2)
    argedge = G.newEdgeStyle(spline="true", color="#ff00ff",stroke="dashed",strength=0.01)



class node(object):
    def __init__(self):
        self.parent = None
        self.id = None
        self.breadchrumbs = []
        self.children = []

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

    def addchild(self,child):
        self.children.append(child)
        child.parent = self
            
    def draw(self,labels=True,breadchrumb=None):
        if not breadchrumb:
            breadchrumb = self.get_breadchrumb()
            
        if self.has_breadchrumb(breadchrumb):
            return None
        self.add_breadchrumb(breadchrumb)

        if not self.id:
            if labels:
                self.id = G.newVertex(style=normalvertex, label=str(self._repr()))
            else:
                self.id = G.newVertex(style=normalvertex)

        x = map(lambda child: {"childvertex" : child.draw(labels,breadchrumb), "edge": self.getedge(child)}, self.children)
        map(lambda link: G.newEdge(self.id, link["childvertex"], style=link["edge"]) if link["childvertex"] else None,x)

        if hasattr(self,"drawhook"):
            self.drawhook()
            
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
        #print "growing",typ

        if typ == type_any:
            res = []
            for t in self.stuff.keys():
                res = res + list(self.stuff[t])
            return random.choice(res)

        
        if typ in self.stuff.keys():
            res = list(self.stuff[typ])

        if transparent in self.stuff.keys():
            res = res + list(self.stuff[transparent])
        if res:
            return random.choice(res)
        
        else:
            if self.stuff == {}:
                raise BaseException("my environment is empty.")
            raise BaseException("expression of this type found in my environment :(")
        
    def push (self,expression):
        if not expression: return False
        typ = expression.output
        if not self.stuff.has_key(typ):
            self.stuff[typ] = set()
            
        self.stuff[typ].add(expression)

    def __add__(self,alienenv):            

        res = Env()
        res.stuff = copy.copy(self.stuff)

        for typ in alienenv.stuff.keys():
            if res.stuff.has_key(typ):
                res.stuff[typ] = res.stuff[typ].union(alienenv.stuff[typ])
            else:
                res.stuff[typ] = alienenv.stuff[typ]
                
        return res


class e(node,object):
    def __init__(self):
        self.parent = None
        self.types = []
        self.env = Env()
        node.__init__(self)
        if "_init" in dir(self):
            self._init()
        self.buildlinks_fromneeds()

#        self.children  = { "child1" : { "needs": integer, "env": "bla", pointer: None } }

#        self.transparent = True
#        self.needs = [boolean,undefined,undefined]
#        self.output = undefined
#        self.operation = lambda x: x

        if hasattr(self,"_init"):
            self._init()

    def getedge(self,child):
        link = self.link(child)
        if not link: return normaledge
        
        if link.has_key("edge"): return link["edge"]
        if link["type"] == boolean: return blueedge
        return normaledge

    def __setattr__(self,name,value):
#        print ">> setattr",self,name,value
        self.__dict__[name] = value

    def children_fun(self):
        return filter(lambda x: x, map(lambda childname: self.child(childname) , self.links))

    def link(self,child):
        if type(child) == types.StringType:
            return self.links[child]
        
        for childname in self.links:
            #print self,"checking " + childname
            if not self.links[childname].has_key("pointer"): continue
            if self.links[childname]["pointer"] == child:
                return self.links[childname]
        return None

    def childname(self,child):
        for childname in self.children:
            if not hasattr(self.children[childname],"pointer"): continue
            if self.children[childname]["pointer"] == child:
                return childname
        return None

    def child(self,name):

        if self.links[name].has_key("pointer"):
            return self.links[name]["pointer"]
        else:
            return None
        
    def linked(self,child):
        if self.link(child)["pointer"]:
            return True
        else:
            return False
    
    def expects(self,child):
        link = self.link(child)
        if link["type"] == transparent and hasattr(self,"parent") and self.parent:
            return self.parent.expects(self)    
        return link["type"]
        
    def needs_fun(self):
        return map(lambda x: self.expects(x), self.links)

    def open_needs_fun(self):
        return filter( lambda x: x, map(lambda x: False if self.child(x) else self.expects(x), self.links))


    def output_fun(self):
        if object.__getattribute__(self, "output") == transparent:
            if self.parent:
                return self.parent.expects(self)
            else:
                return transparent

        return  object.__getattribute__(self, "output")
                
    def __getattribute__(self,name):
        if name[:2] != "__" and name + "_fun" in dir(self):
            fun = object.__getattribute__(self,name + "_fun")
            if callable(fun):
                return fun()
        return object.__getattribute__(self, name)


    def evaluate(self,*argv):
        #print ("eval: " + self._repr())
        if len(self.children) < len(self.needs):
            raise BaseException("my children are missing.")

        return self.operation(*self.children)

    def getenv(self,child):
        link = self.link(child)
        if link and link.has_key("env"): return self.env + link["env"]()
        return self.env

    def env_fun(self):
        #env = Env()
        try:
            env = object.__getattribute__(self,"env")
            if self.parent:
                env = env + self.parent.getenv(self)
        except:
            if self.parent:
                env = self.parent.getenv(self)

        return env

    def gotparent(self,parent):
        self.parent = parent

    def grow(self):
        if not hasattr( self,"needs"):
            return []

#        print self,"children",self.children, "needs",self.open_needs
        self.addchild ( map (lambda typ: self.env.gimme(typ).__call__(), self.open_needs))
        map (lambda child: child.gotparent(self),self.children)
        return self.children
    
    
    def freesocket(self):
        for childname in self.links:
            if not self.links[childname].has_key("pointer"):
                return childname
            if not self.links[childname]["pointer"]:
                return childname
        return None
            
    def addchild(self,child,name=None):
        if type(child) == types.ListType:
            return map(lambda c: self.addchild(c), child)
        
        if not name: name = self.freesocket()
        if not name: raise BaseException(self, "no free child sockets")   
            
        self.links[name]["pointer"] = child
        child.parent = self


    def growdepth(self,depth=3):
        if depth > 0:
            self.grow()
            return reduce (lambda y, x : x + y, map(lambda child: child.growdepth(depth - 1), self.children), 1)
        return 0

    def growdraw(self,depth):
        r = self.growdepth(depth)
        self.draw()
        return r
    
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
transparent = t('transparent')
ender = t('ender')
type_any = t('any')



class def_var(e,object):
    output = undefined
    needs = [ ender, undefined ]
    
    def __init__(self):
        e.__init__(self)
        
        self.output = undefined
        self.needs = [ type_any, undefined ]


        def drawhook (s):                
            G.newEdge(s.id, self.id, style=calledge)
        
        self.env.push( type ('get_var',(e,object),{'output': undefined, "needs": [], 'output_fun': lambda s: self.children[1].output , 'drawhook': drawhook,  'operation': lambda s: self.evaluate(), '_repr': lambda self: "call" }))


    def operation(self,body,nextexp):
        return nextexp.evaluate()

    def _repr(self):
        return "def"


def e2(node):
    def __init__(self):
        pass
    
    
        
        
        
                      




# - problem sa nepoznatim tipom funkcijskog poziva:
#   mogao bi inzistirati na tome da prvo raste function body, sto ce nakon prvog node-a definirati tip funkcije, i call ce postati availiable u environmentu, tj biti dodan u environment u tom trenutku, sto znaci da bi trebao nekako hookati addchild od def_fun-a?

# - problem sa argumentima u environmentu:
#mogao bi dozvoliti definiranje razlicitih environmenta za razlicitu djecu, u toj varijanti djete pita parenta za svoj environment


# ** rjeseno, call je availiable u env-u tek kad funkcija ima djecu, env moze biti specificiran kao per child funkcija.


# - buildlinks_fromneeds se executa na pocetku, a needovi function call-a su dinamicki. rastu sa dodatnim argumentima.

# - def unutar def-a funkcije moze dobiti arg od prve funkcije kao svoje tijelo. u tom slucaju tip argumenta postaje type_any, zdrk, ali nece raditi greske, function call tipa any nigdje nece biti upotrjebljen.

class def_fun(e,object):
    output = transparent
    def __init__(self):
        e.__init__(self)
        self.links = {"function body": dict(type=type_any, env=self.bodyenv, edge=defedge), "continue": dict(type=transparent,env=self.continueenv)}
        self.args = []

    def selftype(self):
        child = self.child("function body")
        if child:
            return child.output
        return undefined

    def get_call(self):
        if not hasattr(self,"call"):
            def open_needs_fun(s):
                #print "HOOK"
                s.buildlinks_fromneeds()
                return e.open_needs_fun(s)

            def callneeds(s):
                return map(lambda a: a.output, self.args)

            
            self.call = type ('call_fun',(e,object),{'output': self.selftype(), "needs_fun": lambda s: callneeds(s), 'open_needs_fun': lambda s: open_needs_fun(s),  'drawhook': lambda s: G.newEdge(s.id, self.id, style=calledge),  'operation': lambda s: self.evaluate(), '_repr': lambda self: "call" })
            
        return self.call
            
    


        
    # call funkcije zna sto mu treba iz callneeds poziva, on gleda spawnane argumente.
    # nekako se tip koji je argument dobio pocetnim assignanjem mora propagirati do njegove klase.
    # u jebemti.


    def get_args(self):
        if self.args:
            return self.args
        return []
    
    def get_newarg(self):

        def gotparent(s,parent):
            if s.__class__ not in self.args:
                s.__class__.output = parent.expects(s)
                self.args.append(s.__class__)
        
        return type ('arg-' + str(len(self.args)),(e,object),{'output': transparent,
                                       "needs": [],
                                       'argnum': len(self.args),
                                       'gotparent': lambda s,parent: gotparent(s,parent),
                                       'operation': lambda s: None,
                                       'drawhook': lambda s: G.newEdge(s.id,self.id,style=argedge),
                                       '_repr': lambda s: "arg " + str(s.argnum)})
    
    def bodyenv(self):
#        print "bodyenv called"
        if self.selftype() == undefined:
            return None

        env = Env()
        env.push(self.get_call())
        env.push(self.get_newarg())
        map (lambda a: env.push(a),self.get_args())
        map (lambda x: env.push(x), self.args)


        #print env.stuff

        if env.stuff:
            return env
        return None
        

    def continueenv(self):
#        print "continueenv called"
        if self.selftype() == undefined:
            return None

        env = Env()
        env.push(self.get_call())

        #print env.stuff
        
        if env.stuff:
            return env

        
        return None
    



        
    def operation(self,body,nextexp):
        return nextexp.evaluate()

    def _repr(self):
        return "def"




conditional_if = type('conditional_if',(e,object),{'output':transparent,
                                                   '_repr': (lambda self: "if"),
                                                   '_init': (lambda self: setattr(self,"links",{ "condition": dict(type=boolean),
                                                                                    "true":dict(type=transparent,edge=greenedge),
                                                                                    "false":dict(type=transparent,edge=rededge)
                                                                                    })),
                                                   'operation': (lambda self,test,e1,e2: e1.evaluate() if test.evaluate() else e2.evaluate())})



bool_constant_true = type('boolean_true',(e,object),{'output':boolean, 'operation': lambda self: True, '_repr': lambda self: "T"})
bool_constant_false = type('boolean_false',(e,object),{'output':boolean, 'operation': lambda self: False, '_repr': lambda self: "F"})

bool_larger = type('boolean_larger',(e,object),{'output':boolean, 'needs':[integer,integer], 'operation': lambda self,x,y: True if x.evaluate() > y.evaluate() else False , '_repr': lambda self: ">"})
bool_smaller = type('boolean_smaller',(e,object),{'output':boolean, 'needs':[integer,integer], 'operation': lambda self,x,y: True if x.evaluate() < y.evaluate() else False , '_repr': lambda self: "<"})
bool_equals = type('boolean_equals',(e,object),{'output':boolean, 'needs':[integer,integer], 'operation': lambda self,x,y: True if x.evaluate() == y.evaluate() else False , '_repr': lambda self: "="})

int_constant = type('int_constant',(e,object),{'output':integer,'_init': lambda self: self.__dict__.__setitem__('value',random.randrange(-100,100)), 'operation': lambda self: self.value, '_repr': lambda self: str(self.value)})

bool_not = type('boolean_not',(e,object),{'output':boolean, 'needs':[boolean], 'operation': lambda self,x: not x.evaluate() , '_repr': lambda self: "not"})
bool_or = type('boolean_or',(e,object),{'output':boolean, 'needs':[boolean,boolean], 'operation': lambda self,x,y: x.evaluate() or y.evaluate() , '_repr': lambda self: "or"})
bool_and = type('boolean_or',(e,object),{'output':boolean, 'needs':[boolean,boolean], 'operation': lambda self,x,y: x.evaluate() and y.evaluate() , '_repr': lambda self: "and"})


int_abs = type('int_abs', (e,object), {'needs' : [integer], 'output' : integer, 'operation' : lambda self,x: abs(x.evaluate()), '_repr': lambda self: 'abs'})
int_plus = type('int_plus', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() + y.evaluate(), '_repr': lambda self: '+'})
int_minus = type('int_minus', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() - y.evaluate(), '_repr': lambda self: '-'})
int_divide = type('int_divide', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() / y.evaluate() if (y.evaluate() != 0) else 0, '_repr': lambda self: ':'})
int_multi = type('int_multi', (e,object), {'needs' : [integer,integer], 'output' : integer, 'operation' : lambda self,x,y: x.evaluate() * y.evaluate(), '_repr': lambda self: '*'})





rootenv = Env()


map(lambda x: rootenv.push(x),[int_abs,int_plus,int_minus,int_divide,int_multi,int_constant,bool_constant_true,bool_constant_false,bool_not,bool_or,bool_and,bool_larger,bool_smaller,bool_equals,conditional_if,def_fun])

#map(lambda x: rootenv.push(x),[conditional_if,int_plus,int_constant,bool_constant_false,bool_larger,bool_constant_true,bool_and,bool_or,bool_not,def_fun])
#map(lambda x: rootenv.push(x),[int_plus,int_constant,bool_constant_false,bool_larger,bool_constant_true,bool_and,bool_or,bool_not,def_fun])

#map(lambda x: rootenv.push(x),[int_plus,int_constant,bool_constant_false,bool_constant_true,bool_not,def_fun])



a = int_abs()
a.env = rootenv
b = conditional_if()
a.addchild(b)
c = def_fun()
b.addchild(c)

#b.grow()


#c.growdepth(4)
#b.grow()
#b.growdepth(6)

#c = conditional_if()
if ubi:
    a.growdraw(5)
    #a.draw()


#print (a.children)
#print (b.needs)
#print (b.children)

#print a.evaluate()



#import cProfile

#def foo():
#    print "grown " + str(a.growdepth(15)) + " nodes."
#cProfile.run('foo()')
