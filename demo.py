#!/usr/bin/python
# coding=utf-8

import nltk
import csv
import json
from nltk.parse.stanford import StanfordParser
from stanfordcorenlp import StanfordCoreNLP
from word_sentiment import WordSentiment,WordScore,SentimentUnit, SentenceScore
from tree import Tree
from nsubj_parser import NsubjParser

from nltk.corpus import opinion_lexicon



def dependency_parse():
    sentence = 'Tom quietly put one coin into his money box.'
    # Initialize stanford core NLP
    standford_nlp = StanfordCoreNLP(r'/Users/pauljing/virtualenv_nltk/standford_lib/stanford-corenlp-full-2018-10-05',
                                    lang='en')
    # Get pos tag by stanford core NLP
    tags = standford_nlp.pos_tag(sentence)
    print tags

    # Get dependency list by stanford core NLP
    dependency_list = standford_nlp.dependency_parse(sentence)
    print dependency_list


if __name__ == '__main__': dependency_parse()
