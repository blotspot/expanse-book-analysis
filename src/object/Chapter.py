from functools import reduce

from src.object.ChapterType import ChapterType
from src.object.Character import Character
from src.object.Segment import Segment


class Chapter:
    """
    Represents a Chapter in a Book
    """

    def __init__(self, number: int, pov: Character, segments: list, c_type: ChapterType):
        """
        :param pov: name of the POV Character
        :param segments: chapter lines
        :param c_type: type of the chapter (prologue, interlude, chapter, epilogue)
        """
        self.number = number
        self.pov = pov
        self.segments = segments
        self.chapter_type = c_type

    def title(self) -> str:
        """
        Creates a formatted string that represents the chapter title.

        :return: formatted chapter title
        """
        if self.chapter_type == ChapterType.CHAPTER:
            return '{} {}: {}'.format(self.chapter_type.name, self.number, self.pov)

        return '{}: {}'.format(self.chapter_type.name, self.pov)

    def segment_nr(self, i: int) -> Segment:
        """
        Return the requested Segment starting at 0.

        :return: Segment
        """
        return self.segments[i]

    def count_words(self) -> int:
        """
        Counts all words in the Chapter.

        :return: Number of Words in the Chapter
        """
        return len(self.words())

    def content(self) -> str:
        """
        Returns the text of this Chapter as a single string.

        :return: complete Chapter content (without Chapter header).
        """
        return reduce(lambda s1, s2: s1 + s2, map(lambda s: s.content(), self.segments))

    def words(self) -> list:
        """
        Returns all words in the Chapter, without any special characters (no punctuation or quotation characters).

        :return: all words in the Chapter as a list of words
        """
        return reduce(lambda s1, s2: s1 + s2, map(lambda s: s.words(), self.segments))

    def __repr__(self):
        return '{}, Segments: {}, Words: {}'.format(self.title(), len(self.segments), self.count_words())

    def print_content(self):
        """
        Creates a formatted string that represents the content of this chapter.
        :return: Formatted chapter content.
        """
        print_str = ''
        for segment in self.segments:
            if segment.number != 0:
                print_str += '\n* * *\n\n'
            print_str += segment.content()

        return print_str


def chapter_to_dict(chapter: Chapter) -> dict:
    """
    Saves a Chapter object as a dict for serialisation via JSON.

    :param chapter: Chapter object
    :return: Serialized Chapter object as dict
    """
    from src.object.Segment import segment_to_dict
    return {
        'no': chapter.number,
        'pov': chapter.pov.ref_name,
        'segments': [segment_to_dict(s) for s in chapter.segments],
        'chapter_type': chapter.chapter_type.name
    }


def chapter_from_dict(obj) -> Chapter:
    """
    Loads a serialized JSON dict as a Chapter object.

    :param obj: JSON dict
    :return: Deserialized Chapter object
    """
    from src.common.character_loader import find_character_for_pov
    from src.object.Segment import segment_from_dict

    if 'no' in obj and 'pov' in obj and 'segments' in obj and 'chapter_type' in obj:
        char = find_character_for_pov(obj['pov'])
        segments = [segment_from_dict(s) for s in obj['segments']]
        return Chapter(obj['no'], char, segments, ChapterType.parse(obj['chapter_type']))
    return obj
