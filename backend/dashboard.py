from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from backend.db import get_all_collection, db

dashboard_bp = Blueprint('dashboard', __name__)


def admin_required():
    # Pastikan user login
    if 'user' not in session:
        flash('Silakan login terlebih dahulu.', 'warning')
        return redirect(url_for('auth.login'))

    # Query admin berdasarkan email dari session
    admin_query = list(db.collection('admin').where('email', '==', session['user']).stream())

    if not admin_query:
        flash('Akses ditolak. Anda bukan admin.', 'danger')
        return redirect(url_for('main.index'))

    # Kalau lolos, fungsi tidak mengembalikan apa pun (None)


@dashboard_bp.route("/dashboard")
def dashboard():
    check = admin_required()
    if check:      # kalau dapat redirect, teruskan
        return check
    orders = get_all_collection("produk")
    return render_template('dashboard/admin.html', orders=orders)


@dashboard_bp.route("/customer")
def customer():
    check = admin_required()
    if check:
        return check
    
    # Query semua orders dari produk collection
    orders = get_all_collection("produk")
    
    # Extract unique customers dari orders
    customers_dict = {}
    for order in orders:
        customer_data = order.get('customer', {})
        email = customer_data.get('email')
        
        # Gunakan email sebagai key untuk unique customers
        if email and email not in customers_dict:
            customers_dict[email] = {
                'name': customer_data.get('name'),
                'email': email,
                'phone': customer_data.get('phone'),
                'alamat': customer_data.get('alamat'),
                'order_count': 1
            }
        elif email:
            customers_dict[email]['order_count'] += 1
    
    # Convert dict ke list
    customers = list(customers_dict.values())
    
    return render_template('dashboard/customer.html', customers=customers)


@dashboard_bp.route("/ubah/<doc_id>", methods=['POST'])
def ubah(doc_id):
    check = admin_required()
    if check:
        return check
    status_baru = request.form.get('status')
    db.collection("produk").document(doc_id).update({"status": status_baru})
    flash(f'Status diubah menjadi {status_baru}.', 'success')
    return redirect(url_for('dashboard.dashboard'))


@dashboard_bp.route("/hapus/<doc_id>")
def hapus(doc_id):
    check = admin_required()
    if check:
        return check
    db.collection("produk").document(doc_id).delete()
    flash('Pesanan dihapus.', 'success')
    return redirect(url_for('dashboard.dashboard'))