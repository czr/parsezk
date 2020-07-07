from parsezk.note import Note

class MockNote(Note):
    def __init__(self, filename, text):
        super().__init__(filename)
        self._text = text

    @property
    def text(self):
        return self._text
