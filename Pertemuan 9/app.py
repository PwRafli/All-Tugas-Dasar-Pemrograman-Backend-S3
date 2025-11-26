from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
Bootstrap(app)

# -----------------------
# KONEKSI MONGODB
# -----------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["Pertemuan9"]
collection = db["barangUKM"]

# -----------------------
# FILTER: Format Harga Indonesia
# -----------------------
@app.template_filter()
def format_harga(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", ".")
    except:
        return value

# -----------------------
# READ
# -----------------------
@app.route('/')
def index():
    items = list(collection.find().sort("kode", 1))   # WAJIB list()
    return render_template('index.html', items=items)

# -----------------------
# CREATE
# -----------------------
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = {
            'kode': request.form['kode'],
            'nama': request.form['nama'],
            'harga': int(request.form['harga']),
            'jumlah': int(request.form['jumlah'])
        }
        collection.insert_one(data)
        return redirect(url_for('index'))

    return render_template('add.html')

# -----------------------
# UPDATE
# -----------------------
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    item = collection.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        collection.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "kode": request.form['kode'],
                    "nama": request.form['nama'],
                    "harga": int(request.form['harga']),
                    "jumlah": int(request.form['jumlah'])
                }
            }
        )
        return redirect(url_for('index'))

    return render_template("edit.html", item=item)

# -----------------------
# DELETE
# -----------------------
@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
