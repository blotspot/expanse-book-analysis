import spacy
from spacy import displacy
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

from expanseanalyzer import parse_speech_in_segment
from expanseanalyzer.common.constants import MODEL_DIR
from expanseanalyzer.common import load_book_by_nr


def ent():
    book = load_book_by_nr(4)

    nlp = spacy.load(MODEL_DIR)
    doc = nlp(book.content())
    print(doc.sentiment)
    displacy.serve(doc, style='ent')


def dep():
    book = load_book_by_nr(1)

    nlp = spacy.load('en_core_web_lg')
    doc = nlp(book.content())
    displacy.serve(doc, style='dep')


def text_blob():
    book = load_book_by_nr(3)

    print(book.words()[:100])
    for chapter in book.chapters:
        blob = TextBlob(chapter.content(), analyzer=NaiveBayesAnalyzer())
        value = blob.sentiment.classification
        print("\t{} (polarity = {})".format(chapter.title(), value))


def speech():
    nlp = spacy.load('en_core_web_sm', disable=['tokenizer', 'textcat', 'ner'])
    book = load_book_by_nr(1)
    speech_content = ''
    for chapter in book.chapters:
        for segment in chapter.segments:
            in_segment = parse_speech_in_segment(segment, nlp)
            if in_segment:
                speech_content += add_sentence_end(' '.join([add_sentence_end(s[1]) for s in in_segment]))
                # print('\n'.join([': '.join(s) for s in in_segment]))
    blob = TextBlob(speech_content)
    print(blob.sentences)
    print(blob.sentiment)


def add_sentence_end(sent: str):
    if not (sent.endswith('.') or sent.endswith('!') or sent.endswith('?')):
        return sent + '. '
    else:
        return sent


if __name__ == '__main__':
    speech()
