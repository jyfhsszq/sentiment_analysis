SELECT count(*) FROM reviews.words where name = 'logistics';

SELECT name, count(*) as cnt FROM reviews.words 
where name not in ('i','%','book','movie','time','cd','album', 'one','lot','nothing','something','anyone','lot')
group by name order by cnt desc

PN: product name


product level: book movie time cd album product file film music game song video sound video gift
               novel 
attribute level: story, way, quality, money, life, thing, price, author, version, prlblem
band item voice picture size person player color brand level age volumn seller photo audio

service level: service time logistics delivery suuport respnse


experience level: 
effect/result/impact: fun love waste taster help horror trouble mood experience interesting

other: 