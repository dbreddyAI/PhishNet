import os
import json
from uuid import uuid4

from flask import Flask, render_template, flash, request, redirect
from flask_login import LoginManager, login_required, login_user, current_user, UserMixin, logout_user
from flask_sqlalchemy import SQLAlchemy
from supports.database import db, Transactions
from supports.database import User as UserModel

from supports import date
from supports.crypto import verify, make_hash
from supports import secrets
from supports import queue
from supports import ml_connection as ml

app = Flask(__name__)
app.secret_key = secrets.flask_key

login_manager = LoginManager()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

db.init_app(app)
login_manager.init_app(app)



class User(UserMixin):
    def __init__(self, uid):
        self.id = uid

def find_user(email):
    user = UserModel.query.filter_by(email=email).first()
    return user if user is not None else None


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if find_user(email) is None:
            new_user = UserModel(
                user_uuid=str(uuid4()),
                email=email,
                password_hash=make_hash(password),
                phone=request.form.get('phone'))
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        else:
            flash("Email is already registered.")

    if request.method == 'GET':
        return render_template('registration.html')


@login_manager.user_loader
def user_loader(userid):
    return User(userid)

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user_details = find_user(email)
    if user_details is None:
        return None
    id = user_details.uuid
    user = User(id)
    user.id = user_details.uuid

    user.is_authenticated = verify(
        request.form.get('password'), user.password_hash
    )

    return user

@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_details = find_user(email)
        if user_details is not None and verify(password, user_details.password_hash):
            id = user_details.user_uuid
            user = User(id)
            user.id = user_details.user_uuid
            login_user(user)
            return redirect('/dashboard')

        return redirect('/')

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    print(current_user.id)
    transactions = Transactions.query.filter(Transactions.user_uuid == current_user.id).all()
    return render_template('transactions.html', transactions=transactions)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return flask.redirect('/')

@app.route('/api/addTransaction', methods=['POST'])
def add_transaction():
    data = request.get_json(force=True)
    store_name, location = date.sep_store_location(data.get('details'))
    uid = str(uuid4())
    new_transaction = Transactions(
        date_of_transction=date.convert_string_to_date(
            data.get('date_of_transaction')),
        amount=data.get('amount'),
        details=data.get('details'),
        uuid=uid,
        user_uuid=data.get('user_uuid'),
        location=location,
        store_name=store_name
    )


    db.session.add(new_transaction)
    db.session.commit()

    # print(ml.predict(uid))

    if data.get('train') == True:
        print('Traning model now')
        ml.initial_train(data.get('user_uuid'))

    return json.dumps({
        'status': 'Success!'
    })

@app.route('/initPredict', methods=['POST'])
def init_predict():
    data = request.get_json(force=True)
    uid = data.get('user_uuid')
    # output = queue.queue_initial_train(uid)
    ml.initial_train(uid)
    return json.dumps({
        'status': 'Success!'
    })

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/static/<path:path>')
def stat(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=80,
    )
