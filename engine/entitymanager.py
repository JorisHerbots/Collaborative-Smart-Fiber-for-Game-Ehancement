from .logger import initiate_logger
from threading import Lock
from . import config


_logger = initiate_logger(__name__, config.debug)


class EntityRegistrationException(Exception):
    pass


class MalformedRegisterPayloadException(Exception):
    pass


class UniqueIdUnknownException(Exception):
    pass


class Entity:
    def __init__(self, ipv4_address, raw_registration_string):
        """Create an entity based upon the registration data

        :type ipv4_address: ipv4 address as string
        :param raw_registration_string: MODULE_ID|UNIQUE_ID\nMODULE_ID|UNIQUE_ID\n...
        """

        # Installed components with their ID(s)
        self.ipv4_address = str(ipv4_address)
        self.connected_components = {}
        self._unique_id_to_module_id = {}

        self._command_backlog_mutex = Lock()
        self._command_backlog = []

        components = str(raw_registration_string).replace("\\n", "\n").split("\n")
        try:
            for component in components:
                module_id, unique_id = component.split('|')
                if module_id not in self.connected_components:
                    self.connected_components[module_id] = []
                self.connected_components[module_id].append(unique_id)

                if unique_id not in self._unique_id_to_module_id:
                    self._unique_id_to_module_id[unique_id] = module_id
                else:
                    _logger.warning("Double registration event discovered, ignoring entry. | Unique ID [{}] | Module "
                                    "ID [{}]".format(unique_id, module_id))

        except ValueError:
            raise MalformedRegisterPayloadException("Given payload contains malformed data | {}"
                                                    .format(raw_registration_string))

    def send_command(self, command):
        with self._command_backlog_mutex:
            self._command_backlog.append(str(command))

    def pop_all_command(self):
        with self._command_backlog_mutex:
            backlog_copy = self._command_backlog
            self._command_backlog = []
        return backlog_copy

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Entity(ipv4_address: {}, connected_components: {}, component_to_module_mapping: {})"\
            .format(str(self.ipv4_address), str(self.connected_components), str(self._unique_id_to_module_id))

    def has_components(self, components):
        """Check for presence of given component(s)

        :param components: list of component name ID's
        :return: true if all given components are present in the entity object, false if otherwise
        """
        # for comp in components:
        #     if comp not in self.components.keys():
        #         return False
        # return True
        return len(list(set(components) - set(self.connected_components.keys()))) == 0

    def get_module_id_from_unique_id(self, unique_id):
        """Retrieve the module corresponding to the unique ID given by a client

        Throws an exception when the unique ID doesn't exist

        :param unique_id:
        :return:
        """
        unique_id = str(unique_id)
        if unique_id not in self._unique_id_to_module_id:
            raise UniqueIdUnknownException("{} unknown".format(unique_id))
        return self._unique_id_to_module_id[unique_id]


class EntityManager:
    def __init__(self):
        # Dictionary of registered clients
        self.known_entities = {}

    def register_entity(self, ipv4_address, raw_register_payload):
        """Register a new entity

        :param ipv4_address: string
        :param raw_register_payload: string
        """
        ipv4_address = str(ipv4_address)
        if ipv4_address in self.known_entities:
            raise EntityRegistrationException("Entity with IP {} is already known to the game engine. Ignoring "
                                              "registration request.".format(ipv4_address))

        try:
            self.known_entities[ipv4_address] = Entity(ipv4_address, raw_register_payload)
        except MalformedRegisterPayloadException as e:
            raise EntityRegistrationException("Could not register new entity, Entity class throws following \"{}\""
                                              .format(e))

    def get_all_clients(self):
        return self.known_entities.values()

    def does_entity_exist(self, ipv4_address):
        """Quick check if given IP address belongs to an entity

        :param ipv4_address:
        :return:
        """
        return str(ipv4_address) in self.known_entities
