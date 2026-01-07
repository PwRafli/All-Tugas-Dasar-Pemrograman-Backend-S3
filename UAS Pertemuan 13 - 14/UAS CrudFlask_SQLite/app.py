from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_mysqldb import MySQL
import math
import os
import re
import time

app = Flask(__name__)

# =====================================================
# BASE DIRECTORY (PENTING UNTUK PATH ABSOLUTE)
# =====================================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# =====================================================
# MySQL CONFIG
# =====================================================
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'  # ganti sesuai password MySQL kamu
app.config['MYSQL_DB'] = 'datahotel_db'

mysql = MySQL(app)

# =====================================================
# UPLOAD CONFIG (FOLDER DI LUAR static)
# =====================================================
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# =====================================================
# HELPER FUNCTIONS
# =====================================================
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def make_safe_filename(filename):
    name, ext = os.path.splitext(filename)
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    timestamp = str(int(time.time()))
    return f"{safe_name}_{timestamp}{ext}"


# =====================================================
# ROUTE: SERVE UPLOADED IMAGE
# =====================================================
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# =====================================================
# READ: LIST + SEARCH + PAGINATION
# =====================================================
@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    cur = mysql.connection.cursor()

    # total data
    if search_query:
        cur.execute(
            "SELECT COUNT(*) FROM hotels WHERE name LIKE %s",
            ('%' + search_query + '%',)
        )
    else:
        cur.execute("SELECT COUNT(*) FROM hotels")

    total_rows = cur.fetchone()[0]
    total_pages = math.ceil(total_rows / per_page)

    # fetch data
    if search_query:
        cur.execute("""
            SELECT * FROM hotels
            WHERE name LIKE %s
            ORDER BY id DESC
            LIMIT %s OFFSET %s
        """, ('%' + search_query + '%', per_page, offset))
    else:
        cur.execute("""
            SELECT * FROM hotels
            ORDER BY id DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))

    hotels = cur.fetchall()
    cur.close()

    return render_template(
        'index.html',
        hotels=hotels,
        page=page,
        total_pages=total_pages,
        search_query=search_query
    )


# =====================================================
# CREATE: FORM
# =====================================================
@app.route('/add', methods=['GET'])
def add_homestay_form():
    return render_template('add.html')


# =====================================================
# CREATE: PROCESS
# =====================================================
@app.route('/add', methods=['POST'])
def add_homestay():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    guests = request.form['guests']
    amenities = request.form['amenities']
    available = True if request.form.get('available') else False

    filename = None

    if 'photo' in request.files:
        photo = request.files['photo']
        if photo and photo.filename != '' and allowed_file(photo.filename):
            filename = make_safe_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO hotels
        (name, description, price, guests, amenities, available, filename)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (name, description, price, guests, amenities, available, filename))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))


# =====================================================
# UPDATE: FORM
# =====================================================
@app.route('/edit/<int:id>', methods=['GET'])
def edit_homestay_form(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hotels WHERE id = %s", (id,))
    hotel = cur.fetchone()
    cur.close()
    return render_template('edit.html', hotel=hotel)


# =====================================================
# UPDATE: PROCESS
# =====================================================
@app.route('/edit/<int:id>', methods=['POST'])
def edit_homestay(id):
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    guests = request.form['guests']
    amenities = request.form['amenities']
    available = True if request.form.get('available') else False

    new_filename = None

    if 'photo' in request.files:
        photo = request.files['photo']
        if photo and photo.filename != '' and allowed_file(photo.filename):
            new_filename = make_safe_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

    cur = mysql.connection.cursor()

    if new_filename:
        cur.execute("""
            UPDATE hotels
            SET name=%s, description=%s, price=%s, guests=%s,
                amenities=%s, available=%s, filename=%s
            WHERE id=%s
        """, (name, description, price, guests,
              amenities, available, new_filename, id))
    else:
        cur.execute("""
            UPDATE hotels
            SET name=%s, description=%s, price=%s, guests=%s,
                amenities=%s, available=%s
            WHERE id=%s
        """, (name, description, price, guests,
              amenities, available, id))

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))


# =====================================================
# DELETE
# =====================================================
@app.route('/delete/<int:id>')
def delete_homestay(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT filename FROM hotels WHERE id=%s", (id,))
    data = cur.fetchone()

    if data and data[0]:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], data[0])
        if os.path.exists(file_path):
            os.remove(file_path)

    cur.execute("DELETE FROM hotels WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))


# =====================================================
# APP RUN
# =====================================================
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)



if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)