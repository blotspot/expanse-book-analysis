import logging
import os

from src.common import REFERENCES_DIR, load_book_titles, LOGGER_FORMAT


def create_link(book, name):
    """
    Create a link for one character in a directory that corresponds to the given books name.
    :param book: name of the book the character appears in
    :param name: name of the character (should be the name of the txt file that contains this characters aliases)
    """
    file_name = '{}.txt'.format(name)
    src_file = REFERENCES_DIR / 'characters' / file_name
    link_dir = REFERENCES_DIR / 'characters' / book
    link_file = link_dir / file_name

    if not link_dir.exists():
        os.mkdir(link_dir)
    if link_file.exists():
        LOG.info('remove existing link_file "%s"', link_file)
        os.remove(link_file)

    LOG.info('create "%s" ...', link_file)
    os.symlink(src_file, link_file)


def create_links(book: str, names: list):
    """
    Create the links for all characters in one book.
    :param book: book name
    :param names: list of character names
    """
    for name in set(names):
        create_link(book, name)


def create_links_for_books():
    """
    Create the character links for all novels.
    """
    books = load_book_titles()

    create_links(books[0], [
        'Holden',
        'Naomi',
        'Alex',
        'Amos',
        'Shed',
        'Miller',
        'Julie',
        'Dresden',
        'Dawes',
        'Shaddid',
        'Fred',
        'Havelock',
        'Muss',
        'Sematimba',
        'Kelly',
        'Gomez',
        'Ade',
        'Becca',
        'McDowell',
        'Diogo'])

    create_links(books[1], [
        'Holden',
        'Naomi',
        'Alex',
        'Amos',
        'Miller',
        'Bobbie',
        'Avasarala',
        'Arjun',
        'Errinwright',
        'Nguyen',
        'Mao',
        'Strickland',
        'Soren',
        'Fred',
        'Basia',
        'Larson',
        'Wendell',
        'Prax'])

    create_links(books[2], [
        'Holden',
        'Naomi',
        'Alex',
        'Amos',
        'Miller',
        'Bobbie',
        'Fred',
        'Avasarala',
        'Monica',
        'Cohen',
        'Anna',
        'Tilly',
        'Julie',
        'Clarissa',
        'Serge',
        'Ren',
        'Stanni',
        'Corin',
        'Ashford',
        'Cortez',
        'Pa',
        'Sam',
        'Bull'])

    create_links(books[3], [
        'Holden',
        'Naomi',
        'Alex',
        'Amos',
        'Miller',
        'Bobbie',
        'Avasarala',
        'Fred',
        'Elvi',
        'Fayez',
        'Murtry',
        'Havelock',
        'Koenen',
        'Wei',
        'Reeve',
        'Marwick',
        'Lucia',
        'Felcia',
        'Jacek',
        'Coop',
        'Cate',
        'Carol',
        'Basia'])

    create_links(books[4], [
        'Holden',
        'Naomi',
        'Alex',
        'Amos',
        'Miller',
        'Bobbie',
        'Clarissa',
        'Avasarala',
        'Fred',
        'Dawes',
        'Pa',
        'Marco',
        'Monica',
        'Erich',
        'Smith',
        'Lydia',
        'Rona',
        'Morris',
        'Butch',
        'Erich',
        'Drummer',
        'Cyn',
        'Filip'])

    create_links(books[5], [
        'Holden',
        'Naomi',
        'Alex',
        'Amos',
        'Bobbie',
        'Miller',
        'Clarissa',
        'Avasarala',
        'Prax',
        'Fred',
        'Dawes',
        'Rosenfeld',
        'Rodriguez',
        'Sanjrani',
        'Shaddid',
        'Pa',
        'Filip',
        'Roberts',
        'Evans',
        'Jakulski',
        'Vandercaust',
        'Josep',
        'Bertold',
        'Oksana',
        'Laura',
        'Nadia',
        'Anna',
        'Salis',
        'Marco'])

    create_links(books[6], [
        'Holden',
        'Naomi',
        'Alex',
        'Amos',
        'Bobbie',
        'Miller',
        'Clarissa',
        'Avasarala',
        'Drummer',
        'Katria',
        'Saba',
        'Cortázar',
        'Singh',
        'Duarte',
        'Tanaka',
        'Overstreet',
        'Vaughn',
        'Fisk',
        'Jordano',
        'Tur',
        'Tanaka',
        'Houston',
        'Natalia',
        'Trejo'])

    create_links(books[7], [
        'Holden',
        'Naomi',
        'Alex',
        'Amos',
        'Bobbie',
        'Miller',
        'Jillian',
        'Ian',
        'Caspar',
        'Chava',
        'Emma',
        'Sagale',
        'Elvi',
        'Fayez',
        'Travon',
        'Jen',
        'Duarte',
        'Teresa',
        'Connor',
        'Muriel',
        'Muskrat',
        'Cortázar',
        'Ilich',
        'Trejo',
        'Drummer',
        'Sagale',
        'Saba'])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)
    LOG = logging.getLogger(__name__)

    create_links_for_books()
