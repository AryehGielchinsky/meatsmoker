# meatsmoker
Python SQL linux meat smoker monitering and control

This Github repository contains the software side of my charcoal and wood fired meat smoker. The temperature is controlled by a fan attached to the smoker which increases airflow when the temperature is too low, and decreases airflow when the temperaure is too high. This repository has been very helpful working on a desktop and pushing code changes to my raspberry pi.

The hardware description will follow soon...



write_temp_to_db: 
This script is run on the raspberry pi. It reads the temperature of the smoker and meat, and sends the data to a google cloud MYSQL db.

control fan: 
This script is run on the raspberry pi. It reads the temperature history from the db, implements a PID (propertional, intergral, derivative) controller, and records some info for debugging to the db.

moniter smoker:
This script can be run on a diffrent computer. It can be used for keeping an eye on the smoker and debug the PID controller.

send alert:
This script can be run on a diffrent computer. It the smoker or meat temperature goes out of predefined temperature bands it will snd an alert to the users phone. The alert is recieved with an app called Automate.



smoke_session_id needs to be changed manually in each script if you want to distinguish diffrent cooking sessions.
