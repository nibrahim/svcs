import os

class FileStorage(object):
    def __init__(self, location):
        "Initialises a FileStorage at the given location"
        self.location = location
        os.mkdir(location)

        
        
