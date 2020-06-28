from pathlib import Path
from parsezk.environment import Config

class Note(object):
    """Represents an individual note entry."""
    def __init__(self, id):
        super(Note, self).__init__()
        self.id = id
        
    def filename(self):
        return Config.get('archive_dir') + '/' + self.id + '.md'

    def text(self):
        return Path(self.filename()).read_text(encoding='utf-8')
