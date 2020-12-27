import pytest
import jwt
import datetime
from app import test, create_app, db
from Models.User_Model import User
from Models.Note_Model import Note

@pytest.fixture()
def createapp():
    app = create_app()
    app.app_context().push()


@pytest.fixture()
def login_the_user():
    app = create_app()
    app.app_context().push()
    app.testing = True
    client = app.test_client()
    global token
    user_id = User.query.filter_by(user_name=username).first().id
    token = jwt.encode({'id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'])
    yield client
    app.testing = False


class TestCreateUser:

    def test1(self):
        data = {'login': 'Bodia', 'password': '1010', 'name': 'Bohdan'}
        test1 = test.post('/UserCreate', json=data)
        assert test1.status_code == 200
        assert test1.get_json() == [{'message': 'Invalid input'}, 400]

    def test2(self):
        data = {'login': 'Bodia', 'password': '22222222'}
        test2 = test.post('/UserCreate', json=data)
        assert test2.status_code == 200
        assert test2.get_json() == [{'message': 'Invalid input'}, 400]

    def test3(self):
        data = {'login': 'Sonia', 'password': '22222222', 'name': 'sonik'}
        test3 = test.post('/UserCreate', json=data)
        assert test3.status_code == 200
        assert test3.get_json() == [{"message": "User exist with such login"}, 409]

    def test4(self):
        data = {'login': 'Bodia', 'name': 'Bohdan'}
        test4 = test.post('/UserCreate', json=data)
        assert test4.status_code == 200
        assert test4.get_json() == [{'message': 'Invalid input'}, 400]

    def test5(self, createapp):
        data = {'login': 'Bodia', 'password': '22222222', 'name': 'bodik'}
        global username
        username = data['name']
        test5 = test.post('/UserCreate', json=data)
        assert test5.status_code == 200
        assert User.query.filter_by(login=str(data['login'])).first() is not None


class TestLogin:
    def test1(self):
        test1 = test.get('/log_in', json=None)
        assert test1.status_code == 401

    def test2(self):
        data = {'username': 'NoUser', 'password': '22222222'}
        test2 = test.get('/log_in', json=data)
        assert test2.status_code == 401

    def test3(self):
        data = {'username': 'bodik', 'password': '12345678'}
        test3 = test.get('/log_in', json=data)
        assert test3.status_code == 401

    def test4(self):
        data = {'username': 'bodik', 'password': '22222222'}
        test4 = test.get('/log_in', json=data)
        assert test4.status_code == 200


class TestEditUser:

    def test1(self, login_the_user):
        data = {'new_login': "super_hot_bodia"}
        headers = {'x-access-token': token}
        test1 = test.put('/UserUpdate', json=data, headers=headers)
        assert test1.status_code == 200
        assert test1.get_json() == [{"message": "User with this data already exist"}, 404]

    def test2(self, login_the_user):
        data = {'new_password': "12345678"}
        headers = {'x-access-token': token}
        test2 = test.put('/UserUpdate', json=data, headers=headers)
        assert test2.status_code == 200

    def test3(self, login_the_user):
        data = {"new_user_name": "bodia"}
        headers = {'x-access-token': token}
        test3 = test.put('/UserUpdate', json=data, headers=headers)
        assert test3.status_code == 200
        assert test3.get_json() == [{"message": "User with this data already exist"}, 404]

    def test4(self, login_the_user):
        data = {'new_login': "Bohdan"}
        headers = {'x-access-token': token}
        test4 = test.put('/UserUpdate', json=data, headers=headers)
        assert test4.status_code == 200

    def test5(self, login_the_user):
        data = {'new_user_name': "Bohdan"}
        global username
        username = "Bohdan"
        headers = {'x-access-token': token}
        test5 = test.put('/UserUpdate', json=data, headers=headers)
        assert test5.status_code == 200


class TestDeleteUser:

    def test1(self, login_the_user):
        headers = {'x-access-token': token}
        test1 = test.delete('/UserDelete', headers=headers)
        assert test1.status_code == 200
        assert User.query.filter_by(user_name=username).first() is None


@pytest.fixture()
def login_the_user_1():
    app = create_app()
    app.app_context().push()
    app.testing = True
    client1 = app.test_client()
    global token
    user_id = User.query.filter_by(user_name= "fortest").first().id
    token = jwt.encode({'id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'])
    yield client1
    app.testing = False


