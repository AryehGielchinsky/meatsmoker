create table PWM
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