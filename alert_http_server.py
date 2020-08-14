#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import numpy as np
import json
from my_functions import get_last_smoke_session_id, get_connection, read_data



def check_meat_temp(temps):
    current_meat_temp=temps['meat_temp']
    desired_meat_temp=203
    warning_degrees=2
    
    if current_meat_temp >= desired_meat_temp - warning_degrees:
        return True
    else:
        return False
    
    
def check_smoker_temp(temps):
    current_smoker_temp=temps['smoker_temp']
    desired_smoker_temp=250
    leeway=30
    
    if (desired_smoker_temp - leeway) < current_smoker_temp < (desired_smoker_temp + leeway) :
        return False
    else:
        return True   
    
def check_time(temps):
    if temps['smoker_delay'] < 60:
        return False
    else:
        return
        
    

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        
        temps={}
        
        df = read_data('recorded_data', smoke_session_id, connection).tail(1)
        
        temps['smoker_temp'] = df.temp0.values[0]
        temps['meat_temp'] = df.temp1.values[0]
        temps['smoker_delay'] = (datetime.datetime.now() - df.date_time)/np.timedelta64(1, 's')
            
        print(temps)
        
        message={}
        message['alert']=check_meat_temp(temps) | check_smoker_temp(temps) | check_time(temps)
        message['alert'] = str(message['alert'])
        message.update(temps)
        message = json.dumps(message) #stringify
    #    message = datetime.datetime.now().strftime('%y/%m/%d %H:%M:%S')

        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(message))
        self.end_headers()

        self.wfile.write(bytes(message, "utf8"))
        return



def run():
    server = ('', 8080)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()
    
    
if __name__ == "__main__":
    print('Starting server')

    connection, login_info = get_connection()
    smoke_session_id = get_last_smoke_session_id(connection)

    run()
