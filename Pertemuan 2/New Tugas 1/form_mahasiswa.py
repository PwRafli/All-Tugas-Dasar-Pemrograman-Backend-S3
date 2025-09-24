import tkinter as tk
from tkinter import messagebox

# fungsi ketika tombol kirim ditekan
def submit():
    data = {
        "Nama": entry_nama.get(),
        "Kelas": entry_kelas.get(),
        "NIM": entry_nim.get(),
        "Alamat": entry_alamat.get(),
        "Umur": entry_umur.get(),
        "Tanggal Lahir": entry_tanggal.get(),
        "Status": status_var.get(),
        "Hobi": [h for h, var in hobi_vars.items() if var.get() == 1],
        "Keahlian": [k for k, var in keahlian_vars.items() if var.get() == 1]
    }
    messagebox.showinfo("Data Terkirim", f"Data berhasil dikirim:\n\n{data}")

# fungsi reset
def reset():
    entry_nama.delete(0, tk.END)
    entry_kelas.delete(0, tk.END)
    entry_nim.delete(0, tk.END)
    entry_alamat.delete(0, tk.END)
    entry_umur.delete(0, tk.END)
    entry_tanggal.delete(0, tk.END)
    status_var.set("Belum Menikah")
    for var in hobi_vars.values():
        var.set(0)
    for var in keahlian_vars.values():
        var.set(0)

root = tk.Tk()
root.title("Form Data Mahasiswa")

# Label dan entry
tk.Label(root, text="Nama:").grid(row=0, column=0, sticky="w")
entry_nama = tk.Entry(root, width=30)
entry_nama.grid(row=0, column=1)

tk.Label(root, text="Kelas:").grid(row=1, column=0, sticky="w")
entry_kelas = tk.Entry(root, width=30)
entry_kelas.grid(row=1, column=1)

tk.Label(root, text="NIM:").grid(row=2, column=0, sticky="w")
entry_nim = tk.Entry(root, width=30)
entry_nim.grid(row=2, column=1)

tk.Label(root, text="Alamat:").grid(row=3, column=0, sticky="w")
entry_alamat = tk.Entry(root, width=30)
entry_alamat.grid(row=3, column=1)

tk.Label(root, text="Umur:").grid(row=4, column=0, sticky="w")
entry_umur = tk.Entry(root, width=30)
entry_umur.grid(row=4, column=1)

tk.Label(root, text="Tanggal Lahir:").grid(row=5, column=0, sticky="w")
entry_tanggal = tk.Entry(root, width=30)
entry_tanggal.grid(row=5, column=1)

# Status menikah
tk.Label(root, text="Status:").grid(row=6, column=0, sticky="w")
status_var = tk.StringVar(value="Belum Menikah")
tk.Radiobutton(root, text="Menikah", variable=status_var, value="Menikah").grid(row=6, column=1, sticky="w")
tk.Radiobutton(root, text="Belum Menikah", variable=status_var, value="Belum Menikah").grid(row=6, column=2, sticky="w")

# Hobi (checkbox)
tk.Label(root, text="Hobi:").grid(row=7, column=0, sticky="nw")
hobi_list = ["Membaca", "Olahraga", "Musik", "Gaming", "Traveling"]
hobi_vars = {}
for i, h in enumerate(hobi_list):
    var = tk.IntVar()
    tk.Checkbutton(root, text=h, variable=var).grid(row=7+i, column=1, sticky="w")
    hobi_vars[h] = var

# Keahlian (checkbox)
tk.Label(root, text="Keahlian:").grid(row=7, column=2, sticky="nw")
keahlian_list = ["Programming", "Design", "Public Speaking", "Menulis", "Fotografi"]
keahlian_vars = {}
for i, k in enumerate(keahlian_list):
    var = tk.IntVar()
    tk.Checkbutton(root, text=k, variable=var).grid(row=7+i, column=3, sticky="w")
    keahlian_vars[k] = var

# Tombol
tk.Button(root, text="Login", command=submit, bg="lightgreen").grid(row=20, column=1, pady=10)
tk.Button(root, text="Reset", command=reset, bg="tomato").grid(row=20, column=2, pady=10)

root.mainloop()
