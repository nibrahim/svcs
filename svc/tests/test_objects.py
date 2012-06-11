import base64
import datetime
import hashlib

from ..storage import File, Commit

def test_create_file():
    """Creates a file object and tests whether it is storing the
    contents."""
    f = File("This is a test string")

    assert f.contents == "This is a test string"

def test_address_file():
    """Verifies the File object computes its id properly"""
    f = File("This is a test string")

    expected_hash = hashlib.sha1("This is a test string").hexdigest()
    assert f.id == expected_hash

def test_serialise_file():
    """Verifies the a File object can serialise itself. 

    Assumes knowledge about the serialisation format."""

    f = File("This is a test string")
    
    expected_content = base64.b64encode("This is a test string")
    f.serialise() == expected_content


def test_load_file():
    """
    Verifies whether a File can be loaded back from it's serialised
    format.
    """
    
    f0 = File("This is a test string")

    s = f0.serialise()
    f1 = File.load(s)
    assert f0.contents == f1.contents
    
def test_create_commit():
    """
    Tries to create a commit and checks whether the contents are
    stored properly.
    """
    # List of files to commit.
    files = [("file1.txt", File("Contents of file 1")),
             ("file2.txt", File("Contents of file 2")),
             ("file3.txt", File("Contents of file 3"))]
    message = "Commit message"
    date = datetime.datetime.now()
    committer = "noufal@nibrahim.net.in"
    parent_commit = None
    c = Commit(committer, message, date, parent_commit, *files)

    assert c.date == date
    assert c.committer == committer
    assert c.parent == parent_commit

    expected_files = [(x, y.id) for x,y in files]
    assert c.files == expected_files
    



    
