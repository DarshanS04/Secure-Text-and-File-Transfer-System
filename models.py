from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
import base64
import os

client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017/securetransfer'))
db = client.get_database()
users = db.users

def create_user(username, password, face_embedding):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    embedding_b64 = base64.b64encode(face_embedding).decode()
    user = {
        'username': username,
        'password_hash': password_hash,
        'face_embedding': embedding_b64
    }
    return users.insert_one(user)

def get_user_by_username(username):
    return users.find_one({'username': username})

def get_user_by_id(user_id):
    return users.find_one({'_id': ObjectId(user_id)})

def verify_password(user, password):
    return bcrypt.checkpw(password.encode(), user['password_hash'])

def get_face_embedding(user):
    return base64.b64decode(user['face_embedding'])
