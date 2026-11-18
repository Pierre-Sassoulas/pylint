#pylint: disable=missing-docstring,invalid-name

from flask import Flask

app = Flask(__name__)

@app.route('/')
def _foo():
    app.logger.debug('bar')
    return 'baz'
