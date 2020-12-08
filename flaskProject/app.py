from flask import Flask, request, flash
from flask_swagger_ui import get_swaggerui_blueprint
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from gevent.pywsgi import WSGIServer
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from Models.User_Model import User
from Models.Note_Model import Note
from Controllers.User_Controller import UserController

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

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


# http://127.0.0.1:5000/api/v1/hello-world-18


@app.route('/api/v1/hello-world-18')
def hello_world():
    return 'Hello World 18 !'


# link to try: http://127.0.0.1:5000/UserCreate?login=Sonia&password=1111&name=sonik
# http://127.0.0.1:5000/UserCreate?login=Severyn&password=2111&name=shu
# use POSTMAN
@app.route('/UserCreate', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        user_data = request.args
        user_controller = UserController()
        if user_controller.create(user_data):
            return "Success added to db!"
        else:
            return "Create failed!"


# link to try: http://127.0.0.1:5000/UserRead?login=Sonia

@app.route('/UserRead', methods=['GET'])
def read_user():
    log = request.args.get('login')
    user_controller = UserController()
    read_user = user_controller.read(log)
    return "For " + read_user.login + " password : " + read_user.password + " user name: " + read_user.user_name


# link to try: http://127.0.0.1:5000/UserUpdate?id=1

@app.route('/UserUpdate', methods=['GET'])
def update_user():
    idi = request.args.get('id')
    user_controller = UserController()
    if user_controller.update(idi):
        return "Success!"
    else:
        return "Create failed!"


# serv = WSGIServer(('127.0.0.1', 5000), app)
# serv.serve_forever()
if __name__ == '__main__':
    app.run()
