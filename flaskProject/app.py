from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route('/api/v1/hello-world-18')
def hello_world():
    return 'Hello World 18 !'


serv = WSGIServer(('127.0.0.1', 5000), app)
serv.serve_forever()
