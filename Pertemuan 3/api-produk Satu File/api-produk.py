import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Routing berdasarkan path
        if self.path == "/":
            response = {"message": "Selamat Datang Di Produk UMKM"}
        elif self.path == "/produk/snack":
            response = {"message": "Halaman Produk Semua Snack.."}
        elif self.path == "/produk/drink":
            response = {"message": "Halaman Produk Semua Soft Drink.."}
        elif self.path.startswith("/produk/snack/"):
            # Ambil id setelah /produk/snack/
            snack_id = self.path.split("/")[-1]
            response = {"message": f"Halaman Produk Snack dengan id = {snack_id}"}
        elif self.path.startswith("/produk/drink/"):
            # Ambil id setelah /produk/drink/
            drink_id = self.path.split("/")[-1]
            response = {"message": f"Halaman Produk Soft Drink dengan id = {drink_id}"}
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())
            return

        # Kirim response JSON
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
