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
    def __init__(self, n, adj, advs):
        self.n = n
        self.adj = adj
        self.advs = advs

    def calculate(self, word_sentiment_dict):
        word_sentiment = word_sentiment_dict.get(self.adj)
        if not word_sentiment:
            word_sentiment = word_sentiment_dict.get(self.n)

        score = 0
        if word_sentiment:
            score = score + word_sentiment.score_increment()

            for adv in self.advs:
                adv_sentiment = word_sentiment_dict.get(adv)
                if adv_sentiment:
                    score = score * adv_sentiment.enhancement_rate()

        return score


class SentenceScore:
    def __init__(self, sentiment_unit_list=[]):
        self.sentiment_unit_list = sentiment_unit_list

    def calculate(self, word_sentiment_dict):
        score = 0
        for sentiment_unit in self.sentiment_unit_list:
            score = score + sentiment_unit.calculate(word_sentiment_dict)
        return score
