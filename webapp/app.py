from flask import Flask
import sys
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>La mia prima Web App!</h1><p>Ciao mondo!</p>'

@app.route('/hello/<nome>')
def hello(nome):
    safe_nome = escape(nome)
    return f'<h1>Ciao {safe_nome}!</h1><p>Benvenuto nella mia web app!</p>'

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
