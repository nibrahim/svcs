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

def test_store_file(file_store):
    "Stores a file object in a FileStorage"
    f = File("This is a test string")
    file_store.store_object(f)
    
    # Manually inspect the storage area. This pokes into it using
    # undocumented APIs.
    expected_obj = file_store.location + "/objects/" + f.id
    assert os.path.exists(expected_obj), "File was not stored in expected location"
    
    
def test_get_file(file_store):
    "Store a file in the store and retrieve it. Then verify it."
    f = File("This is a test string")
    file_store.store_object(f)
    
    retrieved_file = file_store.get_object(f.id)
    assert retrieved_file.contents == "This is a test string"
    

    
