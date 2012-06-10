import hashlib

from ..storage import File

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

