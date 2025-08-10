import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

conn = sqlite3.connect("contacts.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS contacts (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             phone TEXT NOT NULL,
             email TEXT,
             address TEXT)""")
conn.commit()

def fetch_contacts():
    for row in tree.get_children():
        tree.delete(row)
    c.execute("SELECT * FROM contacts")
    for contact in c.fetchall():
        tree.insert("", tk.END, values=contact)

def add_contact():
    name = name_var.get().strip()
    phone = phone_var.get().strip()
    email = email_var.get().strip()
    address = address_var.get().strip()

    if not name or not phone:
        messagebox.showwarning("Input Error", "Name and Phone are required!")
        return

    c.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
              (name, phone, email, address))
    conn.commit()
    clear_inputs()
    fetch_contacts()
    messagebox.showinfo("Success", "Contact added successfully!")

def search_contact():
    query = search_var.get().strip()
    for row in tree.get_children():
        tree.delete(row)

    c.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?",
              (f"%{query}%", f"%{query}%"))
    for contact in c.fetchall():
        tree.insert("", tk.END, values=contact)

def update_contact():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Contact", "Please select a contact to update.")
        return

    values = tree.item(selected, "values")
    contact_id = values[0]

    c.execute("""UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?""",
              (name_var.get(), phone_var.get(), email_var.get(), address_var.get(), contact_id))
    conn.commit()
    clear_inputs()
    fetch_contacts()
    messagebox.showinfo("Updated", "Contact updated successfully!")

def delete_contact():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Contact", "Please select a contact to delete.")
        return

    values = tree.item(selected, "values")
    contact_id = values[0]

    if messagebox.askyesno("Confirm Delete", f"Delete contact '{values[1]}'?"):
        c.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        conn.commit()
        fetch_contacts()

def load_selected_contact(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    name_var.set(values[1])
    phone_var.set(values[2])
    email_var.set(values[3])
    address_var.set(values[4])

def clear_inputs():
    name_var.set("")
    phone_var.set("")
    email_var.set("")
    address_var.set("")

root = tk.Tk()
root.title("📇 Contact Manager")
root.geometry("800x500")
root.config(bg="#f8f9fa")

style = ttk.Style()
style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
style.configure("Treeview", font=("Helvetica", 10), rowheight=25)

name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
address_var = tk.StringVar()
search_var = tk.StringVar()


tk.Label(root, text="Search:", bg="#f8f9fa", font=("Helvetica", 11)).pack(pady=5)
tk.Entry(root, textvariable=search_var, font=("Helvetica", 10), width=30).pack()
tk.Button(root, text="🔍 Search", command=search_contact, bg="#007bff", fg="white").pack(pady=5)


form_frame = tk.Frame(root, bg="#f8f9fa")
form_frame.pack(pady=10)

tk.Label(form_frame, text="Name:", bg="#f8f9fa").grid(row=0, column=0, sticky="w")
tk.Entry(form_frame, textvariable=name_var, width=25).grid(row=0, column=1)

tk.Label(form_frame, text="Phone:", bg="#f8f9fa").grid(row=1, column=0, sticky="w")
tk.Entry(form_frame, textvariable=phone_var, width=25).grid(row=1, column=1)

tk.Label(form_frame, text="Email:", bg="#f8f9fa").grid(row=0, column=2, sticky="w")
tk.Entry(form_frame, textvariable=email_var, width=25).grid(row=0, column=3)

tk.Label(form_frame, text="Address:", bg="#f8f9fa").grid(row=1, column=2, sticky="w")
tk.Entry(form_frame, textvariable=address_var, width=25).grid(row=1, column=3)


btn_frame = tk.Frame(root, bg="#f8f9fa")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="➕ Add", command=add_contact, bg="#28a745", fg="white", width=10).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="✏ Update", command=update_contact, bg="#ffc107", fg="black", width=10).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="❌ Delete", command=delete_contact, bg="#dc3545", fg="white", width=10).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="🔄 Refresh", command=fetch_contacts, bg="#17a2b8", fg="white", width=10).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="🧹 Clear", command=clear_inputs, bg="#6c757d", fg="white", width=10).grid(row=0, column=4, padx=5)


tree = ttk.Treeview(root, columns=("ID", "Name", "Phone", "Email", "Address"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
tree.heading("Address", text="Address")
tree.pack(fill=tk.BOTH, expand=True, pady=10)
tree.bind("<ButtonRelease-1>", load_selected_contact)

fetch_contacts()
root.mainloop()
