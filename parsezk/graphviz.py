from pprint import pformat
from collections import namedtuple


COMPLETE = 'complete'
FORWARD_ONLY = 'forward-only'
BACKWARD_ONLY = 'backward-only'
MENTION = 'mention'

class Printable():
    """Mixin providing a generic __repr__ method"""
    def __repr__(self):
        return (
            '<' + type(self).__name__ + '> ' +
            pformat(vars(self), indent=2)
        )

Route = namedtuple("Route", ["source_id", "destination_id"])

class Link(Printable):
    """Represents a link between notes"""
    def __init__(self, source, destination, status):
        super(Link, self).__init__()
        self.source = source
        self.destination = destination
        self.status = status

    def __eq__(self, other):
        if not isinstance(other, Link):
            return NotImplemented

        return (
            self.source == other.source
            and self.destination == other.destination
            and self.status == other.status
        )

class LinkTable():
    """Represents the links in a NoteCollection"""
    def __init__(self, collection):
        super().__init__()
        self.collection = collection

    @property
    def table(self):
        seen = {}
        table = []

        # Complete and forward links
        for source_id, source_note in self.collection.items():
            for dest_id in source_note.links('Next'):
                seen[Route(source_id=source_id, destination_id=dest_id)] = True
                dest_note = self.collection[dest_id]
                if source_id in dest_note.links('Prev'):
                    table.append(Link(source_id, dest_id, COMPLETE))
                else:
                    table.append(Link(source_id, dest_id, FORWARD_ONLY))

        # Backward links
        for source_id, source_note in self.collection.items():
            for dest_id in source_note.links('Prev'):
                seen[Route(source_id=source_id, destination_id=dest_id)] = True
                dest_note = self.collection[dest_id]
                if source_id in dest_note.links('Next'):
                    # Nothing to do. We picked up complete links above.
                    pass
                else:
                    table.append(Link(dest_id, source_id, BACKWARD_ONLY))

        # Mentions
        for source_id, source_note in self.collection.items():
            for dest_id in source_note.mentions:
                route = Route(source_id=source_id, destination_id=dest_id)
                if not seen.get(route, False):
                    table.append(Link(source_id, dest_id, MENTION))

        return table


class Graphviz():
    """Builds a Graphviz document"""
    def __init__(self, collection):
        super().__init__()
        self.collection = collection
        self.linktable = LinkTable(self.collection)

    @property
    def document(self):
        lines = []
        lines.append("digraph G {")
        lines.append("rankdir=LR")

        for note_id, note in self.collection.items():
            lines.append('"' + note_id + '"')

        for link in self.linktable.table:
            source_id = link.source
            dest_id = link.destination
            if (link.status == FORWARD_ONLY or link.status == BACKWARD_ONLY):
                lines.append('"' + source_id + '" -> "' + dest_id + '" [color="red"]')
            elif (link.status == MENTION):
                lines.append('"' + source_id + '" -> "' + dest_id + '" [color="grey"]')
            else:
                lines.append('"' + source_id + '" -> "' + dest_id + '"')

        lines.append("}")
        return "\n".join(lines)
