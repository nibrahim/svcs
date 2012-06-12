import datetime
import os
import shutil

import py

from ..storage import FileStorage, File, Commit

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
    

def test_store_commit(file_store):
    "Stores a commit in a FileStorage"
    f1, f2, f3 = File("Contents of file 1"), File("Contents of file 2"), File("Contents of file 3")
    files = [["file1.txt", f1.id],
             ["file2.txt", f2.id],
             ["file3.txt", f3.id]]
    message = "Commit message"
    date = datetime.datetime.utcnow().replace(microsecond = 0)
    committer = "noufal@nibrahim.net.in"
    parent_commit = None
    c = Commit(committer, message, date, parent_commit, files)
    
    file_store.store_object(c)

    expected_obj = file_store.location + "/objects/" + c.id
    assert os.path.exists(expected_obj), "Commit was not stored in expected location"
    
def test_store_tip(file_store):
    "Tries to store a commit as the tip. Verifies storage and contents."
    f1, f2, f3 = File("Contents of file 1"), File("Contents of file 2"), File("Contents of file 3")
    files = [["file1.txt", f1.id],
             ["file2.txt", f2.id],
             ["file3.txt", f3.id]]
    message = "Commit message"
    date = datetime.datetime.utcnow().replace(microsecond = 0)
    committer = "noufal@nibrahim.net.in"
    parent_commit = None
    c = Commit(committer, message, date, parent_commit, files)

    file_store.update_tip(c)
    expected_obj = os.path.join(file_store.location, "TIP")
    assert os.path.exists(expected_obj), "Tip not stored"
    assert open(expected_obj).read() == c.id
    
    



