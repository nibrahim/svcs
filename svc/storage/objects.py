class Object(object): pass

class File(Object): 
    def __init__(self, contents):
        self.contents = contents
