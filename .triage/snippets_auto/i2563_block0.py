from flask import Flask
app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.filters['somefilter'] = lambda s: s

@app.route('/')
def hello_world():
    return 'Hello, World!'
