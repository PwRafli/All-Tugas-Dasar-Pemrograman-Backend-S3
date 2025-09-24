# hasil_modul.py

# import modul-modul
import penambahan
import pengurangan
import perkalian
import pembagian

# input dari user
a = float(input("Masukkan angka pertama : "))
b = float(input("Masukkan angka kedua   : "))

# proses perhitungan
hasil_tambah = penambahan.tambah(a, b)
hasil_kurang = pengurangan.kurang(a, b)
hasil_kali   = perkalian.kali(a, b)
hasil_bagi   = pembagian.bagi(a, b)

# tampilkan hasil
print("\n=== Hasil Perhitungan ===")
print(f"Penambahan dari {a} dan {b} adalah {hasil_tambah}")
print(f"Pengurangan dari {a} dan {b} adalah {hasil_kurang}")
print(f"Perkalian dari {a} dan {b} adalah {hasil_kali}")
print(f"Pembagian dari {a} dan {b} adalah {hasil_bagi}")

# contoh penggunaan modul