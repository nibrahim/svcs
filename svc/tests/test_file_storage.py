import os
import shutil

from ..storage import FileStorage

def test_initialisation():
    "Initialises a storage object"
    s = FileStorage("/tmp/test")
    assert os.path.exists("/tmp/test")
    shutil.rmtree("/tmp/test")


def test_init_existing():
    "Loads an existing storage object"
    s0 = FileStorage("/tmp/test")
    assert os.path.exists("/tmp/test")
    s1 = FileStorage("/tmp/test")
    shutil.rmtree("/tmp/test")
    



    
    
    
