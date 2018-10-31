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


def find_word_sentiment_dict():
    csv_reader = csv.reader(open("lexicons/lexicons.csv"))
    word_sentiment_dict = {}

    for i, row in enumerate(csv_reader):
        if i > 0:
            word_sentiment_obj = WordSentiment(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            word_sentiment_dict[word_sentiment_obj.word] = word_sentiment_obj
    return word_sentiment_dict


def word_tokenize():
    word_sentiment_dict = find_word_sentiment_dict

    text = nltk.word_tokenize("I'm not a good teacher, she is a really beautiful girl")
    # part-of-speech tagging
    word_tag_dict = {}
    tags = nltk.pos_tag(text)
    for tag in tags:
        word_tag_dict[tag[0]] = tag[1]

    for word in text:
        sentiment_obj = word_sentiment_dict.get(word)
        if sentiment_obj is None:
            sentiment_obj = WordSentiment(word, "", "", "", "", "", "")

        word_sore = WordScore(word, word_tag_dict.get(word), sentiment_obj)

        print "%s->score:%s,tag:%s, sent:%s" % (word, word_sore.calculate(), word_tag_dict.get(word), json.dumps(sentiment_obj.__dict__))

    # print nltk.help.upenn_tagset('RB')


def sentence_analyze(sentence, word_sentiment_dict, standford_nlp):
    print "    ~~~~~~~~~~~~~~~~~~~~~~~~Start to Analyze~~~~~~~~~~~~~~~~~~~~~~~~"
    print sentence
    #words = nltk.word_tokenize(sentence)

    # part-of-speech tagging
    word_tag_dict = {}
    tags = standford_nlp.pos_tag(sentence)
    for tag in tags:
        word_tag_dict[tag[0]] = tag[1]
    words = [tag[0] for tag in tags]

    dependency_list = standford_nlp.dependency_parse(sentence)
    print dependency_list
    tree = Tree(dependency_list)
    raw_nsubj_list = [(x, y, z) for (x, y, z) in dependency_list if cmp(x, 'nsubj') is 0]
    nsubj_list = remove_dup_nsubj(raw_nsubj_list)

    #amod_list  = [(x, y, z) for (x, y, z) in dependency_list if cmp(x, 'amod') is 0]
    sentiment_unit_list = []

    # for nsubj
    if nsubj_list:
        # [(2, 1, 2), (12, 3, 13)]
        sub_tree_list = tree.find_sub_tree_by_nsubj(nsubj_list)
    else:
        sub_tree_list = [(dependency_list[0][2], 1, Tree.MAX_INT)]

    for sub_tree in sub_tree_list:
        start = sub_tree[1]
        end = sub_tree[2]
        nsubjParser = NsubjParser(tree, words, tags)
        nsubjParser.parse(sub_tree[0], start, end, sentiment_unit_list)

    return SentenceScore(sentiment_unit_list).calculate(word_sentiment_dict)


def review_analyze():
    word_sentiment_dict = find_word_sentiment_dict()
    # eng_parser = StanfordParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
    standford_nlp = StanfordCoreNLP(r'/Users/pauljing/virtualenv_nltk/standford_lib/stanford-corenlp-full-2018-10-05',
                                    lang='en')
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    #f = open('data/dp_examples.txt')
    f = open('data/one.txt')
    lines = f.readlines()
    for line in lines:
        print "####################  Start to Analyze  ####################"
        review_score = 0
        sentences = tokenizer.tokenize(line)
        for sentence in sentences:
            sentence_core = sentence_analyze(sentence, word_sentiment_dict, standford_nlp)
            print 'sentence_core: %s' % sentence_core
            review_score = review_score + sentence_core
        print 'review_score: %s' % review_score

def find_dependent(words, relation):
    #governor = words[dependency_relation[1] - 1]
    return words[relation[2] - 1]


def find_governor(words, relation):
    return words[relation[1] - 1]


def is_adj(word, word_tag_dict):
    return cmp(word_tag_dict[word], 'JJ') is 0 or cmp(word_tag_dict[word], 'JJS') is 0 or cmp(word_tag_dict[word], 'JJR') is 0


def find_adv_list(adj_num, words, dependency_list):
    return [find_dependent(words, (x, y, z)) for (x, y, z) in dependency_list if cmp(x, 'advmod') is 0 and y is adj_num]


def find_relations_by_scope(dependency_list, rel, start, end):
    return [(x, y, z) for (x, y, z) in dependency_list if cmp(x, rel) is 0 and end >= y >= start and end > z >= start]


def build_sentiment_unit(amod_relation, words, dependency_list):
    dependent = find_dependent(words, amod_relation)
    adv_list = find_adv_list(amod_relation[2], words, dependency_list)
    return SentimentUnit('', dependent, adv_list)

def remove_dup_nsubj(raw_nsubj_list):
    dict = {}
    for raw_nsubj in raw_nsubj_list:
        gov = raw_nsubj[1]
        dep = raw_nsubj[2]
        distance = abs(gov-dep)
        if gov not in dict:
            dict[gov] = (0, distance)
        else:
            old_count = dict[gov][0]
            old_distance = dict[gov][1]
            if old_distance < distance:
                distance = old_distance
            dict[gov] = (old_count + 1, distance)

    return [(x, y, z) for (x, y, z) in raw_nsubj_list if (y - z) is dict[y][1]]

if __name__ == '__main__': review_analyze()
