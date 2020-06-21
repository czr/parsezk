from parsezk.note import Note

def test_id():
    id = '202006210735 Test note'
    note = Note(id)
    assert note.id == id
