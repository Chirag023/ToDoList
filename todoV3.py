import tkinter as tk
import json
import os

ACTIVE_FILE = os.path.expanduser("~/VsCode/RandomProjects/ToDoList/tasks.json")
COMPLETED_FILE = os.path.expanduser("~/VsCode/RandomProjects/ToDoList/CompletedTasks.json")
tasks = []
completedTasks = []

view_mode = "active" # active | completed | all


# ---------------- LOAD ----------------
def load_data():
    global tasks, completedTasks

    if os.path.exists(ACTIVE_FILE):
        with open(ACTIVE_FILE, "r") as f:
            tasks = json.load(f)

    if os.path.exists(COMPLETED_FILE):
        with open(COMPLETED_FILE, "r") as f:
            completedTasks = json.load(f)


# ---------------- SAVE ACTIVE ----------------
def save_tasks():
    with open(ACTIVE_FILE, "w") as f:
        json.dump(tasks, f)


# ---------------- SAVE COMPLETED ----------------
def save_completed():
    with open(COMPLETED_FILE, "w") as f:
        json.dump(completedTasks, f)


# ---------------- ADD TASK ----------------
def add_task(event=None):
    text = entry.get().strip()
    if not text:
        return

    tasks.append({
        "text": text,
        "done": False
    })

    entry.delete(0, tk.END)
    save_tasks()
    refresh_ui()


# ---------------- TOGGLE CHECKBOX ----------------
def toggle_task(index):
    tasks[index]["done"] = not tasks[index]["done"]
    save_tasks()
    refresh_ui()


# ---------------- COMPLETE ----------------
def complete_task(index):
    task = tasks.pop(index)

    task["done"] = True
    completedTasks.append(task)

    save_tasks()
    save_completed()
    refresh_ui()

# ---------------- VIEW MODE ----------------
def set_mode(mode):
    global view_mode
    view_mode = mode
    refresh_ui()


# ---------------- UI ----------------
def refresh_ui():
    for widget in frame_tasks.winfo_children():
        widget.destroy()

    if view_mode == "active":
        data = tasks

    elif view_mode == "completed":
        data = completedTasks

    else:
        data = tasks + completedTasks

    for i, task in enumerate(data):

        row = tk.Frame(frame_tasks)
        row.pack(fill="x", pady=2, padx=5)

        text = task["text"]
        done = task["done"]

        font_style = ("Arial", 10, "overstrike") if done else ("Arial", 10)

        label = tk.Label(row, text=text, font=font_style)
        label.pack(side="left")

        # ACTIVE MODE CONTROLS ONLY
        if view_mode == "active":

            tk.Button(
                row,
                text="✕",
                command=lambda idx=i: complete_task(idx)
            ).pack(side="right")

            row.bind("<Double-Button-1>", lambda e, idx=i: complete_task(idx))
            label.bind("<Double-Button-1>", lambda e, idx=i: complete_task(idx))


# ---------------- GUI ----------------
root = tk.Tk()
root.title("To-Do App")
root.geometry("400x500")


entry = tk.Entry(root, width=30)
entry.pack(pady=10)

entry.bind("<Return>", add_task)

tk.Button(root, text="Add Task", command=add_task).pack(pady=5)


# ---------------- TOGGLES ----------------
toggle_frame = tk.Frame(root)
toggle_frame.pack(pady=5)

tk.Button(toggle_frame, text="Active",
          command=lambda: set_mode("active")).pack(side="left", padx=5)

tk.Button(toggle_frame, text="Completed",
          command=lambda: set_mode("completed")).pack(side="left", padx=5)

tk.Button(toggle_frame, text="All",
          command=lambda: set_mode("all")).pack(side="left", padx=5)


# ---------------- TASK AREA ----------------
frame_tasks = tk.Frame(root)
frame_tasks.pack(fill="both", expand=True)


# ---------------- START ----------------
load_data()
refresh_ui()
root.mainloop()