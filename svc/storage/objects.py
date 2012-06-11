import base64
import datetime
import hashlib
import json

class Error(Exception): pass
class BadData(Error, TypeError): pass

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
        return types[typ].load(sdata)
        


class File(Object): 
    def __init__(self, contents):
        self.contents = contents

    @property
    def id(self):
        return super(File, self).id(self.contents)

    def serialise(self):
        "Serialises the object into format that the store can use"
        content = {"content" : base64.b64encode(self.contents)}
        return super(File, self).serialise(content)

    @classmethod
    def load(self, sdata):
        "Creates a File directly from serialised data."
        data = super(File, self).deserialise(sdata)
        return self(base64.b64decode(data['content']))

class Commit(Object):
    def __init__(self, committer, message, date, parent, files):
        # First validate data
        if not isinstance(committer, str):
            raise BadData("Bad committer '%s'"%committer)
        if not isinstance(message, str):
            raise BadData("Bad commit message '%s'"%message)
        if not isinstance(date, datetime.datetime):
            raise BadData("Bad commit date '%s'"%date)
        if not (parent == None or isinstance(parent, Commit)):
            # None is a sentinel rather than a Boolean here
            raise BadData("Bad commit parent '%s'", parent)
        try:
            if not files:
                raise BadData("Cannot create empty commit")
            for x, y in files:
                if not isinstance(x, str):
                    raise BadData("Bad filename '%s'"%x)
                if not isinstance(y, str):
                    raise BadData("Bad file id '%s'"%y)
        except BadData:
            raise
        except Exception:
            raise BadData("Bad file list")


        self.committer = committer
        self.message = message
        self.date = date
        self.parent = parent
        self.files = files

    def serialise(self):
        "Serialises the object into format that the store can use"
        if self.parent == None:
            parent = ""
        else:
            parent = self.parent.id

        data = {"files"     : self.files,
                "message"   : self.message,
                "date"      : str(self.date),
                "committer" : self.committer,
                "parent"    : parent}

        return super(Commit, self).serialise(data)
    

