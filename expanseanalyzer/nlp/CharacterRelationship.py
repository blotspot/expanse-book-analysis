from itertools import product

from expanseanalyzer.common.constants import CSV_CHAR_HITS
from expanseanalyzer.nlp.util import dist
from expanseanalyzer.object.Book import words_in_chapters, Book
from expanseanalyzer.object.Character import Character


class CharacterRelationship:
    """
    Determines if two characters have a relationship in a text, chapter or book.
    """

    def __init__(self, char1: Character, char2: Character, window: int = 15, threshold: int = 2):
        """
        :param char1: Character object
        :param char2: Character object
        :param window: lookup window of words before and after character mention
        :param threshold: amount of mentions that will count as sufficient relationship
        """
        self.threshold = threshold
        self.window = window
        self.char1 = char1
        self.char2 = char2
        self.result = {
            CSV_CHAR_HITS: 0,
            self.char1.ref_name: 0,
            self.char2.ref_name: 0
        }

    def find_in_text(self, words: list):
        """
        Calculates the relationship of two characters by looking for
        mentions of char1 and char2 within the given window in the given bag of words.

        :param words: bag of words
        """
        c1_indexes = self.char1.appearance_indices(words)
        c2_indexes = self.char2.appearance_indices(words)
        c1_mentions = len(c1_indexes)
        c2_mentions = len(c2_indexes)
        match_distances = [dist(item) for item in product(c1_indexes, c2_indexes) if 0 < dist(item) < self.window]
        hits = len(match_distances)

        self.result[CSV_CHAR_HITS] = self.result[CSV_CHAR_HITS] + hits
        self.result[self.char1.ref_name] = self.result[self.char1.ref_name] + c1_mentions
        self.result[self.char2.ref_name] = self.result[self.char2.ref_name] + c2_mentions

    def find_in_chapters(self, chapters: list):
        """
        Calculates the relationship of two characters by looking for
        mentions of char1 and char2 within the given window for each given chapter.

        :param chapters: List of Chapter objects
        """
        all_words = words_in_chapters(chapters)
        if self.char1.appears_in(all_words) and self.char2.appears_in(all_words):
            for chapter in chapters:
                for segment in chapter.segments:
                    self.find_in_text(segment.words())

    def find_in_book(self, book: Book):
        """
        Calculates the relationship of two characters by looking for
        mentions of char1 and char2 within the given window for each chapter in the book.

        :param book: Book object
        """
        self.find_in_chapters(book.chapters)

    def have_relationship(self) -> bool:
        """
        Determines if the character tuple has a relationship by testing if the number of hits is above
        the specified threshold.

        :return: True if hits between char1 and char2 are greater than the threshold, False otherwise.
        """
        return self.result[CSV_CHAR_HITS] > self.threshold
