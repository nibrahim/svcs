import os

from .objects import Object

class Storage(object):
    def store_object(self, obj):
        raise NotImplementedError()

    def get_object(self, address):
        raise NotImplementedError()


class FileStorage(Storage):
    def __init__(self, location):
        "Initialises a FileStorage at the given location"
        self.location = location
        self.obj_dir = "objects"
        if not os.path.isdir(location):
            os.mkdir(location)
            os.mkdir(os.path.join(self.location, self.obj_dir))

    def store_object(self, obj):
        "Stores the serialised object in storage directory."
        address = obj.id
        location = os.path.join(self.location, self.obj_dir, address)
        content = obj.serialise()
        f = open(location, "wb")
        f.write(content)
        f.close()
    
    def get_object(self, address):
        "Retrieves the object with the given address."
        location = os.path.join(self.location, self.obj_dir, address)
        with open(location) as f:
            contents = f.read()
        f = Object.load(contents)
        return f
        


        
