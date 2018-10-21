SELECT count(*) FROM reviews.words;

SELECT name, count(*) as cnt FROM reviews.words 
where name not in ('i','%')
group by name order by cnt desc