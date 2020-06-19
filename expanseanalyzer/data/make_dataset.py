# -*- coding: utf-8 -*-
import logging
import os
from itertools import product

import pandas as pd
import spacy
import textacy

from expanseanalyzer.common import constants
from expanseanalyzer.common.book_io import save_compressed, load_books, load_missing_books_from_raw
from expanseanalyzer.nlp import CharacterRelationship, CentralityCalculator


def main(input_filepath):
    """
    Main method that generates all necessary data.
    :param input_filepath: path to the data dir where the books should be stored as .txt or .json.gz
    """
    if constants.FORCE_INTERIM_SAVE:
        LOGGER.info('Save raw TXT as compressed JSON files ...')
        generate_interim_data()

    LOGGER.info('loading books from "%s" ...', input_filepath.resolve())
    books = load_books(novels_only=True)

    LOGGER.info('process data ...')
    generate_processed_data(books, constants.FORCE_PROCESSED_SAVE)
    LOGGER.info('Done.')


def generate_interim_data():
    """
    Generates gzip json book files form a input txt file
    """
    books = load_missing_books_from_raw(False, [])
    for book in books:
        save_compressed(book)


def generate_processed_data(books, overwrite):
    """
    Calculates the following stats and writs the results into csv files:
     * character relationships over the books
     * character centralities over the books
     * text stats for all books

    :param books: list of Book objects
    :param overwrite: flag that indicates if files that already exist should be overwritten
    """
    create_relationship_csv(books, overwrite)
    calculate_centralities(books)
    calculate_text_stats(books, overwrite)


def create_relationship_csv(books, overwrite):
    """
    Calculates the relationship for each character with every other character in the books.
    :param books: list of Book objects
    :param overwrite: flag that indicates if files that already exist should be overwritten
    """
    from expanseanalyzer.common.character_loader import load_characters_for_book

    output_file = constants.PROCESSED_DATA_DIR / constants.RELATIONSHIP_CSV_FILENAME

    if not os.path.exists(output_file) or overwrite:
        csv_data = {constants.CSV_CHAR_BOOK: [],
                    constants.CSV_CHAR_SRC: [],
                    constants.CSV_CHAR_TRG: [],
                    constants.CSV_CHAR_HITS: [],
                    constants.CSV_CHAR_MENT: [],
                    constants.CSV_CHAR_IMPR: []}
        for book in books:
            chars = load_characters_for_book(book.title)
            prod = []
            for prod_tpl in product(chars, chars):
                if prod_tpl[0] != prod_tpl[1] and [prod_tpl[1], prod_tpl[0]] not in prod:
                    prod.append(list(prod_tpl))
            for char_tuple in prod:
                rel = CharacterRelationship(char_tuple[0], char_tuple[1])
                rel.find_in_book(book)
                if rel.have_relationship():
                    LOGGER.info('found pairing %s x %s in %s', char_tuple[0], char_tuple[1], book.title)
                    add_relationship_data(csv_data, rel.result, book.title, char_tuple[0], char_tuple[1])
                    add_relationship_data(csv_data, rel.result, book.title, char_tuple[1], char_tuple[0])

        dfr = pd.DataFrame(csv_data)
        dfr.to_csv(output_file, index=False, encoding='utf-8')


def add_relationship_data(data, dist, book_title, source, target):
    """
    adds the results of the relationship calculation to the data frame.
    :param data: data frame
    :param dist: distance between source and target
    :param book_title: name of the book
    :param source: source character
    :param target: target character
    """
    data[constants.CSV_CHAR_BOOK].append(book_title)
    data[constants.CSV_CHAR_SRC].append(source.ref_name)
    data[constants.CSV_CHAR_TRG].append(target.ref_name)
    data[constants.CSV_CHAR_HITS].append(dist[constants.CSV_CHAR_HITS])
    data[constants.CSV_CHAR_MENT].append(dist[source.ref_name])
    data[constants.CSV_CHAR_IMPR].append(dist[constants.CSV_CHAR_HITS] / dist[source.ref_name])


