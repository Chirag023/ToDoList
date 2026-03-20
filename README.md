To Do List

A very basic TO DO List app made using tkinter (and in the final version customtkinter, a more UI friendly tkinter) and json file.

The app can be launched like a python script 'python *todo*.py'. On first launch the app requests to initialize a file directory where all the data(tasks) are stored.

The tasks are stored in [{uniqueID}, {task}, {Boolean}] format. When a task is added it is automatically assigned a unique ID and the boolean 'False', which sets the Task as an "Active" task, when an Active task is completed the Boolean value is changed to "False" and the task is removed from the Active file and stored in the Completed file.

New Tasks can be added by simply pressing enter after the Task Description is done without pressing the Add Task button. Similarly, Active Tasks can be updated as completed by either pressing the 'X' button on the right side of the task or simply double-clicking it.

The Tasks can be viewed in different categories (Active/Completed/All), in case of veiwing in "All" category, completed tasks are shown by a strikethrough formatting-style.
