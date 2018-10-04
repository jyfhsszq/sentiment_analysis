import nltk


def word_tokenize():
    text = nltk.word_tokenize("I am a teacher")
    print text
    print nltk.pos_tag(text)


if __name__ == '__main__': word_tokenize()
