import tkinter as tk
import random
import string
from tkinter import messagebox

def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError

        # Use limited special characters
        allowed_symbols = "!@#$%"

        # Combine character sets
        characters = string.ascii_letters + string.digits + allowed_symbols

        password = ''.join(random.choice(characters) for _ in range(length))
        password_var.set(password)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive number.")

def copy_password():
    generated = password_var.get()
    if generated:
        root.clipboard_clear()
        root.clipboard_append(generated)
        messagebox.showinfo("Copied", "Password copied to clipboard.")

# --- UI Setup ---
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x250")
root.resizable(False, False)
root.config(bg="#f2f2f2")

# Title
title_label = tk.Label(root, text="Password Generator", font=("Helvetica", 16, "bold"), bg="#f2f2f2")
title_label.pack(pady=10)

# Length input
length_frame = tk.Frame(root, bg="#f2f2f2")
length_frame.pack(pady=5)
length_label = tk.Label(length_frame, text="Password Length:", font=("Helvetica", 12), bg="#f2f2f2")
length_label.pack(side=tk.LEFT, padx=5)
length_entry = tk.Entry(length_frame, width=10)
length_entry.pack(side=tk.LEFT)

# Generate button
generate_btn = tk.Button(root, text="Generate Password", font=("Helvetica", 12), command=generate_password)
generate_btn.pack(pady=10)

# Show password
password_var = tk.StringVar()
password_entry = tk.Entry(root, textvariable=password_var, font=("Helvetica", 12), width=30, justify='center', bd=2)
password_entry.pack(pady=10)

# Copy button
copy_btn = tk.Button(root, text="Copy", font=("Helvetica", 12), command=copy_password)
copy_btn.pack(pady=5)

# Run the app
root.mainloop()
