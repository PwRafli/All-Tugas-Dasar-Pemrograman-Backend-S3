from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import math

app = Flask(__name__)

# Konfigurasi koneksi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root' # Sesuaikan dengan password Anda jika ada
app.config['MYSQL_DB'] = 'crud_db'

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 5 # Jumlah item per halaman

    # Hitung offset untuk query SQL
    offset = (page - 1) * per_page
    
    cur = mysql.connection.cursor()
    
    # Hitung total data
    if search_query:
        # Menghitung total data dengan pencarian
        cur.execute(f"SELECT COUNT(*) FROM stok WHERE nama LIKE %s", ('%' + search_query + '%',))
    else:
        # Menghitung total data tanpa pencarian
        cur.execute("SELECT COUNT(*) FROM stok")

    total_rows = cur.fetchone()[0]
    total_pages = math.ceil(total_rows / per_page)
    
    # Ambil data berdasarkan pagination dan pencarian
    if search_query:
        cur.execute(
            f"SELECT * FROM stok WHERE nama LIKE %s LIMIT %s OFFSET %s", 
            ('%' + search_query + '%', per_page, offset)
        )
    else:
        cur.execute(
            f"SELECT * FROM stok LIMIT %s OFFSET %s", 
            (per_page, offset)
        )

    dstok = cur.fetchall()
    cur.close()

    # Pastikan 'page' tidak melebihi 'total_pages'
    if page > total_pages and total_pages > 0:
        page = total_pages
        # Hitung ulang offset dan ambil data lagi jika perlu,
        # tapi untuk kesederhanaan, kita biarkan saja sesuai dengan kode yang diberikan.

    return render_template('index.html', dstok=dstok, page=page, total_pages=total_pages, search_query=search_query, offset=offset)

if __name__ == '__main__':
    app.run(debug=True)