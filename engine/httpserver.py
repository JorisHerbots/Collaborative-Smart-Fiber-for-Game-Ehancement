from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from threading import Thread
from .logger import initiate_logger
from . import config, entitymanager


_logger = initiate_logger(__name__, config.debug)


def create_handler_class_with_queue(queue, entitymanager_interface):
    class EngineHTTPHandler(BaseHTTPRequestHandler):
        """Engine HTTP Server

        Minimalistic goal of receiving entity configurations
        """

        def __init__(self, *args, **kwargs):
            self.queue = queue
            self.entitymanager_interface = entitymanager_interface

            super(EngineHTTPHandler, self).__init__(*args, **kwargs)

        def _set_headers(self, response_code=200):
            self.send_response(response_code)
            self.send_header('Content-type', 'application/plain')
            self.end_headers()

        def do_GET(self):
            self._set_headers()
            self.wfile.write(b'{"info" : "GET not supported"}')

        def do_POST(self):
            if self.queue is None or self.entitymanager_interface is None:
                return

            # POST payload
            payload_as_string = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')

            client_ipv4 = self.client_address[0]
            if not self.entitymanager_interface.does_entity_exist(client_ipv4):
                try:
                    self.entitymanager_interface.register_entity(client_ipv4, payload_as_string)
                    self._set_headers(200)
                    self.wfile.write(b"new entity registered")
                except entitymanager.EntityRegistrationException as e:
                    self._set_headers(400)
                    self.wfile.write("{}".format(e).encode())
            else:
                self.queue.put({"entity": self.entitymanager_interface.known_entities.get(client_ipv4),
                                "payload": payload_as_string})
                self._set_headers(200)
                self.wfile.write(b"new payload received")

    return EngineHTTPHandler


def run_server(configuration_queue, entitymanager_interface, host ='127.0.0.1', port=8080):
    """Setup and run the server in a serve forever modus

    To stop the server, a shutdown needs to be issued.
        Use wrapper function stop_server(server)

    :param configuration_queue: queue object
    :param host: where to publish the server
    :param port: port to listen on
    :return: HTTPServer instance
    """
    _logger.info("Initialising Engine HTTP server in separate thread.")
    server = HTTPServer((host, port), create_handler_class_with_queue(configuration_queue, entitymanager_interface))
    Thread(target=server.serve_forever).start()
    return server


def stop_server(server_instance):
    """Issue a shutdown to the given server instance

    :param server_instance:
    """
    _logger.info("Halting Engine HTTP server.")
    server_instance.shutdown()
