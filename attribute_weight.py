import nltk
from nltk import FreqDist
import sys
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')


def insert(cursor, word, pos):
    cursor.execute("insert into words (word, pos) values (%s, %s)", (word, pos))

def get_cursor():
    connect = MySQLdb.connect(host="localhost", user="summer", passwd="cndnj!@#", db="reviews", port=3306, charset="utf8")
    connect.cursor()

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
#print tokens
#fdist = FreqDist(tokens)
#frequency_list = fdist.most_common(50)
print "most_common done"
# create POS dictionary for given text
# word_tag_dict = {}
tags = nltk.pos_tag(tokens)
connect = MySQLdb.connect(host="localhost", user="summer", passwd="cndnj!@#", db="reviews", port=3306, charset="utf8")
cursor = connect.cursor()
print "start insert nn"
for tag in tags:
    if cmp(tag[1], 'NN') is 0:
        cursor.execute("insert into words (name, pos) values (%s, %s)", (tag[0], 'NN'))
#         word_tag_dict[tag[0]] = tag[1]
cursor.close()
connect.commit()
connect.close()

#
# for item in frequency_list:
#     if cmp(word_tag_dict[item[0]], 'NN') is 0:
#         print item



