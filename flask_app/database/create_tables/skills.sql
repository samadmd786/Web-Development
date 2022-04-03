CREATE TABLE IF NOT EXISTS `skills` (
`skill_id`        int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'skill Id',
`experience_id`   int(10)  NOT NULL                	COMMENT 'experience Id', 
`name`            varchar(100)  NOT NULL                	COMMENT 'The name of the skill',
`skill_level`     int(10)  DEFAULT NULL            	COMMENT 'level of skill',
PRIMARY KEY  (`skill_id`),
FOREIGN KEY (experience_id) REFERENCES experiences(experience_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="skill I have";