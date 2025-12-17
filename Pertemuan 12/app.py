from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import math

app = Flask(__name__)

# ===============================
# CONFIG UPLOAD
# ===============================
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ===============================
# MONGODB CONNECTION
# ===============================
client = MongoClient("mongodb://localhost:27017/")
db = client["UASHomeStay"]
collection = db["UASrooms"]

# ===============================
# READ (INDEX + SEARCH + PAGINATION)
# ===============================
@app.route('/')
def index():
    # ambil parameter
    search = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))

    query = {}
    if search:
        query = {
            "$or": [
                {"name": {"$regex": search, "$options": "i"}},
                {"code": {"$regex": search, "$options": "i"}}
            ]
        }

    total_data = collection.count_documents(query)
    total_pages = math.ceil(total_data / limit)
    skip = (page - 1) * limit

    data = list(
        collection.find(query)
        .skip(skip)
        .limit(limit)
    )

    return render_template(
        'index.html',
        data=data,
        page=page,
        total_pages=total_pages,
        search=search,
        limit=limit
    )

# ===============================
# CREATE
# ===============================
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "code": request.form['code'],
            "room_size": request.form['room_size'],
            "price": int(request.form['price']),
            "description": request.form['description'],
            "guests": int(request.form['guests']),
            "available": True if request.form.get('available') else False
        }

        file = request.files.get('photo')
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data["photo"] = filename

        collection.insert_one(data)
        return redirect(url_for('index'))

    return render_template('form.html', item=None)

# ===============================
# UPDATE
# ===============================
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    item = collection.find_one({"_id": ObjectId(id)})

    if request.method == 'POST':
        update_data = {
            "name": request.form['name'],
            "code": request.form['code'],
            "room_size": request.form['room_size'],
            "price": int(request.form['price']),
            "description": request.form['description'],
            "guests": int(request.form['guests']),
            "available": True if request.form.get('available') else False
        }

        file = request.files.get('photo')
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            update_data["photo"] = filename

        collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        return redirect(url_for('index'))

    return render_template('form.html', item=item)

# ===============================
# DELETE
# ===============================
@app.route('/delete/<id>')
def delete(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

# ===============================
# RUN APP
# ===============================
if __name__ == '__main__':
    app.run(debug=True)
