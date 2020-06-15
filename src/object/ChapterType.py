from enum import Enum


class ChapterType(Enum):
    """
    Enum for chapter types.
    """

    PROLOGUE = 1
    CHAPTER = 2
    EPILOGUE = 3
    INTERLUDE = 4

    @staticmethod
    def parse(string):
        """
        parses a string into ChapterType
        :param string: chapter type as string
        :return: corresponding ChapterType
        """
        mapping = {
            'chapter': ChapterType.CHAPTER,
            'epilogue': ChapterType.EPILOGUE,
            'prologue': ChapterType.PROLOGUE,
            'interlude': ChapterType.INTERLUDE
        }

        return mapping[string.lower()]
