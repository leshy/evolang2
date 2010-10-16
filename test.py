
class test(object):
    def __init__(self):
        self.bla = 33
    
    def __getattribute__(self,name):
        print "getattr " + name
        if name == "xx":
            return "HAHAHAHA"
        return object.__getattribute__(self, name)


a = test()

print a.bla
print a.xx
