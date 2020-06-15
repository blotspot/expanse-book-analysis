import gzip
import json
import os

from pathlib import Path

from src.common import constants
from src.object import Book, book_to_dict, book_from_dict


def load_book_titles() -> list:
    """
    Loads a list of all novel book titles.

    :return: list of book titles
    """
    file = constants.REFERENCES_DIR / 'booktitles.txt'
    books = open(file.resolve(), 'r').read().split('\n')
    return [book.strip('\n\r') for book in books]


def load_books(novels_only: bool = False) -> list:
    """
    Load books either from a compressed .json.gz file in {PROJECT_DIR}/data/interim (create files with make_dataset.py)
    or parses books from {PROJECT_DIR}/data/raw .txt files

    :param novels_only: True: only novels will be loaded, False: will also load novellas
    :return: list of Book objects
    """
    books = []
    for (dir_path, _, filenames) in os.walk(constants.INTERIM_DATA_DIR):
        filenames = [name for name in filenames if name.endswith('.json.gz')]
        for filename in filenames:
            book = load_compressed(Path(dir_path) / filename)
            if not novels_only or book.is_novel():
                books.append(book)

    books = load_missing_books_from_raw(novels_only, books)

    return sorted(books, key=lambda b: b.number)


def load_missing_books_from_raw(novels_only: bool, found_books: list):
    """
    Loads all books that aren't in `found_books` from the raw text file.

    :param novels_only: only load novels
    :param found_books: list of books already loaded
    :return: list of missing books
    """
    from src.common.parser import book_name_from_path, book_number_from_path, parse_book

    titles = [book.title for book in found_books]
    for (dir_path, _, filenames) in os.walk(constants.RAW_DATA_DIR):
        if len(filenames) > 0:
            book_title = book_name_from_path(dir_path)
            book_number = book_number_from_path(dir_path)
            if (not novels_only or book_number % 1 == 0) and book_title not in titles:
                found_books.append(parse_book(book_title))

    return found_books


def load_book_by_nr(number: int) -> Book:
    """
    Loads a book by its (publishing) number as Book object.

    Only works for novels.

    :param number: number of the book (starting with 1)
    :return: Book
    """
    books = load_book_titles()

    return load_book(books[number - 1])


def load_book(title: str) -> Book:
    """
    Loads a book by its title as Book object.

    :param title: title of the book
    :return: Book
    """
    file = constants.INTERIM_DATA_DIR / '{}.json.gz'.format(title)
    return load_compressed(file)


def load_compressed(file: Path) -> Book:
    """
    Loads a json string out of a .json.gz file and creates a valid Book object.

    :param file: path to gzipped json file
    :return: Book object created from compressed json file
    """
    with gzip.GzipFile(file, 'rb', compresslevel=constants.JSON_COMPRESS_LVL) as f_in:
        json_str = f_in.read().decode('utf-8')

    return json.loads(json_str, object_hook=book_from_dict)


def save_compressed(book: Book):
    """
    Saves a Book object into a json string and saves it in a compressed .json.gz file.

    :param book: book to save
    """
    json_str = json.dumps(book_to_dict(book))
    file = constants.INTERIM_DATA_DIR / '{}.json.gz'.format(book.title)

    with gzip.GzipFile(file, 'wb', compresslevel=constants.JSON_COMPRESS_LVL) as f_out:
        f_out.write(json_str.encode('utf-8'))
