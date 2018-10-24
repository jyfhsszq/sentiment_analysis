import nltk
import csv
import json
from nltk.parse.stanford import StanfordParser
from stanfordcorenlp import StanfordCoreNLP
from word_sentiment import WordSentiment,WordScore

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

    dependency_list = standford_nlp.dependency_parse(sentence)
    print dependency_list
    amod_list = [(x, y, z) for (x, y, z) in dependency_list if cmp(x, 'amod') is 0]

    if amod_list:
        dependency_relation = amod_list[0]
        governor = words[dependency_relation[1]-1]
        dependent = words[dependency_relation[2]-1]
        word_sentiment = word_sentiment_dict.get(dependent)
        score = 0
        if cmp(word_sentiment.sentiment, 'positive') is 0:
            score = score + 1
        else:
            score = score - 1
        print score

def file_analyze():
    word_sentiment_dict = find_word_sentiment_dict()
    # eng_parser = StanfordParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
    standford_nlp = StanfordCoreNLP(r'/Users/pauljing/virtualenv_nltk/standford_lib/stanford-corenlp-full-2018-10-05',
                                    lang='en')

    f = open('data/dp_examples.txt')
    lines = f.readlines()
    for line in lines:
        review_analyze(line, word_sentiment_dict, standford_nlp)



if __name__ == '__main__': file_analyze()
