"""
Class representing words.
"""

from types import SimpleNamespace


class Word(SimpleNamespace):
    """Represent emtsv columns as object attributes"""

    features = []

    @classmethod
    def header(cls):
        """Return tsv format column headers"""
        return '\t'.join(cls.features)

    def __init__(self, args):
        """Construct word object from list of emtsv feature values"""
        if len(args) != len(self.features):
            raise RuntimeError(f"{len(self.features)} features expected, "
                               + f"{len(args)} provided")

        super().__init__(**dict(zip(self.features, args)))

    def __str__(self):
        """Return tsv format representation of word object."""
        return '\t'.join(self.__dict__.values())

