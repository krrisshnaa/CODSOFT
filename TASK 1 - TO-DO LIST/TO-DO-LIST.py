import tkinter as tk
from tkinter import messagebox, simpledialog
import os

TASK_FILE = "tasks.txt"

def load_tasks():
    tasks = []
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            for line in file:
                parts = line.strip().split("||")
                if len(parts) == 2:
                    task_text = parts[0]
                    done_status = parts[1] == "True"
                    tasks.append({"task": task_text, "done": done_status})
    return tasks

def save_tasks():
    with open(TASK_FILE, "w") as file:
        for task in tasks:
            file.write(f"{task['task']}||{task['done']}\n")

def refresh_task_list():
    for widget in task_frame.winfo_children():
        widget.destroy()

    for i, task in enumerate(tasks):
        task_text = task["task"]
        done = task["done"]

        row = tk.Frame(task_frame, bg="#FFF8DC", pady=3)
        row.pack(fill="x", padx=5, pady=2)

        task_label = tk.Label(
            row,
            text=task_text,
            font=("Segoe UI", 11, "overstrike" if done else "normal"),
            bg="#FFF8DC",
            fg="gray" if done else "black",
            anchor="w",
            width=30
        )
        task_label.pack(side="left", padx=10)

        done_btn = tk.Button(
            row,
            text="✔️" if not done else "↩️",
            command=lambda i=i: toggle_done(i),
            bg="#90EE90", fg="black", width=3
        )
        done_btn.pack(side="left", padx=5)

        edit_btn = tk.Button(
            row,
            text="✏️",
            command=lambda i=i: update_task(i),
            bg="#FFD700", fg="black", width=3
        )
        edit_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(
            row,
            text="🗑️",
            command=lambda i=i: delete_task(i),
            bg="#FF6B6B", fg="white", width=3
        )
        delete_btn.pack(side="right", padx=5)

def add_task():
    task_text = task_entry.get().strip()
    if task_text:
        tasks.append({"task": task_text, "done": False})
        task_entry.delete(0, tk.END)
        refresh_task_list()
        save_tasks()
    else:
        messagebox.showwarning("Empty Task", "Please enter a task!")

def toggle_done(index):
    tasks[index]["done"] = not tasks[index]["done"]
    refresh_task_list()
    save_tasks()

def delete_task(index):
    confirm = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
    if confirm:
        del tasks[index]
        refresh_task_list()
        save_tasks()

def update_task(index):
    current = tasks[index]["task"]
    new_task = simpledialog.askstring("Edit Task", "Update the task:", initialvalue=current)
    if new_task and new_task.strip():
        tasks[index]["task"] = new_task.strip()
        refresh_task_list()
        save_tasks()
    elif new_task == "":
        messagebox.showwarning("Invalid Input", "Task cannot be empty.")

window = tk.Tk()
window.title("TO-DO LIST")
window.geometry("550x600")
window.configure(bg="#FAF0E6")

title_label = tk.Label(window, text="My To-Do List", font=("Segoe UI", 20, "bold"), bg="#FAF0E6", fg="#4B0082")
title_label.pack(pady=15)

entry_frame = tk.Frame(window, bg="#FAF0E6")
entry_frame.pack(pady=10)

task_entry = tk.Entry(entry_frame, font=("Segoe UI", 12), width=35)
task_entry.pack(side="left", padx=10)

add_btn = tk.Button(entry_frame, text="Add Task ➕", font=("Segoe UI", 10, "bold"), bg="#90EE90", command=add_task)
add_btn.pack(side="left")

task_container = tk.Frame(window)
task_container.pack(fill="both", expand=True, padx=20, pady=10)

canvas = tk.Canvas(task_container, bg="#FFF8DC", highlightthickness=0)
scrollbar = tk.Scrollbar(task_container, orient="vertical", command=canvas.yview)
task_frame = tk.Frame(canvas, bg="#FFF8DC")

task_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=task_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

tasks = load_tasks()
refresh_task_list()

window.mainloop()
