
#nema potrebe za odvojenim linkdata objektom i children listom, children moze biti dict sa informacijama o djeci.
#linkdata definira sto objekt ocekuje od djeteta, boju linka u iscrtavanju, environment djeteta, i tak.

class node(object):
    def __init__(self):
        self.id = None
        self.breadchrumbs = []
        self.children = []
        
    def addchild(self,child):
        self.children.append(child)
        
    def getchildren(self):
        return self.children

    def haschild(self,child):
        return child in self.children

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

    def draw(self,breadchrumb=None):
        if not breadchrumb:
            breadchrumb = self.get_breadchrumb()
            
        if self.has_breadchrumb(breadchrumb):
            return None
        self.add_breadchrumb(breadchrumb)

        if not self.id:
            self.id = G.newVertex(style=normalvertex, label=str(self._repr()))

        x = map(lambda child: {"childvertex" : child.draw(breadchrumb), "edge": (self.getlink(child)["edge"] if self.getlink(child).has_key("edge") else normaledge)}, self.getchildren())
        map(lambda link: G.newEdge(self.id, link["childvertex"], style=link["edge"]) if link["childvertex"] else None,x)

        if hasattr(self,"drawpatch"):
            self.drawpatch()
            
        self.del_breadchrumb(breadchrumb)
        return self.id
        
        


class nodeexpression(node):
    def __init__(self):
        node.__init__(self)
        self.parent = None
        self.children = {}
        if not hasattr(self,"linkdata"):
            self.linkdata = {}

    def addchild(self,child,link=None):
        if not link:
            for checklink in self.linkdata:
                if (not self.linkdata[link].has_key("child") or not self.linkdata[link]["child"]):
                    link = checklink
                    break
        if not link:
            raise BaseException("addchild called and all links are taken")

        self.linkdata[link]["child"] = child
        child.parent = self
        return child
    
    def getlink(self,child):
        for link in self.linkdata:
            if (self.linkdata[link].has_key("child") and self.linkdata[link]['child'] == child):
                return link
        return False

    def haschild(self,child):
        return self.getlink(child)
            

    def getchildren(self):
        children = []
        for link in self.linkdata:
            if (self.linkdata[link].has_key("child") and self.linkdata[link]['child']):
                children.append (self.linkdata[link]['child'])
        return children
                              
        
    def draw(self,breadchrumb=None):
        if not breadchrumb:
            breadchrumb = self.get_breadchrumb()
            
        if self.has_breadchrumb(breadchrumb):
            return None
        self.add_breadchrumb(breadchrumb)

        if not self.id:
            self.id = G.newVertex(style=normalvertex, label=str(self._repr()))

        x = map(lambda child: {"childvertex" : child.draw(breadchrumb), "edge": (self.getlink(child)["edge"] if self.getlink(child).has_key("edge") else normaledge)}, self.getchildren())
        map(lambda link: G.newEdge(self.id, link["childvertex"], style=link["edge"]) if link["childvertex"] else None,x)

        if hasattr(self,"drawpatch"):
            self.drawpatch()
            
        self.del_breadchrumb(breadchrumb)
        return self.id
        
