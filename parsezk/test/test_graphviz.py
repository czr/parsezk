import inspect
from os.path import abspath, dirname
from textwrap import dedent
from parsezk.test import MockNote
from parsezk.graphviz import (
    Graphviz,
    Link,
    COMPLETE,
    FORWARD_ONLY,
    BACKWARD_ONLY
)


test_file = inspect.getfile(inspect.currentframe())
test_dir = dirname(abspath(test_file))
archive_dir = test_dir + '/test_graphviz'

def build_notecollection(mapping):
    collection = {}
    for id, text in mapping.items():
        filename = archive_dir + '/' + id + '.md'
        note = MockNote(filename, text)
        collection[id] = note

    return collection


def test_link_complete():
    collection = build_notecollection({
        '202006210735 Test note': dedent("""\
            # Test note

            This is a test.

            Next: [[202007052055 Test note 2]]
            """
        ),
        '202007052055 Test note 2': dedent("""\
            # Test note 2

            This is a test.

            Prev: [[202006210735 Test note]]
            """
        ),
    })
    g = Graphviz(collection)
    assert g.link_table() == [
        Link('202006210735 Test note', '202007052055 Test note 2', COMPLETE),
    ]

def test_link_forward_only():
    collection = build_notecollection({
        '202006210735 Test note': dedent("""\
            # Test note

            This is a test.

            Next: [[202007052055 Test note 2]]
            """
        ),
        '202007052055 Test note 2': dedent("""\
            # Test note 2

            This is a test.
            """
        ),
    })
    g = Graphviz(collection)
    assert g.link_table() == [
        Link('202006210735 Test note', '202007052055 Test note 2', FORWARD_ONLY),
    ]

def test_link_backward_only():
    collection = build_notecollection({
        '202006210735 Test note': dedent("""\
            # Test note

            This is a test.
            """
        ),
        '202007052055 Test note 2': dedent("""\
            # Test note 2

            This is a test.

            Prev: [[202006210735 Test note]]
            """
        ),
    })
    g = Graphviz(collection)
    assert g.link_table() == [
        Link('202006210735 Test note', '202007052055 Test note 2', BACKWARD_ONLY),
    ]

