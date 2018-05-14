class Engine:
    def __init__(self, game_name="Unknown"):
        # Game Name this Engine represents
        self.game_name = game_name

        # Map of all triggers that correspond to a given event
        self.event_triggers = {}

    def add_event_trigger(self, event_name, trigger_pointer):
        """Add a trigger to a given event name

        Decorator functionality event_trigger() available

        :param event_name: alle event names should ideally be strings, if not they'll be converted to strings
        :param trigger_pointer: method call for the trigger
        """
        event_name = str(event_name).lower()
        if event_name not in self.event_triggers:
            self.event_triggers[event_name] = []

        if trigger_pointer not in self.event_triggers[event_name]:
            self.event_triggers[event_name].append(trigger_pointer)

    def event_trigger(self, event_name):
        """A decorator used to add a method as an event trigger

        :param event_name: the event name, see add_event_trigger() for more information
        """

        def decorator(f):
            self.add_event_trigger(event_name, f)
            return f

        return decorator