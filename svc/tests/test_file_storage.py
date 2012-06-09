import glob
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

def test_create_file(file_store):
    # Prepare the file
    f = open("/tmp/input_file", "wb")
    f.write("\nThis is a test\n")
    f.close()
    
    # Ask the Storage object to save the file.
    file_store.create_file(f)
    
    # Manually check if it has been saved This part pokes into the
    # store directly using undocumented variables.
    file_storage_dir = file_store.location + "/files/"
    repo_file = glob.glob(file_storage_dir + "/*")[0]
    file_contents = open(repo_file).read()
    assert file_contents == "\nThis is a test\n"

    
    
    
    
    
    
    

    


    
    
    
