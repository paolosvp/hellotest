import io
from simple_server import MyHandler


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


def test_root_returns_home():
    h = _make_handler('/')
    h.do_GET()
    body = _get_body(h)
    assert 'La mia prima Web App!' in body
    assert '/hello/Mario' in body


def test_hello_name():
    h = _make_handler('/hello/Mario')
    h.do_GET()
    body = _get_body(h)
    assert 'Ciao Mario!' in body


def test_hello_escaping():
    h = _make_handler('/hello/%3Cscript%3E')
    h.do_GET()
    body = _get_body(h)
    assert '<script>' not in body
    assert '&lt;script&gt;' in body


def test_404_response():
    h = _make_handler('/notfound')
    h.do_GET()
    body = _get_body(h)
    assert '404 - Pagina non trovata' in body
