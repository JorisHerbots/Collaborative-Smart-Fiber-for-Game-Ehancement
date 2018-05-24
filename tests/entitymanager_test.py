from engine import Engine, hardwaremanager
import requests
from engine.hardware import led, vibration_motor, three_button


def test_registration():
    e = Engine("entitymanager test")
    try:

        r1 = requests.post("http://127.0.0.1:8080", "0|0\n1|1\n0|2")
        print(r1.text)
        assert r1.status_code == 200
        assert len(e.entitymanager_interface.known_entities) == 1
        components = e.entitymanager_interface.known_entities[list(e.entitymanager_interface.known_entities.keys())[0]]\
            .connected_components
        assert len(components) == 2
        assert '0' in components["0"]
        assert '2' in components["0"]
        assert '1' in components["1"]

        required_components_true = hardwaremanager.create_lookup_list(led, three_button)
        required_components_false = hardwaremanager.create_lookup_list(three_button, vibration_motor)

        assert len(required_components_true) == 2
        assert len(required_components_false) == 2

        for client in e.entitymanager_interface.get_all_clients():
            assert client.has_components(required_components_true)
            assert not client.has_components(required_components_false)

        e.cleanup_interfaces()
    except Exception:
        e.cleanup_interfaces()
        raise
