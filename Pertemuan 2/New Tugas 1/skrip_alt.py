# skrip_alt.py

# hanya mengambil fungsi tertentu dari modul
from modul_sapa import sapa, salam_pagi

# bisa langsung dipanggil tanpa prefix modul
sapa("STIKOM")
salam_pagi("Mahasiswa")

# kalau coba panggil salam_malam() -> ERROR,
# karena tidak di-import
