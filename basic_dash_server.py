from time import sleep
import numpy as np
import pandas as pd
import pymysql.cursors
from datetime import datetime as dt
import os
from datetime import datetime, timedelta
from my_functions import get_smoke_session
from my_functions import get_connection
import dash
import dash_core_components as dcc
import dash_html_components as html


def read_data(Smoke_Session_ID, read_type = 'PWM'):
    try:
        if read_type == 'PWM':
            table_name = 'PWM' 
        elif read_type == 'smoker_temps':
            table_name = 'recorded_data' 
        else:
            print('read_data_PWM neads a table name')
        cursor = connection.cursor()
        sql = """select * 
                from {}
                where smoke_session_id = {}
                """.format(table_name, Smoke_Session_ID)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as inst:
        print('read_data {}'.format(inst) )
        

   
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)   
    
    
        
connection, login_info = get_connection()
Smoke_Session_ID = get_smoke_session(connection)
Smoke_Session_ID=19

df=pd.DataFrame( read_data(Smoke_Session_ID, 'smoker_temps') )


app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                    dict(
                            x=df['date_time']
                            ,y=df['temp0']
                            ,text='smoker'
                            ,name='smoker'
                            )
                    ,dict(
                            x=df['date_time']
                            ,y=df['temp1']
                            ,text='meat1'
                            ,name='meat1'
                            )
                    ,dict(
                            x=df['date_time']
                            ,y=df['temp2']
                            ,text='meat2'
                            ,name='meat2'
                            )
                    
                    ]
            ,'layout': dict(
                    xaxis={'title': 'time'}
                    ,yaxis={'title': 'temp'}
                    #,margin={'l': 40, 'b': 40, 't': 10, 'r': 10}
                    ,legend={'x': 0, 'y': 1}
                    ,hovermode='closest'
                    )
            }
        )
        ]
        )

if __name__ == '__main__':
#    app.run_server(debug=True)
    app.run_server( host= '0.0.0.0')

