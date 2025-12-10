from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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
        name = request.form["name"]
        price = request.form["price"]
        guests = request.form["guests"]
        available = request.form["available"]

        conn = db()
        conn.execute("INSERT INTO barang (name, price, guests, available) VALUES (?, ?, ?, ?)",
                     (name, price, guests, available))
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
        name = request.form["name"]
        price = request.form["price"]
        guests = request.form["guests"]
        available = request.form["available"]

        conn.execute("""
            UPDATE barang 
            SET name=?, price=?, guests=?, available=? 
            WHERE id=?
        """, (name, price, guests, available, id))
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


app.run(debug=True)
if __name__ == "__main__":
    app.run(debug=True)
