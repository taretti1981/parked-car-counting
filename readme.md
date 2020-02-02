# Read me
## OpenCV4 installation
Follow the instruction to install OpenCV4. OpenCV4 contains already YOLO

`
https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/
`


## External File required 
After pull the project, this file is required on the main folder


`
curl https://pjreddie.com/media/files/yolov3.weights -o yolov3.weights
`

## Database
You to set a database (mysql based). You only need two tables


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
) ENGINE=InnoDB AUTO_INCREMENT=32101 DEFAULT CHARSET=latin1
`


### object types


`
CREATE TABLE `object_types` (
  `name` varchar(100) NOT NULL,
  `type` smallint(6) NOT NULL,
  UNIQUE KEY `type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
`
