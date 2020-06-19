from functools import reduce

from colorama import Fore, Style

from expanseanalyzer.object.Chapter import Chapter
from expanseanalyzer.object.ChapterType import ChapterType


def words_in_chapters(chapters: list) -> list:
    """
    Returns all words in the given chapters, without any special characters (no punctuation or quotation characters)

    :param chapters: Chapter objects
    :return: all words in the given Chapters as a list of words
    """
    return reduce(lambda c1, c2: c1 + c2, map(lambda c: c.words(), chapters))


def content_in_chapters(chapters: list) -> str:
    """
    Returns the text of each given Chapter as a single string.

    :param chapters: Chapter objects
    :return: complete content of the given chapters (without Chapter header).
    """
    return reduce(lambda c1, c2: c1 + c2, map(lambda c: c.content(), chapters))


class Book:
    """
    Representation of a book
    """

    def __init__(self, title: str, number: float, chapters: list):
        """
        :param title: Book title
        :param number: Book number (starting with 1)
        :param chapters: all chapters (prologue, epilogue, interludes, chapters) of the book as Chapter objects
        """
        self.title = title
        self.number = number
        self.chapters = list(chapters)
        self._characters = list()

    def is_novel(self) -> bool:
        """
        :return: 'True' if the Book more than one Chapter, 'False' otherwise
        """
        return bool(len(self.chapters) > 1)

    def chapter(self, i: int) -> Chapter:
        """
        Return the requested Chapter starting at 0.

        Includes all chapter types (incl. Interlude, Epilogue, Prologue).

        :return: Chapter
        """
        return self.chapters[i]

    def prologue(self) -> Chapter:
        """
        Return only the Prologue Chapter of the Book.

        :return: Prologue Chapter
        """
        found = None
        for chapter in self.chapters:
            if chapter.chapter_type == ChapterType.PROLOGUE:
                found = chapter

        return found

    def epilogue(self) -> Chapter:
        """
        Return only the Epilogue Chapter of the Book.

        :return: Epilogue Chapter
        """
        found = None
        for chapter in reversed(self.chapters):
            if chapter.chapter_type == ChapterType.EPILOGUE:
                found = chapter

        return found

    def chapters_only(self) -> list:
        """
        Return only the "real" Chapters of the Book (no Interlude, Epilogue, Prologue).

        :return: All "Chapter" Chapters
        """
        return list(filter(lambda c: c.chapter_type == ChapterType.CHAPTER, self.chapters))

    def interludes(self) -> list:
        """
        Return only the interlude Chapters of the Book.

        :return: All interlude Chapters
        """
        return list(filter(lambda c: c.chapter_type == ChapterType.INTERLUDE, self.chapters))

    def chapters_by_pov(self, character) -> list:
        """
        Returns all chapters of this book that are from the POV of the given character.

        :param character: POV Character
        :return: List of all Chapters that are from the given characters POV
        """
        return [c for c in self.chapters if c.pov.ref_name == character]

    def pov_characters(self) -> list:
        """
        Goes over every chapter and gets the pov character.

        :return: a list of all Characters that have a pov-chapter in this book.
        """
        return [c.pov for c in self.chapters]

    def count_words(self) -> int:
        """
        Counts all words in the Book.

        :return: Number of Words in the book
        """
        return len(self.words())

    def words(self) -> list:
        """
        Returns all words in the book, without any special characters (no punctuation or quotation characters).

        :return: all words in the Book as a list of words
        """
        return words_in_chapters(self.chapters)

    def content(self) -> str:
        """
        Returns the text of each Chapter as a single string.

        :return: complete Book content (without Chapter header).
        """
        return reduce(lambda c1, c2: c1 + c2, map(lambda c: c.content(), self.chapters))

    def print_simple(self):
        """
        Prints a short overview of the Book object to console.
        """
        print(self._console_color() + '{} - {:33}'.format(self.number, self.title) + Style.RESET_ALL)

    def print_full(self):
        """
        Prints the full overview of the Book object to console.
        """
        print(self._console_color() + str(self) + Style.RESET_ALL)

    def _console_color(self):
        return Style.BRIGHT + Fore.BLUE if self.is_novel() else Style.DIM + Fore.LIGHTBLACK_EX

    def __repr__(self):
        print_str = '{} - {:33}'.format(self.number, self.title)
        print_str += '[Words: {:6d}] '.format(self.count_words())
        if self.is_novel():
            print_str += '('
            chapter_count = len(self.chapters_only())
            interlude_count = len(self.interludes())
            print_str += '1 Prologue, ' if self.prologue() else ''
            print_str += '{} Chapters'.format(chapter_count)
            print_str += ', {} Interlude'.format(interlude_count) if interlude_count != 0 else ''
            print_str += 's' if interlude_count > 1 else ''
            print_str += ', 1 Epilogue' if self.epilogue() else ''
            print_str += ')'
        return print_str

    def print_content(self):
        """
        Creates a formatted string that contains the whole content of this book
        (including chapter header)
        :return: book as text string
        """
        print_str = ''
        for num, chapter in enumerate(self.chapters):
            if self.is_novel():
                print_str += '\n\n{}'.format(chapter.chapter_type.name)
                if chapter.chapter_type == ChapterType.CHAPTER:
                    print_str += ' {}'.format(num)
                print_str += ': {}\n\n{}'.format(chapter.pov, chapter.print_content())
            else:
                print_str += chapter.print_content()

        return print_str


def book_to_dict(book) -> dict:
    """
    Saves a Book object as a dict for serialisation via JSON.

    :param book: Book object
    :return: Serialized Book object as dict
    """
    from expanseanalyzer.object.Chapter import chapter_to_dict

    return {
        'title': book.title,
        'number': book.number,
        'chapters': [chapter_to_dict(c) for c in book.chapters]
    }


def book_from_dict(obj) -> Book:
    """
    Loads a serialized JSON dict as a Book object.

    :param obj: JSON dict
    :return: Deserialized Book object
    """
    from expanseanalyzer.object.Chapter import chapter_from_dict

    if 'title' in obj and 'number' in obj and 'chapters' in obj:
        return Book(obj['title'], obj['number'], [chapter_from_dict(c) for c in obj['chapters']])
    return obj
