import shutil

from ..storage import FileStorage

def pytest_funcarg__file_store(request):
    store_dir = "/tmp/storage"
    s = FileStorage(store_dir)
    request.addfinalizer(lambda : shutil.rmtree(store_dir))
    return s
    
    
