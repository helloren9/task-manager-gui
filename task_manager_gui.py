import tkinter as tk
from tkinter import messagebox
import datetime
import csv
import os

TASKS_FILE = "tasks.csv"

class Task:
    def __init__(self, task_id, description, completed=False, priority="medium", due_date=None):
        self.id = task_id
        self.description = description
        self.completed = completed
        self.priority = priority
        self.due_date = due_date

def load_tasks():
    tasks = []

    if not os.path.exists(TASKS_FILE):
        return tasks
    
    with open(TASKS_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 3:
                continue

            task_id = int(row[0])
            description = row[1]
            completed = row[2] == "True"
            priority = row[3]
            due_date = row[4] if len(row) > 4 and row[4] != "None" else None 
            
            tasks.append(Task(task_id, description, completed, priority, due_date))

    return tasks

def save_tasks(tasks):
    with open(TASKS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        for task in tasks:
            writer.writerow([task.id, task.description, task.completed, task.priority, task.due_date])

def is_overdue(task):
    if not task.due_date or task.completed:
        return False
    
    due_date = datetime.datetime.strptime(task.due_date, "%Y-%m-%d").date()
    today = datetime.date.today()

    return due_date < today

def refresh_tasks():
    task_listbox.delete(0, tk.END)

    for task in tasks:
        status = "✅" if task.completed else "⏳"
        due = task.due_date if task.due_date else "No due date"

        overdue = ""
        if is_overdue(task):
            overdue = " ⚠️ OVERDUE"

        task_listbox.insert(
            tk.END,
            f"{task.id}. {task.description} | {task.priority.upper()} | Due: {due} | {status}{overdue}"
        )

def add_task_gui():
    desc = entry_desc.get()
    priority = priority_var.get()
    due = entry_due.get()

    if not desc:
        messagebox.showerror("Error", "Task description required")
        return
    
    if due and due != "YYYY-MM-DD (optional)":
        try:
            datetime.datetime.strptime(due, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format")
            return
    else:
        due = None

    task_id = len(tasks) + 1
    tasks.append(Task(task_id, desc, False, priority, due))
    save_tasks(tasks)
    refresh_tasks()

    entry_desc.delete(0, tk.END)
    entry_due.delete(0, tk.END)
    entry_due.insert(0, "YYYY-MM-DD (optional)")

def get_selected_task():
    selection = task_listbox.curselection()
    if not selection:
        return None
    index = selection[0]
    return tasks[index]

def complete_task_gui():
    task = get_selected_task()
    if task:
        task.completed = True
        save_tasks(tasks)
        refresh_tasks()

def delete_task_gui():
    task = get_selected_task()
    if task:
        tasks.remove(task)
        for i, t in enumerate(tasks):
            t.id = i + 1
        save_tasks(tasks)
        refresh_tasks()

root = tk.Tk()
root.title("Task Manager")
root.geometry("600x400")

tasks = load_tasks()

task_listbox = tk.Listbox(root, width=80)
task_listbox.pack(pady=10)

entry_desc = tk.Entry(root, width=40)
entry_desc.pack()

priority_var = tk.StringVar(value="medium")
priority_menu = tk.OptionMenu(root, priority_var, "low", "medium", "high")
priority_menu.pack()

entry_due = tk.Entry(root)
entry_due.insert(0, "YYYY-MM-DD (optional)")
entry_due.pack()

tk.Button(root, text="Add Task", command=add_task_gui).pack(pady=5)

tk.Button(root, text="Complete Task", command=complete_task_gui).pack()
tk.Button(root, text="Delete Task", command=delete_task_gui).pack()

refresh_tasks()

root.mainloop()

