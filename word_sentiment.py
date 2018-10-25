class WordSentiment:
    def __init__(self, word, emotion, color, orientation, sentiment, subjectivity, source):
        self.word = word
        self.emotion = emotion
        self.color = color
        self.orientation = orientation
        self.sentiment = sentiment
        self.subjectivity = subjectivity
        self.source = source


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
    def __init__(self, n, adj, advs):
        self.n = n
        self.adj = adj
        self.advs = advs

    def calculate(self, word_sentiment_dict):
        word_sentiment = word_sentiment_dict.get(self.adj)
        score = 0
        if cmp(word_sentiment.sentiment, 'positive') is 0:
            score = score + 1
        elif cmp(word_sentiment.sentiment, 'positive') is 0:
            score = score - 1
        else:
            score = score

        for adv in self.advs:
            adv_sentiment = word_sentiment_dict.get(adv)
            if adv_sentiment:
                if cmp(adv_sentiment.subjectivity, 'strong') is 0:
                    score = score * 2
                elif cmp(adv_sentiment.subjectivity, 'weak') is 0:
                    score = score * 1.5
                else:
                    score = score * 1
        return score


class SentenceScore:
    def __init__(self, sentiment_unit_list=[]):
        self.sentiment_unit_list = sentiment_unit_list

    def calculate(self, word_sentiment_dict):
        score = 0
        for sentiment_unit in self.sentiment_unit_list:
            score = score + sentiment_unit.calculate(word_sentiment_dict)
        return score
