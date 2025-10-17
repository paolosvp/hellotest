# hellotest

![CI](https://github.com/paolosvp/hellotest/actions/workflows/ci.yml/badge.svg) ![Codecov](https://codecov.io/gh/paolosvp/hellotest/branch/master/graph/badge.svg)

Semplice webapp di esempio in Python/Flask con test.

## Quickstart

- Creare un virtualenv:

  python3 -m venv venv
  source venv/bin/activate
  pip install -r webapp/requirements.txt

- Eseguire l'app Flask (sviluppo):

  python webapp/app.py

- Eseguire i test:

  pytest webapp/test_app.py

## Note

- Le rotte implementate sono `/` e `/hello/<nome>`.
- I file originali sono salvati come `webapp/*.bak`.
- Per la produzione usare `gunicorn` o altro server WSGI.
