import base64
import calendar
import datetime
import hashlib
import json

import py

from ..storage import File, Commit, BadData

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
    files = [("file1.txt", File("Contents of file 1").id),
             ("file2.txt", File("Contents of file 2").id),
             ("file3.txt", File("Contents of file 3").id)]
    message = "Commit message"
    date = datetime.datetime.utcnow()
    committer = "noufal@nibrahim.net.in"
    parent_commit = None
    c = Commit(committer, message, date, parent_commit, files)

    assert c.date == date
    assert c.committer == committer
    assert c.parent == parent_commit
    assert c.files == files
    
def test_validate_commit():
    """
    Tries to instantiate a commit with bad data and makes sure that it
    doesn't allow it.
    """
    files = [("file1.txt", File("Contents of file 1").id),
             ("file2.txt", File("Contents of file 2").id),
             ("file3.txt", File("Contents of file 3").id)]

    t = datetime.datetime.utcnow()

    py.test.raises(BadData, 
                   Commit, False, "message", t, None, files)
    
    py.test.raises(BadData,
                   Commit, "noufal@nibrahim.net.in", 1, t, None, files)

    py.test.raises(BadData, 
                   Commit, "noufal@nibrahim.net.in", "message", "1/June/2012", None, files)

    py.test.raises(BadData, 
                   Commit, "noufal@nibrahim.net.in", "message", t, "", files)

    py.test.raises(BadData, # Empty commit
                   Commit, "noufal@nibrahim.net.in", "message", t, None, [])

    py.test.raises(BadData, # Bad commit data
                   Commit, "noufal@nibrahim.net.in", "message", t, None, [(1,2)])

    py.test.raises(BadData, # Bad commit data
                   Commit, "noufal@nibrahim.net.in", "message", t, None, [("foo.txt",2)])

    py.test.raises(BadData, # Bad commit data
                   Commit, "noufal@nibrahim.net.in", "message", t, None, [File("das")])



def test_serialise_commit():
    """Verifies whether the Commit object is properly serialised"""

    files = [("file1.txt", File("Contents of file 1").id),
             ("file2.txt", File("Contents of file 2").id),
             ("file3.txt", File("Contents of file 3").id)]
    message = "Commit message"
    date = datetime.datetime.utcnow()
    committer = "noufal@nibrahim.net.in"
    parent_commit = None
    c = Commit(committer, message, date, parent_commit, files)
    
    d = {"type" : "Commit",
         "files" : c.files,
         "message" : message,
         "date" : calendar.timegm(date.timetuple()),
         "committer" : committer,
         "parent" : ""}
    
    expected_serialised_data = json.dumps(d)
    actual_serialised_data = c.serialise()
    
    assert expected_serialised_data == actual_serialised_data
    
def test_load_commit(): 
    "Makes sure that serialisation and deserialisation is idempotent"
    files = [("file1.txt", File("Contents of file 1").id),
             ("file2.txt", File("Contents of file 2").id),
             ("file3.txt", File("Contents of file 3").id)]
    message = "Commit message"
    date = datetime.datetime.utcnow().replace(microsecond = 0)
    committer = "noufal@nibrahim.net.in"
    parent_commit = None
    c0 = Commit(committer, message, date, parent_commit, files)

    s = c0.serialise()
    c1 = Commit.load(s)

    assert c0.message == c1.message
    assert c0.date == c1.date
    assert c0.committer == c1.committer
    assert c0.parent == c1.parent
    assert c0.files == c1.files
    
    
