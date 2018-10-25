import nltk
import csv
import json
from nltk.parse.stanford import StanfordParser
from stanfordcorenlp import StanfordCoreNLP
from word_sentiment import WordSentiment,WordScore,SentimentUnit, SentenceScore

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


def review_analyze(sentence, word_sentiment_dict, standford_nlp):
    print "~~~~~~~~~~~~~~~~~~~~~~~~Start to Analyze~~~~~~~~~~~~~~~~~~~~~~~~"
    print sentence
    words = nltk.word_tokenize(sentence)

    # part-of-speech tagging
    word_tag_dict = {}
    tags = standford_nlp.pos_tag(sentence)
    for tag in tags:
        word_tag_dict[tag[0]] = tag[1]

    dependency_list = standford_nlp.dependency_parse(sentence)
    print dependency_list
    nsubj_list = [(x, y, z) for (x, y, z) in dependency_list if cmp(x, 'nsubj') is 0]
    amod_list  = [(x, y, z) for (x, y, z) in dependency_list if cmp(x, 'amod') is 0]
    conj_list  =  [(x, y, z) for (x, y, z) in dependency_list if cmp(x, 'conj') is 0]
    sentiment_unit_list = []

    # for nsubj
    if nsubj_list:
        # for nsubj + amod
        for amod in amod_list:
            sentiment_unit_list.append(build_sentiment_unit(amod, words, dependency_list))

        for conj in conj_list:
            governor1 = find_governor(words, conj)
            dependent1 = find_dependent(words, conj)
            if is_adj(governor1, word_tag_dict) and is_adj(dependent1, word_tag_dict):
                sentiment_unit_list.append(SentimentUnit('', governor1, find_adv_list(conj[1], words, dependency_list)))
                sentiment_unit_list.append(SentimentUnit('', dependent1, find_adv_list(conj[2], words, dependency_list)))
                print governor1

    print SentenceScore(sentiment_unit_list).calculate(word_sentiment_dict)


def file_analyze():
    word_sentiment_dict = find_word_sentiment_dict()
    # eng_parser = StanfordParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
    standford_nlp = StanfordCoreNLP(r'/Users/pauljing/virtualenv_nltk/standford_lib/stanford-corenlp-full-2018-10-05',
                                    lang='en')

    f = open('data/dp_examples.txt')
    lines = f.readlines()
    for line in lines:
        review_analyze(line, word_sentiment_dict, standford_nlp)


def find_dependent(words, relation):
    #governor = words[dependency_relation[1] - 1]
    return words[relation[2] - 1]


def find_governor(words, relation):
    return words[relation[1] - 1]


def is_adj(word, word_tag_dict):
    return cmp(word_tag_dict[word], 'JJ') is 0 or cmp(word_tag_dict[word], 'JJS') is 0 or cmp(word_tag_dict[word], 'JJR') is 0


def find_adv_list(adj_num, words, dependency_list):
    return [find_dependent(words, (x, y, z)) for (x, y, z) in dependency_list if cmp(x, 'advmod') is 0 and y is adj_num]


def build_sentiment_unit(amod_relation, words, dependency_list):
    dependent = find_dependent(words, amod_relation)
    adv_list = find_adv_list(amod_relation[2], words, dependency_list)
    return SentimentUnit('', dependent, adv_list)

if __name__ == '__main__': file_analyze()
