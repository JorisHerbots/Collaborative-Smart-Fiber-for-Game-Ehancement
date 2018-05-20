class EntityRegistrationException(Exception):
    pass


class MalformedRegisterPayloadException(Exception):
    pass


class Entity:
    def __init__(self, ipv4_address, raw_registration_string):
        """Create an entity based upon the registration data

        :type ipv4_address: ipv4 address as string
        :param raw_registration_string: MODULE_ID|UNIQUE_ID\nMODULE_ID|UNIQUE_ID\n...
        """

        # Installed components with their ID(s)
        self.ipv4_address = str(ipv4_address)
        self.components = {}
        components = str(raw_registration_string).split("\n")
        try:
            for component in components:
                module_id, unique_id = component.split('|')
                if module_id not in self.components:
                    self.components[module_id] = []
                self.components[module_id].append(unique_id)
        except ValueError:
            raise MalformedRegisterPayloadException("Given payload contains malformed data | {}"
                                                    .format(raw_registration_string))

    def has_components(self, components):
        """Check for presence of given component(s)

        :param components: list of component name ID's
        :return: true if all given components are present in the entity object, false if otherwise
        """
        # for comp in components:
        #     if comp not in self.components.keys():
        #         return False
        # return True
        return len(list(set(components) - set(self.components.keys()))) == 0


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
