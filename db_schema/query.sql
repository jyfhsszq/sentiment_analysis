SELECT * FROM reviews.sentiments  where sentiment between -5 and -1 order by sentiment asc;
SELECT * FROM reviews.sentiments where linenumber=505845 order by sentiment desc; 

SELECT count(1) FROM reviews.sentiments_1;

select count(*) from train where value like '__label__%'
select * from train where id > 10000 order by id desc

select * from train order by linenumber desc

select * from train where id != linenumber order by id asc

SELECT count(1) FROM reviews.sentiments_1 s
inner join reviews.train t
on s.lineNumber = t.lineNumber
where t.value = 1 and s.sentiment>0
801633


SELECT count(1) from reviews.train t where t.value = 1
select 801633/913684


truncate table train

set @row = 0;
LOAD DATA LOCAL INFILE '/Users/pauljing/Downloads/amazonreviews/train.ft.txt' INTO TABLE reviews.train
FIELDS TERMINATED BY ' '  
LINES TERMINATED BY '\n'
(value)
SET lineNumber = @row:=@row+1;

ALTER table train add INDEX `train_idx02` (`lineNumber`)
ALTER table sentiments_1 add INDEX `sentiments_1_idx02` (`lineNumber`)

show variables like '%time%'

