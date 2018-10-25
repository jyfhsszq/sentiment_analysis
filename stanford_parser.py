#!/usr/bin/python
# coding=utf-8

'''
#set the classpath firstly
export STANFORD_PARSER_PATH="$HOME/virtualenv_nltk/standford_lib"
export STANFORD_PARSER="$STANFORD_PARSER_PATH/stanford-parser.jar"
export STANFORD_MODELS="$STANFORD_PARSER_PATH/stanford-parser-3.9.1-models.jar"
'''


from nltk.parse.stanford import StanfordParser
from stanfordcorenlp import StanfordCoreNLP
eng_parser = StanfordParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

print list(eng_parser.parse("the quick brown fox jumps over the lazy dog".split()))

nlp = StanfordCoreNLP(r'/Users/pauljing/virtualenv_nltk/standford_lib/stanford-corenlp-full-2018-10-05', lang='en')  # 英文使用 lang='en'

#sentence = "the quick brown fox jumps over the lazy dog"
#sentence = "Bills on ports and immigration were submitted by Senator Brownback, Republican of Kansas"
#sentence = "The is a good book."
sentence = "The is a good book."

# print nlp.word_tokenize(sentence)
print nlp.pos_tag(sentence)
print nlp.parse(sentence)
print nlp.dependency_parse(sentence)

f = open('data/dp_examples.txt')
lines = f.readlines()
for line in lines:
    print nlp.pos_tag(line)
    print nlp.dependency_parse(line)
