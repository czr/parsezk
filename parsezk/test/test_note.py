import inspect
import os
import re
from parsezk.environment import Config
from parsezk.note import Note


def setup():
    test_file = inspect.getfile(inspect.currentframe())
    test_dir = os.path.dirname(os.path.abspath(test_file))
    Config.set('archive_dir', test_dir + '/test_note')

def test_id():
    id = '202006210735 Test note'
    note = Note(id)
    assert note.id == id

def test_filename():
    id = '202006210735 Test note'
    note = Note(id)
    assert re.match(
        '.+/test_note/202006210735 Test note.md',
        note.filename(),
    )

def test_text():
    pass
