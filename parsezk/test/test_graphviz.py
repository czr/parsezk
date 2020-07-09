import inspect
import re
from os.path import abspath, dirname
from textwrap import dedent
from parsezk.test import MockNote
from parsezk.graphviz import (
    Graphviz,
    LinkTable,
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
    lt = LinkTable(collection)
    assert lt.table == [
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
    lt = LinkTable(collection)
    assert lt.table == [
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
    lt = LinkTable(collection)
    assert lt.table == [
        Link('202006210735 Test note', '202007052055 Test note 2', BACKWARD_ONLY),
    ]

def test_document_empty():
    collection = build_notecollection({})
    g = Graphviz(collection)
    assert normalize_whitespace(g.document) == normalize_whitespace(dedent("""\
        digraph G {
        }\
    """))

def test_document_complete_links():
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
    assert normalize_whitespace(g.document) == normalize_whitespace(dedent("""
        digraph G {
            "202006210735 Test note" -> "202007052055 Test note 2"
        }
    """))

def normalize_whitespace(string):
    return re.sub(r'(\n|\s)+', r' ', string).strip()

