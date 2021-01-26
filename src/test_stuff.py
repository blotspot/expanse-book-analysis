from src.visualization import explacy
from spacy import displacy
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

from src import parse_speech_in_segment
from src.nlp.util import load_spacy
from src.common.constants import MODEL_DIR, MODEL_DATA_DIR
from src.common import load_book_by_nr, load_book

from stanza.server import CoreNLPClient


def explacy():
    book = load_book_by_nr(1)

    nlp = load_spacy('en')
    explacy.print_parse_info(nlp, book.chapter(2).content())


def ent():
    book = load_book_by_nr(1)

    nlp = load_spacy(MODEL_DIR)
    doc = nlp(book.chapter(2).content())

    for ent in doc.ents:
        if ent.label_ == 'PERSON' and ent._.coref_cluster is not None:
            print(ent._.coref_cluster)


def dep():
    book = load_book_by_nr(1)

    nlp = load_spacy('en')
    doc = nlp(book.chapter(2).content())
    displacy.serve(doc, style='dep')


def text_blob():
    book = load_book_by_nr(3)

    print(book.words()[:100])
    for chapter in book.chapters:
        blob = TextBlob(chapter.content(), analyzer=NaiveBayesAnalyzer())
        value = blob.sentiment.classification
        print("\t{} (polarity = {})".format(chapter.title(), value))


def speech():
    nlp = load_spacy('en', disable=['tokenizer', 'textcat', 'ner'])
    book = load_book_by_nr(1)
    for chapter in book.chapters:
        speech_content = ''
        for segment in chapter.segments:
            analyse_lines_of_undefined_speakers(nlp, segment)
        #     speeches = parse_speech_in_segment(nlp, segment)
        #     speech_content += speech_to_text(speeches, None)
        #
        # if len(speech_content) > 0:
        #     blob = TextBlob(speech_content)
        #     print(chapter.title())
        #     print(blob.sentences)
        #     print(blob.sentiment)


def stanza_speech():
    book = load_book_by_nr(1)
    with CoreNLPClient(
            annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'entitymentions', 'depparse', 'coref', 'quote', 'quote.attribution'],
            timeout=30000,
            memory='16G') as client:
        for chapter in book.chapters:
            for segment in chapter.segments:
                ann = client.annotate(segment.content())
                for quote in ann.quote:
                    print(quote.speaker + ":" + quote.text)


def analyse_lines_of_undefined_speakers(nlp, segment):
    in_segment = parse_speech_in_segment(nlp, segment)
    for s in in_segment:
        if s.speaker == 'N/A':
            if s.line_num > 0:
                print(segment.lines[s.line_num-1])

            print(s)

            if s.line_num + 1 < len(segment.lines):
                print(segment.lines[s.line_num+1])

            print('--------------')


def speech_to_text(spoken_lines, speaker):
    """
    Creates a single string out of a list of Speeches.

    :param spoken_lines: list of Speech objects
    :param speaker: speaker to find line from or 'None' if all lines should be returned
    :return: spoken lines as sentences in one single string.
    """
    if speaker:
        spoken_lines = list(filter(lambda s: s.speaker == speaker, spoken_lines))

    spoken_sentences = ''
    if spoken_lines:
        spoken_sentences = '\n'.join([add_sentence_end(s.spoken_line) for s in spoken_lines])

    return spoken_sentences


def add_sentence_end(sent: str):
    """
    :param sent: sentence
    :return: sentence with a fitting punctuation character
    """
    if sent.endswith(','):
        sent = sent[:-1]

    if not (sent.endswith('.') or sent.endswith('!') or sent.endswith('?')) and len(sent) > 0:
        sent = sent + '.'

    return sent + ' '


def excelcy_train():
    from excelcy import ExcelCy
    print('Train data with Excel : ' + str(MODEL_DATA_DIR / 'excelcy_train_all.xlsx'))
    ecy = ExcelCy.execute(file_path=str(MODEL_DATA_DIR / 'excelcy_train_all.xlsx'))
    ecy = ExcelCy()
    ecy.storage.prepare.add(kind='file', value=str(MODEL_DATA_DIR / 'prepare' / 'locs.xlsx'), entity='')


if __name__ == '__main__':
    # stanza_speech()
    # speech()
    # ent()
    # dep()
    # explacy()
    excelcy_train()

