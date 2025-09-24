# hasil_modul.py
import matematika

def main():
    while True:
        print("\n=== Program Kalkulator Modul ===")
        try:
            a = float(input("Masukkan angka pertama : "))
            b = float(input("Masukkan angka kedua   : "))
        except ValueError:
            print("Input harus berupa angka! Coba lagi.")
            continue

        # hasil perhitungan
        print("\n=== Hasil Perhitungan ===")
        print(f"Penambahan dari {a} dan {b} adalah {matematika.tambah(a, b)}")
        print(f"Pengurangan dari {a} dan {b} adalah {matematika.kurang(a, b)}")
        print(f"Perkalian  dari {a} dan {b} adalah {matematika.kali(a, b)}")
        print(f"Pembagian  dari {a} dan {b} adalah {matematika.bagi(a, b)}")

        # pilihan lanjut atau keluar
        pilih = input("\nApakah mau menghitung lagi? (y/n): ").lower()
        if pilih != "y":
            print("Terima kasih, program selesai.")
            break

if __name__ == "__main__":
    main()
