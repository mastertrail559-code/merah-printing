from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.db import db, get_all_collection
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/chekout', methods=['POST', 'GET'])
def checkout():
    if 'user' not in session:
        flash('Silakan login terlebih dahulu untuk memesan.', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        user_email = session.get('user', '')
        
        order_data = {
            'customer': {
                'name': request.form['name'],
                'email': user_email,
                'phone': request.form['phone'],
                'alamat': request.form['alamat'],
                'note': request.form.get('note', "")
            },
            'order': {
                'produk': request.form['product'],
                'jumlah': request.form['quantity'],
                'mug_size': request.form.get('mug_size', ''),
                'mug_color': request.form.get('mug_color', ''),
                'print_area': request.form.get('print_area', ''),
                'pembayaran': request.form['payment_method'],
                'order_date': datetime.now(),
                'total': request.form['total_price']
            },
            'status': 'proses'
        }
        db.collection("produk").add(order_data)
        flash('Pesanan berhasil dibuat!', 'success')
        return redirect(url_for('main.success'))

    return render_template('chekout/chekout.html')

@main_bp.route('/chekout/baju', methods=['POST', 'GET'])
def checkout_baju():
    if 'user' not in session:
        flash('Silakan login terlebih dahulu untuk memesan.', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        user_email = session.get('user', '')
        
        order_data = {
            'customer': {
                'name': request.form['name'],
                'email': user_email,
                'phone': request.form['phone'],
                'alamat': request.form['alamat'],
                'note': request.form.get('note', "")
            },
            'order': {
                'produk': request.form['product'],
                'jumlah': request.form['quantity'],
                'baju_color': request.form.get('baju_color', ''),
                'baju_size': request.form.get('baju_size', ''),
                'print_type': request.form.get('print_type', ''),
                'pembayaran': request.form['payment_method'],
                'order_date': datetime.now(),
                'total': request.form['total_price']
            },
            'status': 'proses'
        }
        db.collection("produk").add(order_data)
        flash('Pesanan berhasil dibuat!', 'success')
        return redirect(url_for('main.success'))

    return render_template('chekout/baju.html')

@main_bp.route('/chekout/tumbler', methods=['POST', 'GET'])
def checkout_tumbler():
    if 'user' not in session:
        flash('Silakan login terlebih dahulu untuk memesan.', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        user_email = session.get('user', '')
        
        order_data = {
            'customer': {
                'name': request.form['name'],
                'email': user_email,
                'phone': request.form['phone'],
                'alamat': request.form['alamat'],
                'note': request.form.get('note', "")
            },
            'order': {
                'produk': request.form['product'],
                'jumlah': request.form['quantity'],
                'tumbler_color': request.form.get('tumbler_color', ''),
                'tumbler_type': request.form.get('tumbler_type', ''),
                'tumbler_size': request.form.get('tumbler_size', ''),
                'pembayaran': request.form['payment_method'],
                'order_date': datetime.now(),
                'total': request.form['total_price']
            },
            'status': 'proses'
        }
        db.collection("produk").add(order_data)
        flash('Pesanan berhasil dibuat!', 'success')
        return redirect(url_for('main.success'))

    return render_template('chekout/tumbler.html')

@main_bp.route('/chekout/success')
def success():
    return render_template('chekout/success.html')

@main_bp.route('/pesanan')
def pesanan():
    if 'user' not in session:
        flash('Silakan login terlebih dahulu.', 'warning')
        return redirect(url_for('auth.login'))
    
    user_email = session['user']
    orders = get_all_collection("produk")
    
    # Filter pesanan berdasarkan email user
    user_orders = [ord for ord in orders if ord.get('customer', {}).get('email') == user_email]
    
    return render_template('pesanan.html', orders=user_orders)

@main_bp.route('/pesanan/<order_id>')
def detail_pesanan(order_id):
    if 'user' not in session:
        flash('Silakan login terlebih dahulu.', 'warning')
        return redirect(url_for('auth.login'))
    
    user_email = session['user']
    orders = get_all_collection("produk")
    
    # Find the order by ID
    order = None
    order_ref = None
    for ord in orders:
        if ord.get('id') == order_id or ord.get('id', '')[:8].upper() == order_id.upper():
            # Check if user owns this order
            if ord.get('customer', {}).get('email') == user_email:
                order = ord
                break
    
    if not order:
        flash('Pesanan tidak ditemukan.', 'danger')
        return redirect(url_for('main.pesanan'))
    
    return render_template('detail_pesanan.html', order=order)

@main_bp.route('/profile')
def profile():
    if 'user' not in session:
        flash('Silakan login terlebih dahulu.', 'warning')
        return redirect(url_for('auth.login'))
    
    user_email = session['user']
    users = get_all_collection("users")
    
    # Cari user berdasarkan email
    user_data = None
    for u in users:
        if u.get('email') == user_email:
            user_data = u
            break
    
    if not user_data:
        flash('User tidak ditemukan.', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('profile.html', user=user_data)

@main_bp.route('/profile/update-username', methods=['POST'])
def update_username():
    if 'user' not in session:
        return {'success': False, 'message': 'Belum login'}, 401
    
    user_email = session['user']
    new_name = request.form.get('name', '').strip()
    
    if not new_name:
        return {'success': False, 'message': 'Nama tidak boleh kosong'}, 400
    
    try:
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', user_email)
        docs = query.stream()
        
        for doc in docs:
            doc.reference.update({'name': new_name})
        
        flash('Nama berhasil diperbarui!', 'success')
        return redirect(url_for('main.profile'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('main.profile'))

@main_bp.route('/profile/add-address', methods=['POST'])
def add_address():
    if 'user' not in session:
        return {'success': False, 'message': 'Belum login'}, 401
    
    user_email = session['user']
    label = request.form.get('label', '').strip()
    name = request.form.get('name', '').strip()
    alamat = request.form.get('alamat', '').strip()
    phone = request.form.get('phone', '').strip()
    
    if not all([label, name, alamat, phone]):
        flash('Semua field harus diisi', 'danger')
        return redirect(url_for('main.profile'))
    
    try:
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', user_email)
        docs = query.stream()
        
        for doc in docs:
            addresses = doc.get('addresses') or []
            new_address = {
                'label': label,
                'name': name,
                'alamat': alamat,
                'phone': phone
            }
            addresses.append(new_address)
            doc.reference.update({'addresses': addresses})
        
        flash('Alamat berhasil ditambahkan!', 'success')
        return redirect(url_for('main.profile'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('main.profile'))

@main_bp.route('/profile/update-address/<int:index>', methods=['POST'])
def update_address(index):
    if 'user' not in session:
        return {'success': False, 'message': 'Belum login'}, 401
    
    user_email = session['user']
    label = request.form.get('label', '').strip()
    name = request.form.get('name', '').strip()
    alamat = request.form.get('alamat', '').strip()
    phone = request.form.get('phone', '').strip()
    
    if not all([label, name, alamat, phone]):
        flash('Semua field harus diisi', 'danger')
        return redirect(url_for('main.profile'))
    
    try:
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', user_email)
        docs = query.stream()
        
        for doc in docs:
            addresses = doc.get('addresses') or []
            if 0 <= index < len(addresses):
                addresses[index] = {
                    'label': label,
                    'name': name,
                    'alamat': alamat,
                    'phone': phone
                }
                doc.reference.update({'addresses': addresses})
        
        flash('Alamat berhasil diperbarui!', 'success')
        return redirect(url_for('main.profile'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('main.profile'))

@main_bp.route('/produk')
def produk():
    return render_template('produk.html')

@main_bp.route('/kontak')
def kontak():
    return render_template('kontak.html')