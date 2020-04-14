create table cpu_temp (
	id int NOT NULL AUTO_INCREMENT,
	smoke_session_id int,
	date_time DATETIME,
	cpu_temp VARCHAR(255),
	PRIMARY KEY (id)	
)

