from engine import httpserver
import requests


def test_httpserver_availability():
    # {"info" : "GET not supported"}
    s = httpserver.run_server(None)
    r = requests.get("http://127.0.0.1:8080")
    assert r.status_code == 200
    assert r.content == b'{"info" : "GET not supported"}'
    httpserver.stop_server(s)
