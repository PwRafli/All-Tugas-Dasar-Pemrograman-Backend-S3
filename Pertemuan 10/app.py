from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# Folder upload
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Buat folder jika belum ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Koneksi MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["Pertemuan9"]
collection = db["barangUKM"]


# ========================
# ROUTE: READ
# ========================
@app.route('/')
def index():
    data = list(collection.find())
    return render_template('index.html', data=data)


# ========================
# ROUTE: CREATE
# ========================
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']        # ganti dari 'name' → 'nama'
        harga = request.form['harga']
        jumlah = request.form['jumlah']

        file = request.files['file']
        filename = None

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        collection.insert_one({
            "kode": kode,
            "nama": nama,
            "harga": harga,
            "jumlah": jumlah,
            "gambar": filename
        })

        return redirect(url_for('index'))

    return render_template("add.html")


# ========================
# ROUTE: UPDATE
# ========================
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    item = collection.find_one({"_id": ObjectId(id)})

    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        jumlah = request.form['jumlah']

        file = request.files['file']
        filename = item.get("gambar")  # gunakan gambar lama jika tidak upload baru

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        update_data = {
            "kode": kode,
            "nama": nama,
            "harga": harga,
            "jumlah": jumlah,
            "gambar": filename
        }

        collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )

        return redirect(url_for('index'))

    return render_template('edit.html', item=item)


# ========================
# ROUTE: DELETE
# ========================
@app.route('/delete/<id>')
def delete(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


# ========================
# RUN APP
# ========================
if __name__ == '__main__':
    app.run(debug=True)

# ========================
# END OF FILE
# ========================