import os

from src.common import constants
from src.object.Character import Character


def load_characters_from_dir(book_dir) -> list:
    """
    Loads characters from a specific directory.
    The directory should contain txt files with the reference name of a character as file name
    and a list of aliases as content.

    :param book_dir: file path to the book
    :return: list of Character objects
    """
    characters = set()
    names = set()
    for (_, _, filenames) in os.walk(book_dir):
        for filename in filenames:
            if filename != 'persons.txt':
                ref_name = filename.split('.')[0]
                if ref_name not in names:
                    names.add(ref_name)
                    alt_names = open((book_dir / filename).resolve(), 'r').read().split('\n')
                    characters.add(Character(ref_name, alt_names))

    return sorted(characters, key=lambda c: c.ref_name)


def load_all_characters() -> list:
    """
    Loads all Characters with all their name combinations (first name, last name, nickname)

    :return: list of Character objects
    """
    book_dir = constants.REFERENCES_DIR / 'characters'
    return load_characters_from_dir(book_dir)


def load_characters_for_book(book: str) -> list:
    """
    Loads all Characters for a specific book with all their name combinations (first name, last name, nickname)

    :param book: name of the book
    :return: list of Character objects
    """
    book_dir = constants.REFERENCES_DIR / 'characters' / book
    return load_characters_from_dir(book_dir)


ALL_CHARACTERS = load_all_characters()


def find_character_for_pov(pov: str) -> Character:
    """
    finds a Character object that corresponds to the given pov character name
    :param pov: character name (usually the name given in chapter header)
    :return: Character object of the given pov character name
    """
    return next(
        filter(lambda c: c.appears_in([pov]), ALL_CHARACTERS),
        Character(pov, [pov])
    )
