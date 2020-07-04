import re
from pathlib import Path

class Note(object):
    """Represents an individual note entry."""
    def __init__(self, filename):
        super(Note, self).__init__()
        self.filename = filename

    @property
    def id(self):
        result = re.search('([^/]+)\\.md$', self.filename)
        if result:
            return result.group(1)

    @property
    def text(self):
        return Path(self.filename).read_text(encoding='utf-8')

    def links(self, key):
        return re.findall(
            r'\b' + key + r' : \s* \[\[ ( [^\]]+ ) \]\]',
            self.text,
            re.X,
        )

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
