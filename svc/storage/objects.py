import base64
import hashlib
import json

class Object(object): 
    def id(self):
        raise NotImplementedError()

    def serialise(self):
        raise NotImplementedError()

class File(Object): 
    def __init__(self, contents):
        self.contents = contents

    @property
    def id(self):
        return hashlib.sha1(self.contents).hexdigest()

    def serialise(self):
        content = {"type"    : "file",
                   "content" : base64.b64encode(self.contents)}
        return json.dumps(content)

        
