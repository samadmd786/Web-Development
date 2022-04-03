CREATE TABLE IF NOT EXISTS `experiences` (
`experience_id`        int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'The experience id',
`position_id`           int(11)  NOT NULL                	COMMENT 'Position Id', 
`name`           varchar(100)  NOT NULL                	COMMENT 'The name of the experience',
`description`     varchar(1000)  DEFAULT NULL            	COMMENT 'description of experience',
`hyperlink`        varchar(100)  DEFAULT NULL            	COMMENT 'hyperlink of experience',
`start_date`          Datetime  DEFAULT NULL            	COMMENT 'start date.',
`end_date`            Datetime   DEFAULT NULL            	COMMENT 'end date',  
PRIMARY KEY  (`experience_id`),
FOREIGN KEY (position_id) REFERENCES positions(position_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Experience I am affiliated with";