import os

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

    def store_object(self, obj):
        "Stores the serialised object in storage directory."
        address = obj.id
        location = os.path.join(self.location, self.obj_dir, address)
        content = obj.serialise()
        f = open(location, "wb")
        f.write(content)
        f.close()
        
        


        
