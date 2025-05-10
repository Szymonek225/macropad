import tkinter as tk
from tkinter import messagebox, filedialog
import json

shortcuts = ["" for _ in range(9)]

try:
    with open("shortcut_config.json", "r") as f:
        shortcuts = json.load(f)
except:
    pass

def save():
    for i in range(9):
        shortcuts[i] = entries[i].get()
    with open("shortcut_config.json", "w") as f:
        json.dump(shortcuts, f)
    messagebox.showinfo("Zapisano", "Skróty zostały zapisane.")

root = tk.Tk()
root.title("Shortcut Manager")

entries = []

for i in range(9):
    tk.Label(root, text=f"Przycisk {i+1}:").grid(row=i, column=0, padx=10, pady=5)
    e = tk.Entry(root, width=40)
    e.grid(row=i, column=1, padx=10, pady=5)
    e.insert(0, shortcuts[i])
    entries.append(e)

def open_help():
    msg = (
        "Wprowadź skróty w formacie:\n"
        "  ctrl+c, ctrl+shift+z, volume up\n"
        "  open:https://example.com (otwiera stronę)\n"
    )
    messagebox.showinfo("Pomoc", msg)

tk.Button(root, text="Zapisz", command=save).grid(row=10, column=0, columnspan=2, pady=10)
tk.Button(root, text="Pomoc", command=open_help).grid(row=11, column=0, columnspan=2, pady=5)

root.mainloop()
