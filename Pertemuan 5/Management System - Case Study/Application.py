from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Home page - Display all products
@app.route('/')
def index():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products ORDER BY code')
    products = cursor.fetchall()
    conn.close()
    return render_template('list-index.html', products=products)

# Add new product page
@app.route('/add')
def add_product():
    return render_template('list-add.html')

# Process add product form
@app.route('/add', methods=['POST'])
def add_product_post():
    code = request.form['code']
    name = request.form['name']
    price = request.form['price']
    
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (code, name, price) VALUES (?, ?, ?)', 
                  (code, name, price))
    conn.commit()
    conn.close()
    
    return redirect(url_for('list-index.html'))

# Edit product page
@app.route('/edit/<string:code>')
def edit_product(code):
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE code = ?', (code,))
    product = cursor.fetchone()
    conn.close()
    
    if product:
        return render_template('list-edit.html', product=product)
    return redirect(url_for('list-index.html'))

# Process edit product form
@app.route('/edit/<string:code>', methods=['POST'])
def edit_product_post(code):
    name = request.form['name']
    price = request.form['price']
    
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE products SET name = ?, price = ? WHERE code = ?', 
                  (name, price, code))
    conn.commit()
    conn.close()
    
    return redirect(url_for('list-index.html'))

# Delete product
@app.route('/delete/<string:code>')
def delete_product(code):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE code = ?', (code,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('list-index.html'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)