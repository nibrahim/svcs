import hashlib

class Object(object): 
    def id(self):
        raise NotImplementedError()

class File(Object): 
    def __init__(self, contents):
        self.contents = contents

    @property
    def id(self):
        return hashlib.sha1(self.contents).hexdigest()
        
