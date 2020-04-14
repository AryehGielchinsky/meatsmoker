import pandas as pd
from my_functions import get_smoke_session
from my_functions import get_connection
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output



def read_data(Smoke_Session_ID, connection, read_type = 'PWM'):
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






app = dash.Dash(__name__)
    


app.layout = html.Div(
        [
                dcc.Graph(id='the_graph')
                ,html.Button('Click To Refresh', id='my-button', n_clicks=0)
                ]
        )
                        
@app.callback(
        Output('the_graph', 'figure')
        , [Input('my-button', 'n_clicks')]
        )
def on_click(n_clicks):
    connection, login_info = get_connection()
    Smoke_Session_ID = get_smoke_session(connection)
    df=pd.DataFrame( read_data(Smoke_Session_ID, connection, 'smoker_temps') )
    data = [
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
    layout = dict(
            xaxis={'title': 'time'}
            ,yaxis={'title': 'temp'}
            ,legend={'x': 0, 'y': 1}
            ,hovermode='closest'
            ) 
    
    df = None
    return {'data':data
            ,'layout':layout
            }
   
    
    
                        
                        
if __name__ == '__main__':
#    app.run_server(debug=True)
    app.run_server(host= '0.0.0.0')

