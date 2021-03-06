#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 14:51:30 2018

@author: aryeh
"""

import pymysql.cursors
import os
import pandas as pd
       

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


def hit_db(sql, connection):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall() #returns a list of dicts
        connection.commit()
        
        # The results are a list of dicts. I generally want to put them into a df, or get one record
        if len(result)>1:
            return pd.DataFrame(result)
        elif len(result) == 1:
            return result[0]
        else:
            pass
        
    except Exception as inst:
        print('Error is: {}'.format(inst) )
        print('SQL is: {}'.format(sql))


def get_last_smoke_session_id(connection):
    sql = """select max(smoke_session_id) as smoke_session_id from smoke_session"""
    return hit_db(sql, connection)['smoke_session_id']
    


def read_data(table_name, smoke_session_id, connection):
    sql = """select *
             from {0}
             where smoke_session_id = {1}
             """.format(table_name, smoke_session_id)

    return hit_db(sql, connection)

    

        
        
        
        
        
        
        
        
        