def calculate_centralities(books):
    """
    Calculates the centralities for each character in every given book.
    :param books: list of Book objects
    """
    relationship_df = pd.read_csv(constants.PROCESSED_DATA_DIR / constants.RELATIONSHIP_CSV_FILENAME)

    for book in books:
        output_file = constants.PROCESSED_DATA_DIR / constants.CENTRALITY_CSV_FILENAME.format(book.title)
        characters = sorted(set(relationship_df[(relationship_df.book == book.title)].source))
        data = {}
        mentions = {}
        # create a dictionary like:
        # {
        #   'sourceCharacter': {
        #     'targetCharacter 1': 0.1232,
        #     'targetCharacter 2': 0.23,
        #     ...
        #   }
        # }

        for character in characters:
            data.update({character: {}})
            mentions.update({character: {}})
            for sdf in relationship_df[(relationship_df.book == book.title) & (relationship_df.source == character)]:
                data[character].update({sdf.target: sdf.importance})
                mentions.update({character: sdf.mentions})

        centrality = CentralityCalculator(characters, data)
        LOGGER.info('Calculate centralities for %s', book.title)

        dfs = [
            pd.DataFrame.from_dict(mentions, orient='index', columns=[constants.CSV_CHAR_MENT]),
            pd.DataFrame.from_dict(centrality.text_rank_nx(), orient='index', columns=[constants.CENT_CSV_TR]),
            pd.DataFrame.from_dict(centrality.text_rank(), orient='index', columns=[constants.CENT_CSV_OTR]),
            pd.DataFrame.from_dict(centrality.eigenvector_nx(), orient='index', columns=[constants.CENT_CSV_EV]),
            pd.DataFrame.from_dict(centrality.eigenvector(), orient='index', columns=[constants.CENT_CSV_OEV]),
            pd.DataFrame.from_dict(centrality.katz_centrality_nx(), orient='index', columns=[constants.CENT_CSV_KATZ]),
            pd.DataFrame.from_dict(centrality.katz_centrality(), orient='index', columns=[constants.CENT_CSV_OKATZ]),
            pd.DataFrame.from_dict(centrality.degree(), orient='index', columns=[constants.CENT_CSV_DEG]),
            pd.DataFrame.from_dict(centrality.harmonic(), orient='index', columns=[constants.CENT_CSV_HARM]),
            pd.DataFrame.from_dict(centrality.closeness(), orient='index', columns=[constants.CENT_CSV_CLSNS]),
            pd.DataFrame.from_dict(centrality.betweenness_nx(), orient='index', columns=[constants.CENT_CSV_BTWN])
        ]

        out_df = pd.concat(dfs, join='inner', axis=1).sort_values(by=constants.CSV_CHAR_MENT, ascending=False)
        out_df.to_csv(output_file, encoding='utf-8', index_label=constants.CENT_CSV_ID)


def calculate_text_stats(books, overwrite):
    """
    Calculates the text stats of each book. Uses Textacy
    :param books: list of Book objects
    :param overwrite: flag that indicates if files that already exist should be overwritten
    """
    output_file = constants.PROCESSED_DATA_DIR / constants.TEXT_STATS_CSV_FILENAME

    if not os.path.exists(output_file) or overwrite:
        text_stats_list = list()

        nlp = spacy.load(constants.MODEL_DIR, disable=["tagger", "ner", "tokenizer", "textcat"])
        for book in books:
            LOGGER.info('Calculate TextStats %s', book.title)
            text = book.content()
            nlp.max_length = len(text)
            doc = nlp(text)
            text_stats = textacy.TextStats(doc)
            book_properties = dict()
            book_properties['book'] = book.title
            book_properties.update(text_stats.readability_stats)
            book_properties.update(text_stats.basic_counts)
            text_stats_list.append(book_properties)

        text_df = pd.DataFrame(text_stats_list)
        text_df.to_csv(output_file, index=False, encoding='utf-8')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format=constants.LOGGER_FORMAT)
    LOGGER = logging.getLogger(__name__)

    main(constants.RAW_DATA_DIR)
