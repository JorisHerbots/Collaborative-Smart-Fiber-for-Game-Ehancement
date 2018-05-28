from engine import httpserver
import requests


def test_httpserver_availability():
    s = httpserver.run_server(None, None, None, None, port=8081)
    r = requests.get("http://127.0.0.1:8081")
    assert r.status_code == 200
    # assert r.content == b'{"info" : "GET not supported"}'
    httpserver.stop_server(s)