class TestCreateNote:

    def test1(self, login_the_user_1):
        data = {'text': "BuyMilk"}
        headers = {'x-access-token': token}
        test1 = test.post('/NoteCreate', json=data, headers=headers)
        assert test1.status_code == 200
        assert test1.get_json() == [{"message": "Invalid input"}, 400]

    def test2(self, login_the_user_1):
        data = {'text': "BuyMilk", 'tag': "purchase"}
        headers = {'x-access-token': token}
        test2 = test.post('/NoteCreate', json=data, headers=headers)
        global id_note
        id_note = Note.query.filter_by(text=data['text']).first().id
        assert test2.status_code == 200
        assert Note.query.filter_by(text=data['text']).first() is not None


class TestReadNote:

    def test1(self, login_the_user_1):
        data = {'tag': "purchase"}
        headers = {'x-access-token': token}
        test1 = test.get('/NoteByTag', headers=headers)
        assert test1.status_code == 200
        assert test1.get_json() == [{"message": "Error"}, 404]

    def test2(self, login_the_user_1):
        data = {'tag': "purchase"}
        headers = {'x-access-token': token}
        test2 = test.get('/NoteByTag', json=data, headers=headers)
        assert test2.status_code == 200

    def test3(self, login_the_user_1):
        headers = {'x-access-token': token}
        test2 = test.get('/NoteByUser', headers=headers)
        assert test2.status_code == 200


class TestEditNote:

    def test1(self, login_the_user_1):
        data = {'text': "edited"}
        headers = {'x-access-token': token}
        test1 = test.put('/NoteUpdate', headers=headers)
        assert test1.status_code == 200
        assert test1.get_json() == [{"message": "Invalid input"}, 404]

    def test2(self, login_the_user_1):
        data = {'note_id': id_note, 'new_text': "edited"}
        headers = {'x-access-token': token}
        test2 = test.put('/NoteUpdate', json=data, headers=headers)
        assert test2.status_code == 200

    def test3(self, login_the_user_1):
        data = {'note_id': id_note, 'new_text': "edited1"}
        headers = {'x-access-token': token}
        test3 = test.put('/NoteUpdate', json=data, headers=headers)
        assert test3.status_code == 200

    def test4(self, login_the_user_1):
        data = {'note_id': 1, 'new_text': "edited1"}
        headers = {'x-access-token': token}
        test4 = test.put('/NoteUpdate', json=data, headers=headers)
        assert test4.status_code == 200


class TestDeleteNote:

    def test1(self, login_the_user_1):
        data = {'id': id_note}
        headers = {'x-access-token': token}
        test1 = test.delete('/NoteDelete', headers=headers)
        assert test1.status_code == 200
        assert test1.get_json() == [{"message": "Note wasn`t deleted"}, 404]

    def test2(self, login_the_user_1):
        data = {'id': 1}
        headers = {'x-access-token': token}
        test2 = test.delete('/NoteDelete', json=data, headers=headers)
        assert test2.status_code == 200
        assert test2.get_json() == [{"message": "You don`t have access!"}, 403]

    def test3(self, login_the_user_1):
        data = {'id': id_note}
        headers = {'x-access-token': token}
        test3 = test.delete('/NoteDelete', json=data, headers=headers)
        assert test3.status_code == 200
        assert Note.query.filter_by(id=id_note).first() is None

    def test4(self, login_the_user_1):
        headers = {'x-access-token': token}
        test4 = test.get('/UserStatistic', headers=headers)
        assert test4.status_code == 200


class TestWithoutToken:

    def test1(self, login_the_user_1):
        headers = {'x-access-token': "1233455"}
        test1 = test.get('/UserStatistic', headers=headers)
        assert test1.get_json() == {'message' : 'Token is invalid!'}

    def test2(self, login_the_user_1):
        test2 = test.get('/UserStatistic', headers=None)
        assert test2.get_json() == {'message' : 'Token is missing!'}

# pytest -q Tests.py
# coverage run -m --omit 'C:\Users\Administrator\.virtualenvs\*' pytest Tests.py
# coverage report --omit 'C:\Users\Administrator\.virtualenvs\*' -m