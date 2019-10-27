# Read me
## database
### identified_objects
`
CREATE TABLE `identified_objects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` bigint(8) NOT NULL,
  `count` smallint(2) NOT NULL,
  `type` smallint(2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `timestamp_IDX` (`timestamp`) USING BTREE,
  KEY `identified_objects_FK` (`type`),
  CONSTRAINT `identified_objects_FK` FOREIGN KEY (`type`) REFERENCES `object_types` (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1
`
### object types
`
CREATE TABLE `object_types` (
  `name` varchar(100) NOT NULL,
  `type` smallint(6) NOT NULL,
  UNIQUE KEY `type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
`
