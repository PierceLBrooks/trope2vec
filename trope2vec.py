from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models.word2vec import Word2Vec
from nltk.tokenize import word_tokenize

import argparse
from distutils.util import strtobool

import logging
logging.basicConfig(level=logging.DEBUG)

import os
import sys
import json

from util import *
from datetime import datetime

SEED = 42
VDIM = 200 # dimension of vectors
WSIZE = 50 # window size


def prepare_datasets(references, summaries):
    limit = 100

    summary_data = []
    with open(summaries, "r") as descriptor:
        data = json.loads(descriptor.read())
        length = len(list(data.keys()))
        index = 0
        for key in data:
            summary_data.append(TaggedDocument(words=word_tokenize(data[key]), tags=[key]))
            index += 1
            if (index%limit == 0):
                now = datetime.now()
                print(now.strftime("%d-%m-%Y@%H:%M:%S"))
                print(key+" @ "+str(index)+" / "+str(length))

    logging.debug(summary_data[:int(float(limit)**0.5)])

    reference_data = []
    with open(references, "r") as descriptor:
        data = json.loads(descriptor.read())
        length = len(list(data.keys()))
        index = 0
        for key in data:
            reference = data[key]
            for context in reference:
                destinations = reference[context]
                tokens = word_tokenize(context)
                for destination in destinations:
                    reference_data.append(list(flatten([key, destination, tokens])))
            index += 1
            if (index%limit == 0):
                now = datetime.now()
                print(now.strftime("%d-%m-%Y@%H:%M:%S"))
                print(key+" @ "+str(index)+" / "+str(length))

    return summary_data, reference_data


# initialize document vector with pv-dm (retrofitting mode)
def pretraining(summary_data):
    if not os.path.exists("./models/pv-dm.txt"):
        model = Doc2Vec(
            vector_size=VDIM,
            window=WSIZE,
            epochs=5,
            dm=1, # use pv-dm
            workers=1, # to ensure reproducibility
            seed=SEED
        )
        model.build_vocab(summary_data, min_count=1)

        logging.info("--- Pre-training started. ---")
        model.train(
            summary_data,
            epochs=model.epochs,
            total_examples=model.corpus_count
        )
        logging.info("--- Pre-training ended. ---")

        # save pre-trained doc2vec as word2vec format file 
        with open("./models/pv-dm.txt", "w") as descriptor:
            descriptor.write(f"{len(summary_data)} {VDIM}\n")

            for k in model.docvecs.doctags:
                descriptor.write(f"{k} {' '.join([str(i) for i in model[k].tolist()])}\n")
        logging.info("--- Pre-trained doc2vec saved. ---")


# hyperdoc2vec
def training(reference_data, retrofit):
    if ((retrofit and not os.path.exists("./models/t2v-retrofit.model"))
        or (not retrofit and not os.path.exists("./models/t2v-random.model"))):
        model = Word2Vec(
            size=VDIM,
            window=WSIZE,
            negative=1000,
            sg=0, # use CBOW model
            cbow_mean=1, # use average vector
            workers=10, # to ensure reproducibility
            seed=SEED
        )

        model.build_vocab(reference_data, min_count=1)
        if retrofit:
            model.intersect_word2vec_format("./models/pv-dm.txt", lockf=1.0, binary=False)

        logging.info("--- Training started. ---")
        model.train(
            reference_data,
            epochs=100,
            total_examples=model.corpus_count
        )
        logging.info("--- Training ended. ---")

        type_string = "retrofit" if retrofit else "random"
        model.save(f"./models/t2v-{type_string}.model")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--retrofit', default=str(True))
    parser.add_argument('--references')
    parser.add_argument('--summaries')
    args = parser.parse_args()

    retrofit = strtobool(args.retrofit)
    references = args.references
    summaries = args.summaries
    summary_data, reference_data = prepare_datasets(references, summaries)

    #sys.exit(0)

    if retrofit:
        pretraining(summary_data)

    training(reference_data, retrofit)

    type_string = "retrofit" if retrofit else "random"
    model = Word2Vec.load(f"./models/t2v-{type_string}.model")
    #print("IN vectors")
    #print(len(model.wv.vectors))
    #print(model.wv.vocab)
    #print(model.wv.vectors)
    print("OUT vectors")
    print(len(model.trainables.syn1neg))
    print(model.trainables.syn1neg)
