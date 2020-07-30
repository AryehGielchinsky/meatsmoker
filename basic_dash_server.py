import pandas as pd
from my_functions import get_last_smoke_session_id, get_connection, read_data
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


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
    smoke_session_id = get_last_smoke_session_id(connection)
    df = read_data('recorded_data', smoke_session_id, connection)
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

