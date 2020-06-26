#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = '{"alert":"True", "smoker_temp":250, "meat_temp":160}'

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
run()