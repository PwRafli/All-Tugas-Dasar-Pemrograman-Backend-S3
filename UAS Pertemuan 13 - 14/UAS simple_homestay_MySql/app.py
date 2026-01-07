from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os, math
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# koneksi database
def db():
    conn = sqlite3.connect("stokumkm.db")
    conn.row_factory = sqlite3.Row
    return conn

# init database
def init_db():
    conn = db()
    conn.execute("DROP TABLE IF EXISTS barang")
    conn.execute("""
        CREATE TABLE barang(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo TEXT,
            code_room TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            room_size TEXT,
            price REAL NOT NULL,
            guests INTEGER NOT NULL,
            available INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ================= READ + SEARCH + PAGINATION =================
@app.route("/")
def index():
    search = request.args.get("search", "")
    page = int(request.args.get("page", 1))
    per_page = 5
    offset = (page - 1) * per_page

    conn = db()

    total = conn.execute("""
        SELECT COUNT(*) FROM barang
        WHERE name LIKE ? OR code_room LIKE ?
    """, (f"%{search}%", f"%{search}%")).fetchone()[0]

    rows = conn.execute("""
        SELECT * FROM barang
        WHERE name LIKE ? OR code_room LIKE ?
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (f"%{search}%", f"%{search}%", per_page, offset)).fetchall()

    conn.close()

    total_pages = math.ceil(total / per_page)

    return render_template(
        "index.html",
        stoks=rows,
        page=page,
        total_pages=total_pages,
        search=search
    )

# ================= CREATE =================
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        file = request.files["photo"]
        if file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            filename = "noimage.png"

        conn = db()
        conn.execute("""
            INSERT INTO barang
            (photo, code_room, name, description, room_size, price, guests, available)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            filename,
            request.form["code_room"],
            request.form["name"],
            request.form["description"],
            request.form["room_size"],
            request.form["price"],
            request.form["guests"],
            request.form["available"]
        ))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add.html")

# ================= UPDATE =================
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

        conn.execute("""
            UPDATE barang SET
            photo=?, code_room=?, name=?, description=?, room_size=?,
            price=?, guests=?, available=?
            WHERE id=?
        """, (
            filename,
            request.form["code_room"],
            request.form["name"],
            request.form["description"],
            request.form["room_size"],
            request.form["price"],
            request.form["guests"],
            request.form["available"],
            id
        ))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    conn.close()
    return render_template("edit.html", stoks=stok)

# ================= DELETE =================
@app.route("/delete/<int:id>")
def delete(id):
    conn = db()
    conn.execute("DELETE FROM barang WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
