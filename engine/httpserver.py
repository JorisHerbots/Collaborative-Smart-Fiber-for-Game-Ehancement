from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from threading import Thread


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Engine HTTP Server

    Minimalistic goal of receiving and sending configurations to and from entities
    """

    def _set_headers(self, response_code=200):
        self.send_response(response_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(b'{"info" : "GET not supported"}')


def run_server(host = '127.0.0.1', port=8080):
    server = HTTPServer((host, port), SimpleHTTPRequestHandler)
    Thread(target=server.serve_forever).start()
    return server


def stop_server(server):
    server.shutdown()
