from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, UserMixin
from models import create_user, get_user_by_username, verify_password, get_face_embedding
from deepface import DeepFace
import numpy as np
import cv2
import base64

auth_bp = Blueprint('auth', __name__)

class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.username = user_doc['username']

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        face_img = request.files['face_image']
        img_bytes = face_img.read()
        np_img = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        embedding = DeepFace.represent(img_path = img, model_name = 'SFace', enforce_detection=False)[0]["embedding"]
        embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
        if get_user_by_username(username):
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        create_user(username, password, embedding_bytes)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        face_img = request.files['face_image']
        img_bytes = face_img.read()
        np_img = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        user = get_user_by_username(username)
        if not user or not verify_password(user, password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        stored_embedding = np.frombuffer(get_face_embedding(user), dtype=np.float32)
        input_embedding = DeepFace.represent(img_path = img, model_name = 'SFace', enforce_detection=False)[0]["embedding"]
        input_embedding = np.array(input_embedding, dtype=np.float32)
        cos_sim = np.dot(stored_embedding, input_embedding) / (np.linalg.norm(stored_embedding) * np.linalg.norm(input_embedding))
        if cos_sim < 0.45:
            flash('Face authentication failed', 'danger')
            return redirect(url_for('auth.login'))
        login_user(User(user))
        flash('Login successful!', 'success')
        return redirect(url_for('transfer.panel'))
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))
