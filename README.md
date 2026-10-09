# Python Merah — Aplikasi Web E-commerce / Custom Order

Aplikasi web berbasis Flask dengan integrasi Firebase Firestore. Menyediakan sistem pemesanan produk (baju, tumbler), manajemen pesanan pengguna, profil, dan checkout.

## Tech Stack
- **Backend:** Python 3, Flask (blueprints)
- **Database:** Firebase Firestore (`firebase.json`)
- **Frontend:** HTML templates (`templates/`), CSS/JS statis (`static/`)

## Struktur Folder
- `backend/` — blueprint Flask (`auth`, `main`, `dashboard`) + `db.py`
- `templates/` — halaman HTML (`index`, `produk`, `pesanan`, `profile`, `chekout/*`)
- `static/` — CSS (`css/`), JS (`js/`), gambar (`images/`)
- `app.py` — entry point aplikasi

## Fitur Utama
- Autentikasi pengguna (`auth_bp` — login/register)
- Katalog produk (`produk.html`)
- Checkout pesanan (`baju`, `tumbler`) — menyimpan ke Firestore `produk`
- Riwayat pesanan (`pesanan`, `detail_pesanan/<id>`)
- Profil pengguna — update nama, tambah/edit alamat
- Dashboard admin (`dashboard` blueprint)

## Database Schema (Firebase Firestore)
- Koleksi `users` — data pengguna + array `addresses`
- Koleksi `produk` — pesanan dengan struktur `customer`, `order`, `status`

## Instalasi
```bash
# 1. Buat virtual environment
python -m venv venv

# 2. Aktifkan
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependensi (contoh)
pip install flask firebase-admin

# 4. Konfigurasi
Pastikan `firebase.json` sudah benar.
Set `app.secret_key` di `app.py` (saat ini hardcoded; ganti sebelum produksi).

# 5. Jalankan
python app.py
# Aplikasi berjalan di http://localhost:5000
```

## Catatan Keamanan
- `app.secret_key` saat ini hardcoded (`"supersecretkey"`). Ganti dengan key acak sebelum deploy produksi.
- Pastikan `firebase.json` tidak di-commit ke repo publik tanpa filter jika berisi kredensial sensitif.

## File Penting
- `app.py` — konfigurasi Flask + registrasi blueprint
- `backend/auth.py` — login, register, session handling
- `backend/main.py` — checkout, pesanan, profil, produk
- `backend/db.py` — koneksi Firebase
- `templates/layout/` — base template (`admin_base.html`, `user_base.html`)


