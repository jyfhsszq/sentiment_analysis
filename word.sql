//算法：单词的数量／这里领域里单词的总数 


sELECT count(*) FROM reviews.words where name = 'logistics';

21429832

SELECT name, count(*) as cnt FROM reviews.words 
where name not in ('i','%','book','movie','time','cd','album', 'one','lot','nothing','something','anyone','lot')
group by name order by cnt desc


SELECT count(*) as cnt FROM reviews.words 
where name in ('book', 'movie', 'cd', 'album', 'product', 'film', 'music', 'game', 'song', 'video')
group by name order by cnt desc

SELECT name, count(*) as cnt, 1+count(*)/2438634 as percent FROM reviews.words 
where name in ('book', 'movie', 'cd', 'album', 'product', 'film', 'music', 'game', 'song', 'video')
group by name order by cnt desc

PN: product name


product level: book movie cd album product film music game song video sound video gift novel 




attribute level: story, way, quality, money, life, thing, price, author, version, problem
band item voice picture size person player color brand level age volumn seller photo audio 'sound'
rice
SELECT name, count(*) as cnt, 1+count(*)/440284 as percent FROM reviews.words 
where name in ('quality', 'price', 'size', 'level', 'brand', 'picture', 'sound', 'band','person','player',' color','brand','level','age',' volumn','seller','photo','audio')
group by name order by cnt desc

service level: service time logistics delivery suport respnse

logistics:9751

SELECT name, count(*) as cnt, 1+count(*)/45840 as percent FROM reviews.words 
where name in ('service', 'logistics', 'delivery', 'support', 'response', 'attitude')
group by name order by cnt desc



experience level: 
effect/result/impact: fun love waste taster help horror trouble mood experience interesting problem

SELECT name, count(*) as cnt, 1+count(*)/269309 as percent FROM reviews.words 
where name in ('fun', 'waste', 'taste', 'help', 'horror', 'trouble','experience','interest','problem')
group by name order by cnt desc

other: 