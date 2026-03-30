from flask import Flask, redirect
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from pymongo import MongoClient
from auth import auth_bp, User
from transfer import transfer_bp
import os
from flask_wtf.csrf import generate_csrf
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/securetransfer')

csrf = CSRFProtect(app)
login_manager = LoginManager(app)

mongo = MongoClient(app.config['MONGO_URI'])
db = mongo.get_database()

app.register_blueprint(auth_bp)
app.register_blueprint(transfer_bp)

@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf())

@app.route('/')
def index():
    return redirect('/login')

@login_manager.user_loader
def load_user(user_id):
    from models import get_user_by_id
    user_doc = get_user_by_id(user_id)
    return User(user_doc) if user_doc else None

if __name__ == '__main__':
    app.run(debug=True)
