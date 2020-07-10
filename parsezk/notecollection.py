import re
from collections.abc import Mapping
from pathlib import Path
from parsezk.environment import Config
from parsezk.note import Note


class NoteCollection(Mapping):
    """An archive of notes"""
    def __init__(self):
        self.notes = {}
        archive_path = Path(Config.get('archive_dir'))
        for child in archive_path.iterdir():
            if child.is_file() and re.match(r'.*\.md$', child.name):
                note = Note(str(child))
                self.notes[note.id] = note
        super().__init__()

    def __getitem__(self, key):
        return self.notes[key]

    def __iter__(self):
        return iter(self.notes)

    def __len__(self):
        return len(self.notes)
