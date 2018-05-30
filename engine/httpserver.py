from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from threading import Thread
from .logger import initiate_logger
from . import config, entitymanager


_logger = initiate_logger(__name__, config.debug)


def create_handler_class_with_queue(queue, entitymanager_interface, game_start_call,
                                    is_game_running_call, new_entity_event):
    class EngineHTTPHandler(BaseHTTPRequestHandler):
        """Engine HTTP Server

        Minimalistic goal of receiving entity configurations
        """

        def __init__(self, *args, **kwargs):
            self.queue = queue
            self.entitymanager_interface = entitymanager_interface
            self._game_start_call = game_start_call

            super(EngineHTTPHandler, self).__init__(*args, **kwargs)

        def _set_headers(self, response_code=200, content_length=-1):
            """Set HTTP headers before issuing a response

            :param response_code: HTTP code
            """
            self.send_response(response_code)
            self.send_header('Content-type', 'text/plain;charset=UTF-8')
            if content_length >= 0:
                self.send_header("Content-Length", content_length)
            self.end_headers()

        def do_GET(self):
            """HTTP GET requests

            Return commands waiting in the entity queues
            """
            if self.entitymanager_interface is None:
                self._set_headers(200)
                self.wfile.write(b'Entity Interface missing, presuming testing mode')
                return

            client_ipv4 = self.client_address[0]
            if not self.entitymanager_interface.does_entity_exist(client_ipv4):
                self._set_headers(400)
                self.wfile.write(b'Unknown entity')

            commands = self.entitymanager_interface.known_entities.get(client_ipv4).pop_all_command()
            commands_as_string = "\n".join(commands)
            data = commands_as_string.encode()
            self._set_headers(response_code=200, content_length=len(data))
            self.wfile.write(data)

        def do_POST(self):
            """HTTP POST requests

            Handle new registrations if the engine is the register phase
            In running phase post requests will get handled as entity updates
            """
            if self.queue is None or self.entitymanager_interface is None:
                return

            # POST payload
            payload_as_string = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')

            # Client IPV4 address (TODO: We assume IPV4 as internet protocol)
            client_ipv4 = self.client_address[0]

            # Separate internal messages (TODO: Find better way to accomplish this)
            if client_ipv4 == "127.0.0.1" and payload_as_string == "START_GAME" and not is_game_running_call():
                self._game_start_call()
                self._set_headers(200)
                self.wfile.write(b"Game switched to RUNNING phase.")
                return

            if not is_game_running_call() and not self.entitymanager_interface.does_entity_exist(client_ipv4):
                try:
                    self.entitymanager_interface.register_entity(client_ipv4, payload_as_string)
                    new_entity_event("entity_registered",
                                     {"entity": self.entitymanager_interface.known_entities.get(client_ipv4)})
                    self._set_headers(200)
                    self.wfile.write(b"new entity registered")
                except entitymanager.EntityRegistrationException as e:
                    self._set_headers(400)
                    self.wfile.write("{}".format(e).encode())
            elif is_game_running_call():
                self.queue.put({"entity": self.entitymanager_interface.known_entities.get(client_ipv4),
                                "payload": payload_as_string})
                self._set_headers(200)
                self.wfile.write(b"new payload received")

    return EngineHTTPHandler


def run_server(configuration_queue, entitymanager_interface, game_start_call,
               is_game_running_call, new_entity_event, host ='127.0.0.1', port=8080):
    """Setup and run the server in a serve forever modus

    To stop the server, a shutdown needs to be issued.
        Use wrapper function stop_server(server)

    :param is_game_running_call:
    :param entitymanager_interface:
    :param configuration_queue: queue object
    :param host: where to publish the server
    :param port: port to listen on
    :return: HTTPServer instance
    """
    _logger.info("Initialising Engine HTTP server in separate thread.")
    server = HTTPServer((host, port), create_handler_class_with_queue(configuration_queue, entitymanager_interface,
                                                                      game_start_call, is_game_running_call,
                                                                      new_entity_event))
    Thread(target=server.serve_forever).start()
    return server


def stop_server(server_instance):
    """Issue a shutdown to the given server instance

    :param server_instance:
    """
    _logger.info("Halting Engine HTTP server.")
    server_instance.shutdown()
