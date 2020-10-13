import re
from os import walk

from pathlib import Path

from src.common.constants import RAW_DATA_DIR
from src.object import Book, ChapterType, Chapter, Segment, Speech


def book_name_from_path(book_path):
    """
    Parses the book title from a directory string.

    :param book_path: path of the currently parsed book
    :return: book title
    """
    return re.search(r'(?<=[0-9][0-9]_).+', book_path).group(0)


def book_number_from_path(book_path: str) -> float:
    """
    Parses the book number from a directory string.

    Novellas will have a floating point value like "1.1" which indicates that it was the first novella
    to be published between book 1 and book 2.

    :param book_path: path of the currently parsed book
    :return: book number
    """
    num = int(re.findall(r'[0-9]{2}', book_path)[-1])
    return num / 10


def parse_chapters(content: list) -> list:
    """
    Reads all the line found in one book file and converts them into Chapter objects.

    Ignores blank lines.

    :param content: file content from 'book.txt'
    :return: list of chapters in a book
    """
    from src.common.character_loader import find_character_for_pov

    chapters = []
    chapter_start = -1
    current_chapter = None
    chapter_pattern = re.compile(r'^(Chapter|Epilogue|Prologue|Interlude)( )?(-?[A-Za-z]+){0,2}?:( )?')
    chapter_count = 0

    for (i, line) in enumerate(content):
        if re.search(chapter_pattern, line):
            if current_chapter:
                current_chapter.segments = parse_chapter(content[chapter_start:i])
            chapter_start = i + 1
            head = line.split(':')
            chapter_type = ChapterType.parse(head[0].split(' ')[0].strip())
            pov_character = head[-1].strip()
            char = find_character_for_pov(pov_character)
            current_chapter = Chapter(chapter_count, char, [], chapter_type)
            chapter_count += 1
            chapters.append(current_chapter)

        if len(chapters) == 0:
            from src.object.Character import Character

            # Novellas don't have chapter headers
            chapter_start = i
            current_chapter = Chapter(chapter_count, Character('', []), [], ChapterType.CHAPTER)
            chapter_count += 1
            chapters.append(current_chapter)

    # last chapter needs to be segmented too
    current_chapter.segments = parse_chapter(content[chapter_start:])

    return chapters


def parse_chapter(chapter_content: list) -> list:
    """
    parses all segments of a chapter
    :param chapter_content: content of the chapter
    :return: list of segments
    """
    segments = []
    current_segment = Segment(0, [])
    segment_pattern = re.compile(r'^\* \* \*$')
    segment_start = 0

    for (i, line) in enumerate(chapter_content):
        if re.search(segment_pattern, line):
            current_segment = parse_segment(chapter_content[segment_start:i], current_segment, segments)
            segment_start = i + 1

    parse_segment(chapter_content[segment_start:], current_segment, segments)

    return segments


def parse_segment(segment_content: list, segment: Segment, segments: list) -> Segment:
    """
    Parses a single segment in one chapter.
    :param segment_content: content of the segment
    :param segment: current segment
    :param segments: list of parsed segments
    :return: Segment object
    """
    if len(segment_content) > 0:
        segment.lines = segment_content
        segments.append(segment)
        segment = Segment(segment.number + 1, [])
    return segment


def parse_book(title: str) -> Book:
    """
    Loads the 'book.txt' file that lies in the 'data/raw/{number}_{title}' directory of this project
    and parses its content into a Book object.

    :param title: of the book
    :return: Book object
    """
    book = None
    for (dir_path, _, filenames) in walk(RAW_DATA_DIR):
        if len(filenames) > 0:
            book_number = book_number_from_path(dir_path)
            if dir_path.find(title) < 0:
                continue

            book = Book(title, book_number, [])
            book_path = Path(dir_path) / next(file for file in filenames if re.search(r'^(book)', file))
            book.chapters = parse_chapters(open(book_path.resolve(), 'r').readlines())

    return book


def parse_speech_in_segment(nlp, segment: Segment) -> list:
    """
    Parses all speeches in a segment.

    :param segment: segment
    :param nlp: spacy nlp object
    :return: list of found speeches and its speakers
    """
    speeches = []
    for i, line in enumerate(segment.lines):
        spoken_line, speaker = parse_speech(line, nlp)
        if spoken_line:
            speeches.append(Speech(speaker, spoken_line, i))

    return speeches


def parse_speech(line: str, nlp) -> tuple:
    """
    Parses the speech in a line of text.

    :param line: text line
    :param nlp: spacy nlp object
    :return: the spoken line and the speaker
    """
    speech_pattern = re.compile(r'(?<=“).*?(?=”)')
    speech = speech_pattern.findall(line)
    speaker = "N/A"
    ids = [line.index(s) + len(s) + 1 for s in speech]
    for idx in ids:
        if idx < len(line):
            doc = nlp(line.split('”')[1].split('“')[0])
            nouns = [chunk.text for chunk in doc.noun_chunks]
            if nouns:
                speaker = nouns[0].strip()

    return ' '.join(speech), speaker
