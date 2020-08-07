#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import json



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
    leeway=25
    
    if (desired_smoker_temp - leeway) < current_smoker_temp < (desired_smoker_temp + leeway) :
        return False
    else:
        return True   
    
    
    

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        
        # this here for testing. should pull from db
        temps={}
        temps['smoker_temp'] = 257.3
        temps['meat_temp'] = 195
        
        message={}
        message['alert']=check_meat_temp(temps) | check_smoker_temp(temps)
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
    
print('Starting server')
run()
