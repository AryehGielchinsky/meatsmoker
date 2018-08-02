#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 14:51:30 2018

@author: aryeh
"""

import pymysql.cursors
import os

 
def get_smoke_session(connection):
    try:
        cursor = connection.cursor()
        sql = """select max(id) as smoke_session_id from smoke_session"""
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0]['smoke_session_id'] #not sure why it returns a list with a dict in it
    except Exception as inst:
        print('get_smoke_session {}'.format(inst) )  
        

def get_connection():
    #get DB info
    login_info = {}
    with open(os.path.expanduser('~/passwords/meat_smoker_mysql_info.txt')) as f:
        for line in f:
            (key, val) = line.split()
            login_info[key] = val

    # Connect to the database
    connection = pymysql.connect(host=login_info['host'],
                                 user=login_info['user'],
                                 password=login_info['password'],
                                 db=login_info['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
    
    return connection, login_info