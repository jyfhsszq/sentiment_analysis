'''
#set the classpath firstly
export STANFORD_PARSER_PATH="$HOME/virtualenv_nltk/standford_lib"
export STANFORD_PARSER="$STANFORD_PARSER_PATH/stanford-parser.jar"
export STANFORD_MODELS="$STANFORD_PARSER_PATH/stanford-parser-3.9.1-models.jar"
'''


from nltk.parse.stanford import StanfordParser
eng_parser = StanfordParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

print list(eng_parser.parse("the quick brown fox jumps over the lazy dog".split()))
