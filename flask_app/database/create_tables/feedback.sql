CREATE TABLE IF NOT EXISTS `feedback` (
`comment_id`        int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'The comment id',
`name`           varchar(100)  NOT NULL                	COMMENT 'the commentators name',
`email`     varchar(80)  DEFAULT NULL            	COMMENT 'the commentators email',
`comment`        varchar(1000)  DEFAULT NULL            	COMMENT 'The text of the comment',
PRIMARY Key(comment_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Feedback provider";