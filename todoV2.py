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

def add_task(event=None):
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

def complete_task(task):
    global listbox_tasks

    index = listbox_tasks[task]

    completed = [{
        "text": index["text"],
        "done": True
    }]

    save_completed(completed)

    listbox_tasks.pop(task)

    save_tasks()
    refresh_listbox()
    

def refresh_listbox():
    for widget in frame_tasks.winfo_children():
        widget.destroy()
    
    for i, task in enumerate(listbox_tasks):

        row = tk.Frame(frame_tasks)
        row.pack(fill="x", padx=5, pady=2)

        font_style = ("Arial", 10, "overstrike") if task["done"].get() else ("Arial", 10)
        
        cb = tk.Checkbutton(
            row,
            text=task["text"],
            variable=task["done"],
            font=font_style,
            command=save_tasks
        )
        cb.pack(side="left")

        del_btn = tk.Button(
            row,
            text="x",
            command=lambda idx=i: complete_task(idx)
        )
        del_btn.pack(side="right")

        #bind doubleclick to complete task
        cb.bind("<Double-Button-1>", lambda e, idx=i: complete_task(idx)) 


#--------------------- GUI -----------------

root = tk.Tk()
root.title("To-Do-List")
root.geometry("350x450")

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

tk.Button(root, text="Add Task", command=add_task).pack(pady=5)

#bind so that pressing enter will add task
entry.bind("<Return>", lambda event: add_task())  

frame_tasks = tk.Frame(root)
frame_tasks.pack(pady=10, fill="both", expand=True)

#--------start--------

load_tasks()
root.mainloop()