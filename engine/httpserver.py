from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from threading import Thread
from .logger import initiate_logger
from . import config


_logger = initiate_logger(__name__, config.debug)


def create_handler_class_with_queue(queue):
    class EngineHTTPHandler(BaseHTTPRequestHandler):
        """Engine HTTP Server

        Minimalistic goal of receiving entity configurations
        """

        def __init__(self, *args, **kwargs):
            self.queue = queue

            super(EngineHTTPHandler, self).__init__(*args, **kwargs)

        def _set_headers(self, response_code=200):
            self.send_response(response_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

        def do_GET(self):
            self._set_headers()
            self.wfile.write(b'{"info" : "GET not supported"}')

        def do_POST(self):
            if self.queue is None:
                return
            data_as_string = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
            self.queue.put(data_as_string)

            # TODO: Reply if correct? of simple ack reply

    return EngineHTTPHandler


def run_server(configuration_queue, host ='127.0.0.1', port=8080):
    """Setup and run the server in a serve forever modus

    To stop the server, a shutdown needs to be issued.
        Use wrapper function stop_server(server)

    :param configuration_queue: queue object
    :param host: where to publish the server
    :param port: port to listen on
    :return: HTTPServer instance
    """
    _logger.info("Initialising Engine HTTP server in separate thread.")
    server = HTTPServer((host, port), create_handler_class_with_queue(configuration_queue))
    Thread(target=server.serve_forever).start()
    return server


def stop_server(server_instance):
    """Issue a shutdown to the given server instance

    :param server_instance:
    """
    _logger.info("Halting Engine HTTP server.")
    server_instance.shutdown()
