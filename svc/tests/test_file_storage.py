import glob
import os
import shutil

import py

from ..storage import FileStorage, File

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

def test_create_file():
    """Creates a file object and tests whether it is storing the
    contents."""
    f = File("This is a test string")

    assert f.contents == "This is a test string"

    
    
    
    
    
    
    

    


    
    
    
