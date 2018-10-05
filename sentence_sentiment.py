import nltk
import csv
import json
from word_sentiment import WordSentiment,WordScore

from nltk.corpus import opinion_lexicon


def word_tokenize():
    csv_reader = csv.reader(open("lexicons/lexicons.csv"))
    word_sentiment_dict = {}

    for i, row in enumerate(csv_reader):
        if i > 0:
            word_sentiment_obj = WordSentiment(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            word_sentiment_dict[word_sentiment_obj.word] = word_sentiment_obj
            # print word_sentiment_dict.keys()
    # print opinion_lexicon.positive()
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


if __name__ == '__main__': word_tokenize()
