#!/usr/bin/python
# coding=utf-8
#https://github.com/beefoo/text-analysis

class WordSentiment:
    def __init__(self, word, emotion, color, orientation, sentiment, subjectivity, source):
        self.word = word
        self.emotion = emotion
        self.color = color
        self.orientation = orientation
        self.sentiment = sentiment
        self.subjectivity = subjectivity
        self.source = source

    def enhancement_rate(self):
        rate = 1
        if cmp(self.subjectivity, 'strong') is 0:
            rate = rate * 2
        elif cmp(self.subjectivity, 'weak') is 0:
            rate = rate * 1.5
        else:
            rate = rate * 1
        return rate

    def score_increment(self):
        score = 0
        if cmp(self.sentiment, 'positive') is 0:
            score = score + 1
        elif cmp(self.sentiment, 'negative') is 0:
            score = score - 1
        else:
            score = score
        return score * self.enhancement_rate()



class WordScore:
    def __init__(self, word, pos, word_sentiment=WordSentiment):
        self.word = word
        self.pos = pos
        self.word_sentiment = word_sentiment

    def calculate(self):
        score = 0
        if cmp(self.pos, 'JJ') is 0:
            if cmp(self.word_sentiment.sentiment, 'positive') is 0:
                score = score + 1
            else:
                score = score - 1
        return score


class SentimentUnit:
    '''
    :param core. 名词或者动词
    '''
    def __init__(self, core, adj, advs):
        self.core = core
        self.adj = adj
        self.advs = advs

    '''
    被修饰词有可能是名次，也可能是动词。
    每个情感单元的情感度等于被修饰词的情感度和形容词的情感度之和，乘以特征词的权重，然后再乘以副词对语气的增强度。
    其中，距离被修饰词近的副词将对语气的增强度更强，距离被修饰词远的副词将对语气的增强度较弱，
    所以，修饰词离被修饰词的远近是衡量情感度的关键一个因素。
    公式：unit_sentiment = [S(word) + S(adj)] * feature_word_weight * Sum(E(adv)/distance)
    如果被修饰词没有情感度，就取形容词的情感度。如果形容词也没有情感度，则这个情感单元的情感度为零。
    '''
    def calculate(self, words, word_sentiment_dict, weights, negative_word_dict):
        core_word = str(words[self.core]).lower()
        core_weight = 1
        if core_word and core_word in weights:
            core_weight = weights[core_word]

        adj_word = str(words[self.adj]).lower()
        core_word_sentiment = word_sentiment_dict.get(core_word)
        adj_word_sentiment = word_sentiment_dict.get(adj_word)
        core_position = self.core
        score = 0
        if core_word_sentiment:
            score = score + core_word_sentiment.score_increment() * core_weight

        if adj_word_sentiment:
            core_position = self.adj
            score = score + adj_word_sentiment.score_increment()

        for adv in self.advs:
            adv_word = str(words[adv]).lower()
            if adv_word in negative_word_dict:
                score = score * -1
            adv_sentiment = word_sentiment_dict.get(adv_word)
            if adv_sentiment:
                if score is 0:
                    score = score + adv_sentiment.score_increment()
                else:
                    dist = abs(adv - core_position)
                    if dist is 0:
                        dist = 1
                    score = score * adv_sentiment.enhancement_rate() / dist

        return score


class SentenceScore:
    def __init__(self, sentiment_unit_list=[]):
        self.sentiment_unit_list = sentiment_unit_list

    def calculate(self, words, word_sentiment_dict, weights, negative_word_dict):
        score = 0
        for sentiment_unit in self.sentiment_unit_list:
            score = score + sentiment_unit.calculate(words, word_sentiment_dict, weights, negative_word_dict)
        return score
