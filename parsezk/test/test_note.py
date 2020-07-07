import inspect
import re
from os.path import abspath, dirname
from textwrap import dedent
from parsezk.environment import Config
from parsezk.note import Note
from parsezk.test import MockNote


test_file = inspect.getfile(inspect.currentframe())
test_dir = dirname(abspath(test_file))
archive_dir = test_dir + '/test_note'

def test_filename():
    filename = archive_dir + '/202006210735 Test note.md'
    note = Note(filename)
    assert re.match(
        '.+/test_note/202006210735 Test note.md',
        note.filename,
    )

def test_id():
    filename = archive_dir + '/202006210735 Test note.md'
    note = Note(filename)
    assert note.id == '202006210735 Test note'

def test_text():
    filename = archive_dir + '/202006210735 Test note.md'
    note = Note(filename)
    expected = dedent("""\
        # Test note

        This is a test.
        """
    )
    assert note.text == expected

def test_link_single():
    text = dedent("""\
        # Test note

        This is a test.

        Next: [[202007010705 Test note 2]]
        """
    )
    filename = archive_dir + '/202006210735 Test note.md'
    note = MockNote(filename, text)

    assert note.links('Next') == ['202007010705 Test note 2']

def test_link_multiple():
    text = dedent("""\
        # Test note

        This is a test.

        Next: [[202007010705 Test note 2]]
        Next: [[202007010705 Test note 3]]
        """
    )
    filename = archive_dir + '/202006210735 Test note.md'
    note = MockNote(filename, text)

    assert note.links('Next') == ['202007010705 Test note 2', '202007010705 Test note 3']

def test_title():
    text = dedent("""\
        # Test note title

        This is a test.
        """
    )
    filename = archive_dir + '/202006210735 Test note.md'
    note = MockNote(filename, text)

    assert note.title == 'Test note title'

def test_title_missing():
    text = dedent("""\
        This is a test.
        """
    )
    filename = archive_dir + '/202006210735 Test note.md'
    note = MockNote(filename, text)

    assert note.title == None

def test_title_multiple():
    text = dedent("""\
        # Test note title

        This is a test.

        # Test note title 2

        This is still a test.
        """
    )
    filename = archive_dir + '/202006210735 Test note.md'
    note = MockNote(filename, text)

    assert note.title == 'Test note title'
