from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from backend.db import db

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        sandi = request.form['password']
        nama = request.form['name']

        # Cek email sudah ada
        user_exist = db.collection('users').where('email', '==', email).get()
        if user_exist:
            flash('Email sudah terdaftar!', 'danger')
            return redirect(url_for('auth.register'))

        # Hash password sebelum disimpan
        sandi_hash = generate_password_hash(sandi, method='pbkdf2:sha256', salt_length=16)

        # Simpan ke Firestore
        db.collection('users').add({
            'name': nama,
            'email': email,
            'password': sandi_hash
        })

        flash('Registrasi berhasil, silakan login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        sandi = request.form['password']

        # Cek admin
        admin_docs = db.collection('admin').where('email', '==', email).get()
        if admin_docs:
            admin_data = admin_docs[0].to_dict()
            sandi_tersimpan = admin_data.get('password', '')

            # Cek password hash dulu
            if sandi_tersimpan.startswith('pbkdf2:'):
                if check_password_hash(sandi_tersimpan, sandi):
                    session['user'] = email
                    session['is_admin'] = True
                    flash('Login admin berhasil!', 'success')
                    return redirect(url_for('dashboard.dashboard'))
            else:  # fallback untuk password plain text lama
                if sandi == sandi_tersimpan:
                    session['user'] = email
                    session['is_admin'] = True
                    flash('Login admin berhasil (plain)!', 'success')
                    return redirect(url_for('dashboard.dashboard'))

        # Cek user
        user_docs = db.collection('users').where('email', '==', email).get()
        if user_docs:
            user_data = user_docs[0].to_dict()
            sandi_tersimpan = user_data.get('password', '')

            # Cek password hash
            if sandi_tersimpan.startswith('pbkdf2:'):
                if check_password_hash(sandi_tersimpan, sandi):
                    session['user'] = email
                    session['is_admin'] = False
                    flash('Login berhasil!', 'success')
                    return redirect(url_for('main.index'))
            else:  # fallback untuk password plain text lama
                if sandi == sandi_tersimpan:
                    session['user'] = email
                    session['is_admin'] = False
                    flash('Login berhasil (plain)!', 'success')
                    return redirect(url_for('main.index'))

        flash('Email atau password salah.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logout berhasil.', 'info')
    return redirect(url_for('auth.login'))