CREATE TABLE IF NOT EXISTS `leaderboard` (
`gameId`        int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'The game id',
`word`           varchar(100)  NOT NULL                	COMMENT 'hidden word', 
`user`           varchar(100)  NOT NULL                	COMMENT 'user who played the game',
`time`     varchar(300)  DEFAULT NULL            	COMMENT 'Time taken to guess the word',
`date`     varchar(300)         DEFAULT NULL                             COMMENT 'help to find word of the day',
PRIMARY KEY  (`gameid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="game leaderboard";