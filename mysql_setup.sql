CREATE Database my_tables
;

create table my_tables.smoke_session
	(smoke_session_id int NOT NULL AUTO_INCREMENT,
	date_time DATETIME,
	meat_type VARCHAR(255),
	kilos FLOAT,
	notes VARCHAR(255),
	PRIMARY KEY (smoke_session_id)
	)
;

create table my_tables.recorded_data
	(id int NOT NULL AUTO_INCREMENT,
	smoke_session_id int,
	date_time DATETIME,
	temp0 FLOAT,
	temp1 FLOAT,
	temp2 FLOAT,
	temp3 FLOAT,
	PRIMARY KEY (id),
	INDEX (smoke_session_id)
	)
;
	
create table my_tables.PWM
	(id int NOT NULL AUTO_INCREMENT,
	smoke_session_id int,
	date_time DATETIME,
	curr_temp FLOAT,
	desired_temp FLOAT,
	duty_cycle_p FLOAT,
	duty_cycle_i FLOAT,
	duty_cycle_d FLOAT,
	duty_cycle FLOAT,
	PRIMARY KEY (id),
	INDEX (smoke_session_id)
	)
;
