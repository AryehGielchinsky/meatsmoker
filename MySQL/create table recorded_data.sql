create table recorded_data
	(id int NOT NULL AUTO_INCREMENT,
	smoke_session_id int,
	date_time DATETIME,
	temp0 FLOAT,
	temp1 FLOAT,
	temp2 FLOAT,
	temp3 FLOAT,
	PRIMARY KEY (id)
	)