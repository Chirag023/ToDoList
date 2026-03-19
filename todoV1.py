import tkinter as tk
import json
import os

TASKS_LIST = os.path.expanduser("~/VsCode/RandomProjects/ToDoList/tasks.json")
COMPLETED_TASKS_LIST = os.path.expanduser("~/VsCode/RandomProjects/ToDoList/CompletedTasks.json")
listbox_tasks = []

#load any previous tasks from file
def load_tasks():
    global listbox_tasks
    if os.path.exists(TASKS_LIST):
        #load file as readonly
        with open(TASKS_LIST, "r") as file:  
            data = json.load(file)
            listbox_tasks.clear()

        for item in data:

            #Old Format load
            # if isinstance(item, str):
            #     listbox_tasks.append({
            #         "text": item,
            #         "done": tk.BooleanVar(value=False)
            #     })
            
            #New Format load
            # else:
                listbox_tasks.append({
                    "text": item["text"],
                    "done" : tk.BooleanVar(value=item["done"])
                })
        
            #should work with only new format code after old tasks are deleted
    refresh_listbox()


def save_tasks():
    data=[
        {"text": t["text"],
        "done": t["done"].get()}
        for t in listbox_tasks
    ]
    #open file with write permission
    with open(TASKS_LIST, "w") as file:
        json.dump(data, file)

def save_completed(completed):
    if os.path.exists(COMPLETED_TASKS_LIST):
        with open(COMPLETED_TASKS_LIST, "r") as f:
            old_data = json.load(f)
    
    else:
        old_data = []

    old_data.extend(completed)

    with open(COMPLETED_TASKS_LIST, "w") as f:
        json.dump(old_data, f)

def add_task():
    text = entry.get().strip()

    if text == "":
        return
    
    listbox_tasks.append({
        "text": text,
        "done": tk.BooleanVar(value=False)
    })
    
    entry.delete(0, tk.END)
    save_tasks()
    refresh_listbox()

def delete_task():
    try:
        global listbox_tasks

        completed = []
        remaining = []
        
        for t in listbox_tasks:
            if t["done"].get():
                completed.append({
                    "text": t["text"],
                    "done": True
                })
            else:
                remaining.append(t)
        save_completed(completed)

        listbox_tasks = remaining
        
        save_tasks()
        refresh_listbox()
        
    except:
        pass

def refresh_listbox():
    for widget in frame_tasks.winfo_children():
        widget.destroy()
    
    for task in listbox_tasks:
        cb = tk.Checkbutton(
            frame_tasks,
            text=task["text"],
            variable=task["done"],
            command=save_tasks
        )
        cb.pack(anchor="w")        

root = tk.Tk()
root.title("To-Do-List")
root.geometry("350x450")

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

tk.Button(root, text="Add Task", command=add_task).pack(pady=5)
entry.bind("<Return>", lambda event: add_task())

tk.Button(root, text="Done", command=delete_task).pack(pady=5)

frame_tasks = tk.Frame(root)
frame_tasks.pack(pady=10, fill="both", expand=True)

load_tasks()
root.mainloop()