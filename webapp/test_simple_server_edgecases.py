import io
from simple_server import MyHandler
import urllib.parse


def _make_handler(path: str) -> MyHandler:
    h = MyHandler.__new__(MyHandler)
    h.requestline = f'GET {path} HTTP/1.1'
    h.command = 'GET'
    h.path = path
    h.request_version = 'HTTP/1.1'
    h.headers = {}
    h.rfile = io.BytesIO()
    h.wfile = io.BytesIO()
    h.client_address = ('127.0.0.1', 0)
    h.server = None
    h._headers_buffer = []
    h.close_connection = False
    h.protocol_version = 'HTTP/1.1'
    return h


def _get_body(handler: MyHandler) -> str:
    raw = handler.wfile.getvalue()
    text = raw.decode('utf-8', errors='ignore')
    parts = text.split('\r\n\r\n', 1)
    return parts[1] if len(parts) == 2 else text


def test_encoded_slash_in_name():
    # %2F decodes to '/', so encoded slashes should split path — server treats segments literally
    # ensure that a name containing an encoded slash is handled as separate segments (404)
    name = 'foo%2Fbar'
    h = _make_handler(f'/hello/{name}')
    h.do_GET()
    body = _get_body(h)
    # after unquoting, the name contains '/', server includes it in response
    assert 'Ciao foo/bar!' in body


def test_name_with_spaces_and_special_chars():
    raw = 'John Doe & Co.'
    encoded = urllib.parse.quote(raw, safe='')
    h = _make_handler(f'/hello/{encoded}')
    h.do_GET()
    body = _get_body(h)
    assert 'Ciao John Doe &amp; Co.' in body


def test_very_long_name():
    long_name = 'a' * 500
    encoded = urllib.parse.quote(long_name, safe='')
    h = _make_handler(f'/hello/{encoded}')
    h.do_GET()
    body = _get_body(h)
    assert 'Ciao ' in body
    assert long_name in body
