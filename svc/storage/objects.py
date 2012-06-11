import base64
import hashlib
import json

types = {}

class ObjectFactory(type):
    def __new__(self, name, bases, attrs):
        obj = super(ObjectFactory, self).__new__(self, name, bases, attrs)
        types[name] = obj
        return obj

class Object(object): 
    __metaclass__ = ObjectFactory

    def id(self, content):
        return hashlib.sha1(content).hexdigest()

    def serialise(self, data):
        data['type'] = self.__class__.__name__
        return json.dumps(data)

    @classmethod
    def deserialise(self, data):
        return json.loads(data)

    @classmethod
    def load(self, sdata):
        """
        A factory that instantiates an Object from serialised data.

        The type of the content is used to decide which class to
        instantiate.
        """
        data = self.deserialise(sdata)
        typ = data["type"]
        return types[typ].load(data)
        


class File(Object): 
    def __init__(self, contents):
        self.contents = contents

    @property
    def id(self):
        return super(File, self).id(self.contents)

    def serialise(self):
        content = {"content" : base64.b64encode(self.contents)}
        return super(File, self).serialise(content)

    @classmethod
    def load(self, data):
        "Creates a File directly from deserialised data"
        return self(base64.b64decode(data['content']))
