#!/usr/bin/python
# directional graph

import ubigraph

G = ubigraph.Ubigraph()
G.clear()


normalvertex = G.newVertexStyle(fontcolor="#809c21", fontfamily="terminus",color="#405c71", size="0.5")


normaledge = G.newEdgeStyle(arrow="true",color="#cccccc",arrow_radius="0.3",arrow_position="0.0")

normaledge = G.newEdgeStyle(spline="true")

#normaledge = G.newEdgeStyle()


class hooklist(list,object):
    def __init__(self,*argv):

        self.hook_add = []
        self.hook_remove = []
        
        list.__init__(self,*argv)

    def __setitem__(self,index,item,*argv):
        map (lambda fun: fun(self[index]), self.hook_remove)
        list.__setitem__(self,index,item,*argv)
        map (lambda fun: fun(self[index]), self.hook_add)

    def __delitem__(self,index,*argv):
        list.__delitem__(self,index,*argv)
        map (lambda fun: fun(self[index]), self.hook_remove)
        
    def append(self,item,*argv):
        list.append(self,item,*argv)
        map (lambda fun: fun(item), self.hook_add)


class node(object):
    def __init__(self):
        self.parent = None
        self.id = None
        self.drawing = False
        self.children = hooklist()

        self.children.hook_add.append(lambda child: child.__dict__.__setitem__("parent",self))
        self.children.hook_remove.append(lambda child: child.__dict__.__setitem__("parent",None))

    def draw(self):
        if self.drawing:
            return None
        
        self.drawing = True
            
        if not self.id:
            self.id = G.newVertex(style=normalvertex, label=str(self._repr()))

        map (lambda vertexid: G.newEdge(self.id,vertexid,style=normaledge  ) if vertexid != None else None ,map(lambda child: child.draw(),self.children))
            
        self.drawing = False
            
        return self.id
        



def test():
    a = node()
    b = node()
    c = node()


    a.children.append(b)
    a.children.append(c)
    
    a.draw()

    
