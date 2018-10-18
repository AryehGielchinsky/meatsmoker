#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 18:42:37 2018

@author: aryeh
"""

import time
from gpiozero import MCP3008
#from math import log
import pymysql.cursors
from datetime import datetime as dt
import signal 
import os
import numpy as np
from my_functions import get_smoke_session
from my_functions import get_connection
import subprocess



def write_data(cpu_temp):
 #   temp[temp is np.nan] = 'null'
    try:
        cursor = connection.cursor()
        local_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """insert into recorded_data (smoke_session_id, date_time, cpu_temp)
                  values ({}, '{}', {} )""".format(Smoke_Session_ID, local_time, cpu_temp )
        cursor.execute(sql)
            # connection is not autocommit by default. So you must commit to save your changes.
        connection.commit()
    except Exception as inst:
        print('write_date {}'.format(inst) )
        
connection, login_info = get_connection()

Smoke_Session_ID = get_smoke_session(connection)


bashCommand = "vcgencmd measure_temp"


while True:
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)
  #  write_data(output)
    slep(30)	
