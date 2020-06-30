import inspect
from os.path import abspath, dirname
from parsezk.environment import Config
from parsezk.notecollection import NoteCollection


def setup():
    test_file = inspect.getfile(inspect.currentframe())
    test_dir = dirname(abspath(test_file))
    Config.set('archive_dir', test_dir + '/test_notecollection')

def test_keys():
    collection = NoteCollection()
    assert list(collection.keys()) == [
        '202006210735 Test note',
        '202006281843 Test note 2',
    ]

def test_get():
    collection = NoteCollection()
    assert collection['202006210735 Test note'].id == '202006210735 Test note'
