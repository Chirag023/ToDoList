import tkinter as tk
import json
import os

FILE_NAME = os.path.expanduser("~/VsCode/RandomProjects/ToDoList/tasks.json")
listbox_tasks = []

#load any previous tasks from file
def load_tasks():
    global listbox_tasks
    if os.path.exists(FILE_NAME):
        #load file as readonly
        with open(FILE_NAME, "r") as file:  
            listbox_tasks = json.load(file)
    refresh_listbox()


def save_tasks():
    #open file with write permission
    with open(FILE_NAME, "w") as file:
        json.dump(listbox_tasks, file)


def add_task():
    task = entry.get()
    if task.strip() != "":
        listbox_tasks.append(task)
        entry.delete(0, tk.END)
        save_tasks()
        refresh_listbox()

def delete_task():
    try:
        selected_task = listbox.curselection()[0]
        listbox_tasks.pop(selected_task)
        save_tasks()
        refresh_listbox()
    except:
        pass

def refresh_listbox():
    
    listbox.delete(0, tk.END)
    tasks = list(listbox_tasks)
    for i,task in enumerate(tasks, start=1):
        var = task["done"]

        cb = tk.Checkbutton(
            task
        )
        
        listbox.insert(tk.END, f"{i}. {task}")

root = tk.Tk()
root.title("To-Do-List")
root.geometry("300x400")

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

add_btn = tk.Button(root, text="Add Task", command=add_task)
add_btn.pack(pady=5)
entry.bind("<Return>", lambda event: add_task())

delete_btn=tk.Button(root, text="Delete Task", command=delete_task)
delete_btn.pack(pady=5)

listbox = tk.Listbox(root, width=40, height=15)
listbox.pack(pady=10)

load_tasks()
root.mainloop()