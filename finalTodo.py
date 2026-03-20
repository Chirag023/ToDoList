import tkinter as tk
from tkinter import filedialog
import uuid
import customtkinter as ctk
import json
import os

CONFIG_FILE = "config.json"
SAVE_DIR = None

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None


def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

def ask_folder():
    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Choose folder to save your tasks")

    root.destroy()
    return folder

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

config = load_config()

if not config:
    SAVE_DIR = ask_folder()

    if not SAVE_DIR:
        raise SystemExit("No folder selected!")

    save_config({"save_dir": SAVE_DIR})
else:
    SAVE_DIR = config["save_dir"]


ACTIVE_FILE = os.path.join(SAVE_DIR, "tasks.json")
COMPLETED_FILE = os.path.join(SAVE_DIR, "CompletedTasks.json")

os.makedirs(SAVE_DIR, exist_ok=True)


tasks = []
completedTasks = []
view_mode = "active"


# ---------------- LOAD ----------------
def load_data():
    global tasks, completedTasks

    if os.path.exists(ACTIVE_FILE):
        with open(ACTIVE_FILE, "r") as f:
            try:
                tasks = json.load(f)
            except:
                tasks = []

    if os.path.exists(COMPLETED_FILE):
        with open(COMPLETED_FILE, "r") as f:
            try:
                completedTasks = json.load(f)
            except:
                completedTasks = []


# ---------------- SAVE ----------------
def save_tasks():
    with open(ACTIVE_FILE, "w") as f:
        json.dump(tasks, f)

def save_completed():
    with open(COMPLETED_FILE, "w") as f:
        json.dump(completedTasks, f)


# ---------------- ADD ----------------
def add_task(event=None):
    text = entry.get().strip()
    if not text:
        return

    tasks.append({
        "id": str(uuid.uuid4()),
        "text": text,
        "done": False
    })

    entry.delete(0, "end")

    save_tasks()
    refresh_ui()


# ---------------- COMPLETE ----------------
def complete_task(task_id):
    for task in tasks:
        if task["id"]==task_id:
            tasks.remove(task)

            task["done"] = True
            completedTasks.append(task)

            save_tasks()
            save_completed()
            refresh_ui()
            return


# ---------------- MODE ----------------
def set_mode(mode):
    global view_mode
    view_mode = mode
    refresh_ui()

    frame_tasks._parent_canvas.yview_moveto(0)

def make_handler(tid):
    def handler(event):
        complete_task(tid)
    return handler

# ---------------- UI ----------------
def refresh_ui():
    for widget in frame_tasks.winfo_children():
        widget.destroy()

    if view_mode == "active":
        data = tasks
    elif view_mode == "completed":
        data = completedTasks
        font = ("Arial", 16, "overstrike")
    else:
        data = completedTasks + tasks

    if not data:
        ctk.CTkLabel(frame_tasks, text="No tasks here").pack(pady=20)
        return

    for i,task in enumerate(reversed(data)):

        bg = "#414040" if i % 2 == 0 else "#242424"
        btn_bg = "#242424" if i % 2 == 0 else "#414040"

        card = ctk.CTkFrame(frame_tasks, corner_radius=12, fg_color=bg)
        card.pack(fill="x", pady=5, padx=10)

        if view_mode == "completed":
            font = ("Arial", 16)
        else:
            font = ("Arial", 16, "overstrike") if task["done"] else ("Arial", 16)

        label = ctk.CTkLabel(
            card,
            text=task["text"],
            anchor="w",
            font=font
        )
        label.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        if view_mode == "active":
            ctk.CTkButton(
                card,
                text="✕",
                width=30,
                corner_radius=10,
                fg_color=btn_bg,
                hover_color="#323858",
                command=lambda tid=task["id"]: complete_task(tid)
            ).pack(side="right", padx=10)

        handler = make_handler(task["id"])
        
        card.bind("<Double-Button-1>", handler)
        label.bind("<Double-Button-1>", handler)
    
    frame_tasks.update_idletasks()
    frame_tasks._parent_canvas.configure(
        scrollregion=frame_tasks._parent_canvas.bbox("all")
    )


# ---------------- APP ----------------
app = ctk.CTk()
app.title("To-Do App")
app.geometry("400x500")

entry = ctk.CTkEntry(app, placeholder_text="Enter a task...")
entry.pack(pady=15, padx=10, fill="x")
entry.bind("<Return>", add_task)

ctk.CTkButton(app, text="Add Task", command=add_task, corner_radius=10)\
    .pack(pady=5)

toggle_frame = ctk.CTkFrame(app, corner_radius=10)
toggle_frame.pack(pady=10)

ctk.CTkButton(toggle_frame, text="Active",
              command=lambda: set_mode("active")).pack(side="left", padx=5)

ctk.CTkButton(toggle_frame, text="Completed",
              command=lambda: set_mode("completed")).pack(side="left", padx=5)

ctk.CTkButton(toggle_frame, text="All",
              command=lambda: set_mode("all")).pack(side="left", padx=5)


# ---------------- SCROLL AREA ----------------
frame_tasks = ctk.CTkScrollableFrame(app, corner_radius=10)
frame_tasks.pack(fill="both", expand=True, padx=10, pady=10)

def _on_mousewheel(event):
    frame_tasks._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

frame_tasks.bind_all("<MouseWheel>", _on_mousewheel)
frame_tasks.bind_all("<Button-4>", lambda e: frame_tasks._parent_canvas.yview_scroll(-1, "units"))
frame_tasks.bind_all("<Button-5>", lambda e: frame_tasks._parent_canvas.yview_scroll(1, "units"))

# ---------------- START ----------------
load_data()
refresh_ui()
app.mainloop()