from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash
from flask_login import login_required, current_user
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
import secrets
import io

transfer_bp = Blueprint('transfer', __name__)

@transfer_bp.route('/panel')
@login_required
def panel():
    return render_template('panel.html')

@transfer_bp.route('/encrypt', methods=['POST'])
@login_required
def encrypt():
    data_type = request.form['type']
    key = request.form['key']
    if not key:
        key = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
    else:
        key = base64.urlsafe_b64encode(key.encode()).decode() if len(key) != 44 else key
    aesgcm = AESGCM(base64.urlsafe_b64decode(key))
    nonce = secrets.token_bytes(12)
    if data_type == 'text':
        plaintext = request.form['plaintext'].encode()
        ct = aesgcm.encrypt(nonce, plaintext, None)
        enc_data = base64.b64encode(nonce + ct)
        return render_template('panel.html', enc_data=enc_data.decode(), key=key, mode='text')
    elif data_type == 'file':
        file = request.files['file']
        file_bytes = file.read()
        ct = aesgcm.encrypt(nonce, file_bytes, None)
        enc_file = nonce + ct
        return send_file(io.BytesIO(enc_file), as_attachment=True, download_name=file.filename + '.enc')
    flash('Encryption failed', 'danger')
    return redirect(url_for('transfer.panel'))

@transfer_bp.route('/decrypt', methods=['POST'])
@login_required
def decrypt():
    key = request.form['key']
    key = base64.urlsafe_b64encode(key.encode()).decode() if len(key) != 44 else key
    aesgcm = AESGCM(base64.urlsafe_b64decode(key))
    data_type = request.form['type']
    if data_type == 'text':
        enc_data = base64.b64decode(request.form['enc_data'])
        nonce, ct = enc_data[:12], enc_data[12:]
        try:
            pt = aesgcm.decrypt(nonce, ct, None)
            return render_template('panel.html', dec_data=pt.decode(), mode='text')
        except Exception:
            flash('Decryption failed', 'danger')
            return redirect(url_for('transfer.panel'))
    elif data_type == 'file':
        file = request.files['file']
        enc_file = file.read()
        nonce, ct = enc_file[:12], enc_file[12:]
        try:
            pt = aesgcm.decrypt(nonce, ct, None)
            return send_file(io.BytesIO(pt), as_attachment=True, download_name=file.filename.replace('.enc', ''))
        except Exception:
            flash('Decryption failed', 'danger')
            return redirect(url_for('transfer.panel'))
    flash('Decryption failed', 'danger')
    return redirect(url_for('transfer.panel'))
