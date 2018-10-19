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
