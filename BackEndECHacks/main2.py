import json
import uuid
import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# from supports.database import User

app = Flask(__name__)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
# from supports.database import db

db.init_app(app)

class Transactions(db.Model):
    date_of_transction = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    details = db.Column(db.String, nullable=False)
    uuid = db.Column(db.String, nullable=False)
    user_uuid = db.Column(db.String, nullable=False)
    fraud = db.Column(db.Bool, nullable=False)

class User(db.Model):
    user_uuid = db.Column(
        db.String,
        nullable=False,
        unique=True
    )
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)


@app.route('/', methods = ['PUT']) # If the server makes a request to the base url of '/'
def main():
    if request.is_json: # Checks that the data is in json format
        content = request.get_json() # Retrieves the json content form the request
        print(content) # Just to show you want json content looks like
    return json.dumps({
        'status': 'Success!'
    }) # Returns data back to the other server making the request


@app.route('/viewTransactions', methods = ['POST'])
def view_transactions():
    if request.is_json:
        content = request.get_json()
        print(content)
    return json.dumps({
        'status': 'Success!'
    })

if __name__ == "__main__":
    app.run()
