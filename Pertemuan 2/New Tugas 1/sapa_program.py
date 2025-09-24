# sapa_program.py

def sapa(nama):
    """Menyapa dengan nama."""
    print("Halo", nama, "!")

def salam_pagi(nama):
    """Menyapa dengan ucapan selamat pagi."""
    print("Selamat pagi,", nama, "! Semoga harimu menyenangkan.")

def salam_malam(nama):
    """Menyapa dengan ucapan selamat malam."""
    print("Selamat malam,", nama, "! Jangan lupa istirahat ya.")

# ====== Bagian pemanggilan utama ======
if __name__ == "__main__":
    sapa("STIKOM")
    salam_pagi("Mahasiswa")
    salam_malam("Dosen")

    print("\nProgram selesai, tekan Enter untuk keluar...")
    input()   # tunggu user tekan Enter sebelum exit