#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import tussam_requests as tussam


class requestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        route = self.path.lstrip("/")

        # Status code
        self.send_response(200)

        # Headers
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        # Response data
        data = tussam.get_positions(route)
        self.wfile.write(bytes(data, "utf8"))
        return


def run():
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, requestHandler)
    print('Starting tussam-tbs server...')
    httpd.serve_forever()


run()
