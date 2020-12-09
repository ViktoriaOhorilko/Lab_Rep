from flask import Flask, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from gevent.pywsgi import WSGIServer
from db import db
from Models.User_Model import User
from Models.Note_Model import Note
from Models.EditorsTable import Editors
from Controllers.User_Controller import UserController
from Controllers.Note_Controller import NoteController

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
# use POSTMAN post
@app.route('/UserCreate', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        user_data = request.args
        user_controller = UserController()
        return user_controller.create(user_data)


# link to try: http://127.0.0.1:5000/UserUpdate?id=1
@app.route('/UserUpdate', methods=['PUT'])
def update_user():
    idi = request.args.get('id')
    user_controller = UserController()
    return user_controller.update(idi)


# link to try: http://127.0.0.1:5000/UserDelete?id=1
@app.route('/UserDelete', methods=['DELETE'])
def delete_user():
    id_of_d = request.args.get('id')
    user_controller = UserController()
    return user_controller.delete(id_of_d)


# link to try: http://127.0.0.1:5000/NoteCreate?text=BuyMilk&tag=purchase&login=Severyn
@app.route('/NoteCreate', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        note_data = request.args
        note_controller = NoteController()
        return note_controller.create(note_data)


# link to try: http://127.0.0.1:5000/NoteByTag?tag=purchase2
@app.route('/NoteByTag', methods=['GET'])
def notes_by_tag():
    tag_data = request.args.get('tag')
    note_controller = NoteController()
    read_notes = note_controller.all_notes(tag_data)
    return read_notes


# http://127.0.0.1:5000/NoteByUser?user=1
@app.route('/NoteByUser', methods=['GET'])
def notes_by_user():
    note_data = request.args.get('user')
    note_controller = NoteController()
    read_notes = note_controller.all_notes_by_user_id(note_data)
    return read_notes


# link to try: http://127.0.0.1:5000/NoteUpdate?userid=2&noteid=2
@app.route('/NoteUpdate', methods=['PUT'])
def update_notes():
    note_data = request.args
    note_controller = NoteController()
    return note_controller.update_note(note_data)


# link to try: http://127.0.0.1:5000/NoteDelete?id=1
@app.route('/NoteDelete', methods=['DELETE'])
def delete_note():
    id_of_n = request.args.get('id')
    note_controller = NoteController()
    return note_controller.delete(id_of_n)


# serv = WSGIServer(('127.0.0.1', 5000), app)
# serv.serve_forever()
if __name__ == '__main__':
    app.run()
