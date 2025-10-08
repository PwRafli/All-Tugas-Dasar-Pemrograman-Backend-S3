from flask import Flask, render_template, request

app = Flask(__name__)

# -------------------------------
# Routing Dasar
# -------------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Routing dengan method GET & POST
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        return f"<h3>Halo {nama}, kami sudah menerima email kamu ({email})!</h3>"
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)