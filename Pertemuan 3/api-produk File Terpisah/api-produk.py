import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# Fungsi untuk membaca data dari file JSON
def load_data():
    with open('contoh json external/data.json', "r") as f:
        return json.load(f)

# Fungsi untuk mendapatkan semua produk snack
def get_all_snacks():
    data = load_data("snacks.json")
    return data.get("snacks", [])

# Fungsi untuk mendapatkan semua produk drink
def get_all_drinks():
    data = load_data("drinks.json")
    return data.get("drinks", [])

# Fungsi untuk mendapatkan produk snack berdasarkan id
def get_snack_by_id(snack_id):
    snacks = get_all_snacks()
    for snack in snacks:
        if snack["id"] == snack_id:
            return snack
    return None

# Fungsi untuk mendapatkan produk drink berdasarkan id
def get_drink_by_id(drink_id):
    drinks = get_all_drinks()
    for drink in drinks:
        if drink["id"] == drink_id:
            return drink
    return None

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            response = {"message": "Selamat Datang Di Produk UMKM"}
        elif self.path == "/produk/snack":
            snacks = get_all_snacks()
            response = {"snacks": snacks}
        elif self.path == "/produk/drink":
            drinks = get_all_drinks()
            response = {"drinks": drinks}
        elif self.path.startswith("/produk/snack/"):
            snack_id = self.path.split("/")[-1]
            snack = get_snack_by_id(snack_id)
            if snack:
                response = {"snack": snack}
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Snack not found"}).encode())
                return
        elif self.path.startswith("/produk/drink/"):
            drink_id = self.path.split("/")[-1]
            drink = get_drink_by_id(drink_id)
            if drink:
                response = {"drink": drink}
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Drink not found"}).encode())
                return
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())
            return

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    port = 8000
    server_address = ("", port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f"Server berjalan di http://localhost:{port}")
    httpd.serve_forever()