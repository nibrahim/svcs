import os

class Storage(object):
    def store_object(self, obj):
        raise NotImplementedError()

    def get_object(address):
        raise NotImplementedError()


class FileStorage(Storage):
    def __init__(self, location):
        "Initialises a FileStorage at the given location"
        self.location = location
        if not os.path.isdir(location):
            os.mkdir(location)

        
