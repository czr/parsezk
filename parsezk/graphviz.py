from pprint import pformat


COMPLETE = 'complete'
FORWARD_ONLY = 'forward-only'
BACKWARD_ONLY = 'backward-only'

class Printable():
    """Mixin providing a generic __repr__ method"""
    def __repr__(self):
        return (
            '<' + type(self).__name__ + '> ' +
            pformat(vars(self), indent=2)
        )

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
        table = []

        # Complete and forward links
        for source_id, source_note in self.collection.items():
            for dest_id in source_note.links('Next'):
                dest_note = self.collection[dest_id]
                if source_id in dest_note.links('Prev'):
                    table.append(Link(source_id, dest_id, COMPLETE))
                else:
                    table.append(Link(source_id, dest_id, FORWARD_ONLY))

        # Backward links
        for source_id, source_note in self.collection.items():
            for dest_id in source_note.links('Prev'):
                dest_note = self.collection[dest_id]
                if source_id in dest_note.links('Next'):
                    # Nothing to do. We picked up complete links above.
                    pass
                else:
                    table.append(Link(dest_id, source_id, BACKWARD_ONLY))

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
        for link in self.linktable.table:
            source_id = link.source
            dest_id = link.destination
            lines.append('"' + source_id + '" -> "' + dest_id + '"')
        lines.append("}")
        return "\n".join(lines)
