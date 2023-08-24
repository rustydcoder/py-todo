import tkinter as tk
import json
from tkinter import messagebox

MEMORY_PATH = "data.json"
unique_id = 0


# ---------------------------- ESSENTIALS ------------------------------- #
def set_unique_id(keys):
    global unique_id

    if len(keys) > 0:
        int_keys = [int(key) for key in keys]
        int_keys.sort()
        unique_id = int_keys[-1]


def display_listbox(item):
    if isinstance(item, str):
        todo_listbox.insert(0, item)
    else:
        for i in item:
            todo_listbox.insert(0, i)


def load_listbox():
    global unique_id
    data = load_from_db()

    set_unique_id(list(data))

    if len(data) > 0:
        display_listbox(data.values())


def validate_entry(entry):
    data = load_from_db()

    if len(entry) == 0:
        messagebox.showerror(title="Cannot leave empty", message="You have to enter something to do")
        return False

    if len(data) > 0 and entry in list(data.values()):
        messagebox.showerror(title="Enter a new todo", message=f"You are not done with {entry} task.")
        return False

    return True


# ---------------------------- FILE STORAGE ------------------------------- #
def save_to_db(new_data):
    try:
        with open(MEMORY_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        with open(MEMORY_PATH, "w") as f:
            json.dump(new_data, f, indent=4)
    else:
        data.update(new_data)
        with open(MEMORY_PATH, "w") as f:
            json.dump(data, f, indent=4)
    finally:
        todo_entry.delete(0, tk.END)


def load_from_db():
    try:
        with open(MEMORY_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {}
    else:
        return data


def remove_from_db(data):
    with open(MEMORY_PATH, "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------- ADD ENTRY TO LISTBOX ------------------------------- #
def add_to_list():
    global unique_id
    unique_id += 1

    entry = todo_entry.get().title()

    if validate_entry(entry):
        display_listbox(entry)
        save_to_db({unique_id: entry})


# ---------------------------- DELETE ITEM FROM LISTBOX ------------------------------- #
def remove_from_list():
    global unique_id
    data = load_from_db()

    if len(data) > 0:
        i = todo_listbox.curselection()[0]
        item = todo_listbox.get(i)

        data_keys = list(data.keys())
        data_values = list(data.values())

        remove_this = messagebox.askyesno(title="Remove Task", message="Are you done with this task?")

        if remove_this and item in data_values:
            idx = data_values.index(item)
            key = data_keys[idx]
            todo_idx = todo_listbox.get(0, tk.END).index(item)

            data.pop(key)
            todo_listbox.delete(todo_idx)

            todo_entry.focus()
            set_unique_id(list(data))
            remove_from_db(data)


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.geometry("600x400")
window.title("Todo List")
window.config(pady=50, padx=50)

title_label = tk.Label(window, text="TODO LIST", font=("Arial", 25, "bold"))
title_label.pack()

content_frame = tk.Frame(window)
content_frame.pack()
content_frame.config(padx=20, pady=20)

content_label = tk.Label(content_frame, text="Enter a task:", font=("Arial", 15, "normal"))
content_label.grid(column=0, row=0)

todo_entry = tk.Entry(content_frame)
todo_entry.grid(column=0, row=1)

add_btn = tk.Button(content_frame, width=17, text="Add", highlightthickness=0, command=add_to_list)
add_btn.grid(column=0, row=2)

done_btn = tk.Button(content_frame, width=17, text="Done", highlightthickness=0, command=remove_from_list)
done_btn.grid(column=0, row=3)

tk.Button(content_frame, width=17, text="Exit", highlightthickness=0, command=window.destroy).grid(column=0, row=4)

tk.Frame(content_frame, padx=20, pady=20, height=10, width=40).grid(column=1, row=0, rowspan=5)

todo_frame = tk.Frame(content_frame, padx=5, pady=5)
todo_frame.grid(column=2, row=0, rowspan=5)

todo_listbox = tk.Listbox(todo_frame)
todo_listbox.pack()

load_listbox()
window.mainloop()
