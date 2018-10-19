import nltk
from nltk import FreqDist
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#from nltk.book import *
#fdist = FreqDist(gutenberg.words('chesterton-thursday.txt'))
# fdist = FreqDist(['select', 'a', 'a'])
# frequency_list = fdist.most_common(50)
# for item in frequency_list:
#     print item

#print fdist.most_common(50)
#print fdist
#print(*a,sep = '\n')
#[print(i) for i in a]

#f = open('data/RedDream.txt')
f = open('data/train.ft.txt')
raw = f.read()
# for line in raw.split('\n'):
#     print line
tokens = nltk.word_tokenize(raw)
print tokens
fdist = FreqDist(tokens)
frequency_list = fdist.most_common(50)

# create POS dictionary for given text
word_tag_dict = {}
tags = nltk.pos_tag(tokens)
for tag in tags:
    word_tag_dict[tag[0]] = tag[1]

for item in frequency_list:
    if cmp(word_tag_dict[item[0]], 'NN') is 0:
        print item
