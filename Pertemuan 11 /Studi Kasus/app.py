from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# lokasi upload
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# koneksi database
def db():
    conn = sqlite3.connect("stokumkm.db")
    conn.row_factory = sqlite3.Row
    return conn

# inisialisasi tabel
def init_db():
    conn = db()

    conn.execute("DROP TABLE IF EXISTS barang")

    conn.execute("""
        CREATE TABLE barang(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo TEXT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            guests INTEGER NOT NULL,
            available INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# READ
@app.route("/")
def index():
    conn = db()
    rows = conn.execute("SELECT * FROM barang").fetchall()
    conn.close()
    return render_template("index.html", stoks=rows)

# CREATE
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        file = request.files["photo"]
        if file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            filename = "noimage.png"

        name = request.form["name"]
        price = request.form["price"]
        guests = request.form["guests"]
        available = request.form["available"]

        conn = db()
        conn.execute("""
            INSERT INTO barang (photo, name, price, guests, available)
            VALUES (?, ?, ?, ?, ?)
        """, (filename, name, price, guests, available))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add.html")

# UPDATE
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = db()
    stok = conn.execute("SELECT * FROM barang WHERE id=?", (id,)).fetchone()

    if request.method == "POST":

        file = request.files["photo"]
        if file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            filename = stok["photo"]

        name = request.form["name"]
        price = request.form["price"]
        guests = request.form["guests"]
        available = request.form["available"]

        conn.execute("""
            UPDATE barang
            SET photo=?, name=?, price=?, guests=?, available=?
            WHERE id=?
        """, (filename, name, price, guests, available, id))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    conn.close()
    return render_template("edit.html", stoks=stok)

# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    conn = db()
    conn.execute("DELETE FROM barang WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
