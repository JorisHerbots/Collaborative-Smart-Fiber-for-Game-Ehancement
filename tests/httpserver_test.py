from engine import httpserver
import requests


def test_httpserver_availability():
    s = httpserver.run_server(None, None, None, None, None, port=8096)
    r = requests.get("http://127.0.0.1:8096")
    assert r.status_code == 200
    # assert r.content == b'{"info" : "GET not supported"}'
    httpserver.stop_server(s)
