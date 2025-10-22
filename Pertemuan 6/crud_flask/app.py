from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Folder penyimpanan gambar
app.config['UPLOAD_FOLDER'] = 'static/Upload_Image'

# Pastikan folder upload ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Koneksi ke database MySQL
# --- IMPORTANT: Make sure your database details are correct ---
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # <-- Change if your password is different
    database="crud_db"
)
cursor = conn.cursor()

# ==============================
# 🔹 FILTER FORMAT RUPIAH
# ==============================
@app.template_filter('rupiah')
def format_rupiah(value):
    try:
        value = int(value)
        return f"Rp {value:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return "Rp 0"

# ==============================
# 🔹 HALAMAN UTAMA (TAMPIL DATA)
# ==============================
@app.route('/')
def index():
    search = request.args.get('search', '')
    if search:
        query = "SELECT * FROM stok WHERE kode LIKE %s OR nama LIKE %s"
        cursor.execute(query, (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM stok")
    data = cursor.fetchall()
    return render_template('index.html', data=data, search=search)

# ==============================
# 🔹 TAMBAH BARANG
# ==============================
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        file = request.files['file']

        foto = None
        if file and file.filename != '':
            foto = file.filename
            # Use app.root_path for an absolute path, ensuring reliability
            save_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], foto)
            file.save(save_path)

        try:
            cursor.execute("INSERT INTO stok (kode, nama, harga, foto) VALUES (%s, %s, %s, %s)",
                           (kode, nama, harga, foto))
            conn.commit()
            flash("Barang berhasil ditambahkan!", "success")
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
            conn.rollback()
        return redirect(url_for('index'))

    return render_template('add.html')

# ==============================
# 🔹 EDIT BARANG
# ==============================
@app.route('/edit/<string:kode>', methods=['GET', 'POST'])
def edit(kode):
    cursor.execute("SELECT * FROM stok WHERE kode=%s", (kode,))
    data = cursor.fetchone()

    if not data:
        flash("Barang tidak ditemukan!", "danger")
        return redirect(url_for('index'))

    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        file = request.files['file']
        old_foto = data[3]  # kolom foto

        # Jika user upload foto baru
        if file and file.filename != '':
            # Hapus foto lama dari server
            if old_foto:
                old_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], old_foto)
                if os.path.exists(old_path):
                    os.remove(old_path)
            # Simpan foto baru
            foto = file.filename
            save_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], foto)
            file.save(save_path)
        else:
            foto = old_foto  # tetap gunakan foto lama

        try:
            cursor.execute("UPDATE stok SET nama=%s, harga=%s, foto=%s WHERE kode=%s",
                           (nama, harga, foto, kode))
            conn.commit()
            flash("Data barang berhasil diperbarui!", "success")
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
            conn.rollback()
        return redirect(url_for('index'))

    return render_template('edit.html', data=data)

# ==============================
# 🔹 HAPUS FOTO SAJA
# ==============================
@app.route('/delete_photo/<string:kode>', methods=['POST'])
def delete_photo(kode):
    try:
        cursor.execute("SELECT foto FROM stok WHERE kode=%s", (kode,))
        result = cursor.fetchone()

        if result and result[0]:
            foto_filename = result[0]
            # Construct the absolute path to the file
            foto_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], foto_filename)

            # Delete file from the server if it exists
            if os.path.exists(foto_path):
                os.remove(foto_path)

            # Update database to remove the filename reference
            cursor.execute("UPDATE stok SET foto=NULL WHERE kode=%s", (kode,))
            conn.commit()
            flash("Foto berhasil dihapus secara permanen!", "success")
        else:
            flash("Tidak ada foto untuk dihapus!", "warning")

    except Exception as e:
        flash(f"Terjadi kesalahan: {e}", "danger")
        conn.rollback()

    return redirect(url_for('index'))

# ==============================
# 🔹 HAPUS BARANG
# ==============================
@app.route('/delete/<string:kode>', methods=['POST'])
def delete(kode):
    try:
        cursor.execute("SELECT foto FROM stok WHERE kode=%s", (kode,))
        result = cursor.fetchone()

        # Hapus foto dari server jika ada
        if result and result[0]:
            foto_filename = result[0]
            foto_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], foto_filename)
            if os.path.exists(foto_path):
                os.remove(foto_path)

        # Hapus data dari database
        cursor.execute("DELETE FROM stok WHERE kode=%s", (kode,))
        conn.commit()
        flash("Barang berhasil dihapus!", "danger")

    except Exception as e:
        flash(f"Terjadi kesalahan: {e}", "danger")
        conn.rollback()

    return redirect(url_for('index'))

# ==============================
if __name__ == '__main__':
    app.run(debug=True)