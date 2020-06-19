import re
from functools import reduce


class Segment:
    """
    Represents a Segment in a Chapter
    """

    def __init__(self, number: int, lines: list, characters=None):
        """
        :param number: ordinal number in the chapter
        :param lines: segment lines
        """
        if characters is None:
            characters = []
        self.characters = characters
        self.number = number
        self.lines = lines

    def count_words(self) -> int:
        """
        Counts all words in the Segment.

        :return: Number of Words in the Chapter
        """
        return len(self.words())

    def content(self) -> str:
        """
        Returns the text of this Segment as a single string.

        :return: complete Segment content.
        """
        return reduce(lambda l1, l2: l1 + l2, self.lines) if len(self.lines) > 0 else ''

    def words(self) -> list:
        """
        Returns all words in the Segment, without any special characters (no punctuation or quotation characters).

        :return: all words in the Segment as a list of words
        """
        pattern = re.compile(r'(?!-)(?:-\b|\b-|\'\b|\b\'|\w)+(?=\b)')
        text = self.content().replace('’', '\'')
        return re.findall(pattern, text)

    def __repr__(self):
        return 'No: {}, Lines: {}, Words: {}'.format(self.number, len(self.lines), self.count_words())


def segment_to_dict(segment: Segment) -> dict:
    """
    Saves a Segment object as a dict for serialisation via JSON.

    :param segment: Segment object
    :return: Serialized Segment object as dict
    """
    return {
        'no': segment.number,
        'lines': segment.lines,
        'characters': segment.characters
    }


def segment_from_dict(obj) -> Segment:
    """
    Loads a serialized JSON dict as a Segment object.

    :param obj: JSON dict
    :return: Deserialized Segment object
    """
    if 'no' in obj and 'lines' in obj and 'characters' in obj:
        return Segment(obj['no'], obj['lines'], obj['characters'])
    return obj
