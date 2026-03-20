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
            try:
                tasks = json.load(f)
            except json.JSONDecodeError:
                tasks = []

    if os.path.exists(COMPLETED_FILE):
        with open(COMPLETED_FILE, "r") as f:
            try:
                completedTasks = json.load(f)
            except json.JSONDecodeError:
                completedTasks = []


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

    if not data:
        tk.Label(frame_tasks, text="No tasks here").pack()
        return
    else:
        for i, task in enumerate(data):

            bg_color = "#ffffff" if i % 2 == 0 else "#d3d3d3"
            
            row = tk.Frame(frame_tasks, bg=bg_color)
            row.pack(fill="x", expand=True, pady=2, padx=5)

            text = task["text"]
            done = task["done"]

            font_style = ("Arial", 10, "overstrike") if done else ("Arial", 10)

            label = tk.Label(row, text=text, font=font_style, bg=bg_color)
            label.pack(side="left")

            # ACTIVE MODE CONTROLS ONLY
            if view_mode == "active":

                tk.Button(
                    row,
                    text="✕",
                    bg="#423D3D",
                    fg="#E2D8D8",
                    relief="flat",
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
container = tk.Frame(root)
container.pack(fill="both", expand=True)

canvas = tk.Canvas(container)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

frame_tasks = tk.Frame(canvas)

frame_tasks.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas_window = canvas.create_window((0,0), window=frame_tasks, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def resize_frame(event):
    canvas.itemconfig(canvas_window, width=event.width)

canvas.bind("<Configure>", resize_frame)
# ---------------- MOUSE WHEEL SCROLL --------------

def _on_mousewheel(event):
    if event.num==5:
        canvas.yview_scroll(1, "units")
    elif event.num==4:
        canvas.yview_scroll(-1, "units")
    elif event.delta:
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)
canvas.bind_all("<Button-4>", _on_mousewheel)
canvas.bind_all("<Button-5>", _on_mousewheel)


# ---------------- START ----------------
load_data()
refresh_ui()
root.mainloop()