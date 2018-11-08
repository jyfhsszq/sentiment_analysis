#coding=utf-8
import threading
from time import ctime,sleep
import math
import MySQLdb

def process(start, end):
    connect = MySQLdb.connect(host="localhost", user="summer", passwd="cndnj!@#", db="reviews", port=3306,
                              charset="utf8")
    cursor = connect.cursor()

    f = open('/Users/pauljing/Downloads/amazonreviews/train.ft.txt')
    raw = f.read()
    ln = 0
    insert_count = 0
    p_count = 0
    for line in raw.split("\n"):
        ln = ln + 1
        if end >= ln >= start:
            p_count = p_count + 1
            if line.startswith('__label__1'):
                insert_count = insert_count + 1
                insert(cursor, ln, '-1')

            if line.startswith('__label__2'):
                insert_count = insert_count + 1
                insert(cursor, ln, '1')

            if ln % 10000 is 0:
                connect.commit()

    connect.commit()
    cursor.close()
    connect.close()
    print "insert count: % s" % insert_count
    print "processed count: % s" % p_count

def insert(cursor, line_number, val):
    cursor.execute("insert into train (lineNumber, value) values (%s, %s)", (line_number, val))

if __name__ == '__main__':
    threads = []
    total = 1820772
    chunk = 300000
    thread_count = int(math.ceil(total/chunk)) + 1
    for i in range(0, thread_count):
        startIndex = i*chunk + 1
        endIndex = (i+1)*chunk
        new_thread = threading.Thread(target=process, args=(startIndex, endIndex))
        threads.append(new_thread)

    for t in threads:
        #t.setDaemon(True)
        t.start()

    t.join()
