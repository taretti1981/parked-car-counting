# Read me
## database
`
CREATE TABLE parked_cars (
  id int(11) NOT NULL AUTO_INCREMENT,
  timestamp bigint(8) NOT NULL,
  number_cars smallint(2) NOT NULL,
  PRIMARY KEY (id),
  KEY parked_cars_timestamp_IDX (timestamp) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1
`