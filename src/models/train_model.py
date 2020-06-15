from __future__ import unicode_literals, print_function

import ast
import random

import pandas as pd
import spacy
from pathlib import Path
from spacy.util import minibatch, compounding

from src.common import constants


def main(model=None, output_dir=None, n_iter=250):
    """
    Load the model, set up the pipeline and train the entity recognizer.
    """
    train_data = pd.read_csv(constants.REFERENCES_DIR / 'model' / 'train_data.csv', sep=';', header=None)
    train_data = [(t[0], ast.literal_eval(t[1])) for t in train_data.values]

    labels_to_add = set()
    for data in train_data:
        if data[1].get('entities') is not None:
            labels = set([e[2] for e in data[1]['entities']])
            labels_to_add.update(labels)

    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    [ner.add_label(label) for label in labels_to_add]

    train_model(nlp, train_data, model, n_iter)
    save_model(nlp, train_data, output_dir)


def train_model(nlp, train_data, model, n_iter):
    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        if model is None:
            nlp.begin_training()
        for _ in range(n_iter):
            random.shuffle(train_data)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.60,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)


def save_model(nlp, train_data, output_dir):
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)


if __name__ == "__main__":
    # Install spacy first and download model via:
    # `python -m spacy download en_core_web_lg`
    main(model='en_core_web_lg', output_dir=constants.MODEL_DIR)
