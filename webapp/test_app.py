from app import app
import pytest


@pytest.fixture
def client():
    return app.test_client()


def test_home_status(client):
    res = client.get('/')
    assert res.status_code == 200
    assert 'text/html' in res.content_type


@pytest.mark.parametrize('raw,expected', [
    ('Mario', 'Ciao Mario!'),
    ('José', 'Ciao José!'),
    ('%3Cscript%3E', '&lt;script&gt;'),
    ('%3Cbr%3E', '&lt;br&gt;'),
])
def test_hello_various_inputs(client, raw, expected):
    from urllib.parse import quote
    # treat strings containing '%' as already-encoded
    path = raw if '%' in raw else quote(raw, safe='')
    res = client.get(f'/hello/{path}')
    assert res.status_code == 200
    data = res.get_data(as_text=True)
    assert expected in data


def test_hello_empty_name(client):
    # Requesting the route with trailing slash but no name should 404
    res = client.get('/hello/')
    assert res.status_code == 404
