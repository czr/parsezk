import re
from pathlib import Path
from unicodedata import normalize

def normalize_id(id):
    return normalize('NFC', id)

class Note(object):
    """Represents an individual note entry."""
    def __init__(self, filename):
        super(Note, self).__init__()
        self.filename = filename

    @property
    def id(self):
        result = re.search('([^/]+)\\.md$', self.filename)
        if result:
            return normalize_id(result.group(1))

    @property
    def text(self):
        return Path(self.filename).read_text(encoding='utf-8')

    def links(self, key):
        links = re.findall(
            r'\b' + key + r' : \s* \[\[ ( [^\]]+ ) \]\]',
            self.text,
            re.X,
        )
        return [normalize_id(l) for l in links]

    @property
    def title(self):
        m = re.match(
            r'\A \# \s+ (.*)',
            self.text,
            re.X,
        )
        if m:
            return m.group(1)
        else:
            return None

    @property
    def mentions(self):
        mentions = re.findall(
            r'\[\[ ( [^\]]+ ) \]\]',
            self.text,
            re.X,
        )
        return [normalize_id(m) for m in mentions]
