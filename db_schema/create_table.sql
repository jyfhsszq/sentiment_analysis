USE `reviews`;

DROP TABLE IF EXISTS `sentiments`;
CREATE TABLE `sentiments` (
    `Id` BIGINT(20) NOT NULL  AUTO_INCREMENT COMMENT 'sequence Id',
    `lineNumber` BIGINT(20) NOT NULL COMMENT 'line number',
    `sentiment` DOUBLE COMMENT 'sentiment value',
    PRIMARY KEY (`id`),
    KEY `idx01` (`id`)
) ENGINE=INNODB CHARSET=utf8 COMMENT='review sentiment';

DROP TABLE IF EXISTS `train`;
CREATE TABLE `train` (
    `Id` BIGINT(20) NOT NULL  AUTO_INCREMENT COMMENT 'sequence Id',
    `lineNumber` BIGINT(20) NOT NULL COMMENT 'line number',
    `value` VARCHAR(100) NOT NULL COMMENT 'sentiment value',
    PRIMARY KEY (`id`),
    KEY `train_idx01` (`id`)
) ENGINE=INNODB CHARSET=utf8 COMMENT='train data sentiment';

DROP TABLE IF EXISTS `logs`;
CREATE TABLE `train` (
    `Id` BIGINT(20) NOT NULL  AUTO_INCREMENT COMMENT 'sequence Id',
    `log` VARCHAR(10000) NOT NULL COMMENT 'logs',
    PRIMARY KEY (`id`),
    KEY `train_idx01` (`id`)
) ENGINE=INNODB CHARSET=utf8 COMMENT='train data sentiment';