create table PWM (
	id int NOT NULL AUTO_INCREMENT,
	smoke_session_id int,
	date_time DATETIME,
	curr_temp float,
	desired_temp float,
	duty_cycle_p float,
	duty_cycle_i float,
	duty_cycle_d float,
	duty_cycle float,
	PRIMARY KEY (id)	
)

