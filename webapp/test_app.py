from app import app


def test_home_status():
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200


def test_hello_escaping():
    client = app.test_client()
    # URL-encoded <script> to simulate malicious input
    res = client.get('/hello/%3Cscript%3E')
    data = res.get_data(as_text=True)
    # raw <script> should not appear unescaped
    assert '<script>' not in data
    # escaped form should be present
    assert '&lt;script&gt;' in data
