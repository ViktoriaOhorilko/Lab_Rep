from flask import Flask, request, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import check_password_hash
from functools import wraps
from gevent.pywsgi import WSGIServer
from db import db
from Models.User_Model import User
from Models.Note_Model import Note
from Models.EditorsTable import Editors
from Controllers.User_Controller import UserController
from Controllers.Note_Controller import NoteController
import datetime
import jwt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key'
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


def _token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated




# link to try: http://127.0.0.1:5000/UserCreate?login=Sonia&password=1111&name=sonik
# http://127.0.0.1:5000/UserCreate?login=Severyn&password=2111&name=shu
# use POSTMAN post
@app.route('/UserCreate', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        user_data = request.args
        user_controller = UserController()
        return user_controller.create(user_data)


@app.route('/log_in')
def login():
    data=request.authorization

    if not data or not data.username or not data.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user=User.query.filter_by(user_name=data.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, data.password):
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


# link to try: http://127.0.0.1:5000/UserUpdate?new_user_name

@app.route('/UserUpdate', methods=['PUT'])
@_token_required
def update_user(current_user):
    data = request.args
    user_controller = UserController()
    return user_controller.update(current_user.id, data)


# link to try: http://127.0.0.1:5000/UserDelete

@app.route('/UserDelete', methods=['DELETE'])
@_token_required
def delete_user(current_user):
    user_controller = UserController()
    return user_controller.delete(current_user.id)


# link to try: http://127.0.0.1:5000/NoteCreate?text=BuyMilk&tag=purchase&login=Severyn
@app.route('/NoteCreate', methods=['GET', 'POST'])
@_token_required
def create_note(current_user):
    if request.method == 'POST':
        note_data = request.args
        note_controller = NoteController()
        return note_controller.create(note_data,current_user)


# link to try: http://127.0.0.1:5000/NoteByTag?tag=purchase2
@app.route('/NoteByTag', methods=['GET'])
@_token_required
def notes_by_tag(current_user):
    tag_data = request.args.get('tag')
    note_controller = NoteController()
    read_notes = note_controller.all_notes(tag_data)
    return read_notes


# http://127.0.0.1:5000/NoteByUser?user=1
@app.route('/NoteByUser', methods=['GET'])
@_token_required
def notes_by_user(current_user):
    note_controller = NoteController()
    read_notes = note_controller.all_notes_by_user_id(current_user.id)
    return read_notes


# link to try: http://127.0.0.1:5000/NoteUpdate?&noteid=2
@app.route('/NoteUpdate', methods=['PUT'])
@_token_required
def update_notes(current_user):
    note_data = request.args
    note_controller = NoteController()
    return note_controller.update_note(current_user.id, note_data)


# link to try: http://127.0.0.1:5000/NoteDelete?id=1
@app.route('/NoteDelete', methods=['DELETE'])
@_token_required
def delete_note(current_user):
    id_of_n = request.args.get('id')
    note_controller = NoteController()
    return note_controller.delete(current_user.id,id_of_n)


# link to try: http://127.0.0.1:5000/UserStatistic
@app.route('/UserStatistic', methods=['GET'])
@_token_required
def user_statistic(current_user):
    return Editors.read_user_editions(current_user.id)


# serv = WSGIServer(('127.0.0.1', 5000), app)
# serv.serve_forever()
if __name__ == '__main__':
    app.run()
