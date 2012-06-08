import os

from ..storage import FileStorage

def test_initialisation():
    "Initialises a storage object"
    s = FileStorage("/tmp/test")
    assert os.path.exists("/tmp/test")
    
    
    
