import tkinter as tk
import os
import winsound  # Import the winsound library

# Character limit for the description field
CHARACTER_LIMIT = 100

# Function to add a task and open a window for it
def add_task():
    add_window = tk.Toplevel(root)
    add_window.title("Add Task")
    
    # Create a label and entry for task name
    tk.Label(add_window, text="Task Name:").pack()
    task_name_entry = tk.Entry(add_window, width=40)
    task_name_entry.pack()
    
    # Create a label and text entry for task description
    tk.Label(add_window, text="Description:").pack()
    task_description_text = tk.Text(add_window, wrap=tk.WORD, width=40, height=5)
    task_description_text.pack()

    # Create a label to display remaining character count
    character_count_label = tk.Label(add_window, text=f"0/{CHARACTER_LIMIT} symbols left")
    character_count_label.pack()

    # Function to update the character count label
    def update_character_count(event):
        character_count = len(task_description_text.get("1.0", tk.END))
        remaining_count = CHARACTER_LIMIT - character_count
        character_count_label.config(text=f"{character_count}/{CHARACTER_LIMIT} symbols left")
        if remaining_count < 0:
            character_count_label.config(fg="red")
        else:
            character_count_label.config(fg="black")
    
    # Bind a function to the text widget to update character count
    task_description_text.bind("<KeyRelease>", update_character_count)
    
    # Function to validate the description field and limit character count
    def validate_description(P):
        description = task_description_text.get("1.0", tk.END)
        character_count = len(description)
        if character_count > CHARACTER_LIMIT:
            # Play a noise to indicate the character limit is exceeded
            winsound.Beep(1000, 500)
            description = description[:CHARACTER_LIMIT]  # Trim the description
            task_description_text.delete("1.0", tk.END)
            task_description_text.insert("1.0", description)
        return True
    
    # Bind a function to the text widget to validate character count
    task_description_text.bind("<KeyRelease>", validate_description)
    
    # Function to save the added task
    def save_task():
        task_name = task_name_entry.get()
        description = task_description_text.get("1.0", tk.END)
        create_task_file(task_name, description)
        task_listbox.insert(tk.END, task_name)
        add_window.destroy()
    
    # Function to cancel adding a task
    def cancel_task():
        add_window.destroy()
    
    # Create buttons to save the task or cancel
    save_button = tk.Button(add_window, text="Save", command=save_task)
    save_button.pack()
    cancel_button = tk.Button(add_window, text="Cancel", command=cancel_task)
    cancel_button.pack()

# Function to remove the selected task and its text file
def remove_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        selected_task = task_listbox.get(selected_task_index[0])
        task_listbox.delete(selected_task_index)
        delete_task_file(selected_task)

# Function to edit the selected task
def edit_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        selected_task = task_listbox.get(selected_task_index[0])
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Task")
        
        # Create a label and entry for task name
        tk.Label(edit_window, text="Task Name:").pack()
        task_name_entry = tk.Entry(edit_window, width=40)
        task_name_entry.insert(0, selected_task)
        task_name_entry.pack()
        
        # Create a label and text entry for task description
        tk.Label(edit_window, text="Description:").pack()
        task_description_text = tk.Text(edit_window, wrap=tk.WORD, width=40, height=5)
        task_description_text.pack()
        
        task_file = os.path.join("tasks", f"{selected_task}.txt")
        if os.path.exists(task_file):
            with open(task_file, "r") as file:
                description = file.read()
                task_description_text.insert("1.0", description)

        # Create a label to display remaining character count
        character_count_label = tk.Label(edit_window, text=f"0/{CHARACTER_LIMIT} symbols left")
        character_count_label.pack()
        
        # Function to update the character count label
        def update_character_count(event):
            character_count = len(task_description_text.get("1.0", tk.END))
            remaining_count = CHARACTER_LIMIT - character_count
            character_count_label.config(text=f"{character_count}/{CHARACTER_LIMIT} symbols left")
            if remaining_count < 0:
                character_count_label.config(fg="red")
            else:
                character_count_label.config(fg="black")
        
        # Bind a function to the text widget to update character count
        task_description_text.bind("<KeyRelease>", update_character_count)
        
        # Function to validate the description field and limit character count
        def validate_description(P):
            description = task_description_text.get("1.0", tk.END)
            character_count = len(description)
            if character_count > CHARACTER_LIMIT:
                # Play a noise to indicate the character limit is exceeded
                winsound.Beep(1000, 500)
                description = description[:CHARACTER_LIMIT]  # Trim the description
                task_description_text.delete("1.0", tk.END)
                task_description_text.insert("1.0", description)
            return True
        
        # Bind a function to the text widget to validate character count
        task_description_text.bind("<KeyRelease>", validate_description)
        
        # Function to save changes to the task
        def save_changes():
            new_task_name = task_name_entry.get()
            new_description = task_description_text.get("1.0", tk.END)
            new_task_file = os.path.join("tasks", f"{new_task_name}.txt")
            
            if new_task_name != selected_task:
                # Rename the task file
                os.rename(task_file, new_task_file)
            
            # Save the updated description
            with open(new_task_file, "w") as file:
                file.write(new_description)
            
            task_listbox.delete(selected_task_index)
            task_listbox.insert(selected_task_index[0], new_task_name)
            edit_window.destroy()
        
        # Function to cancel editing
        def cancel_edit():
            edit_window.destroy()
        
        # Create buttons to save changes or cancel editing
        save_button = tk.Button(edit_window, text="Save", command=save_changes)
        save_button.pack()
        cancel_button = tk.Button(edit_window, text="Cancel", command=cancel_edit)
        cancel_button.pack()

# Function to create a task's text file
def create_task_file(task_name, description):
    task_file = os.path.join("tasks", f"{task_name}.txt")
    with open(task_file, "w") as file:
        file.write(description)

# Function to delete a task's text file
def delete_task_file(task_name):
    task_file = os.path.join("tasks", f"{task_name}.txt")
    if os.path.exists(task_file):
        os.remove(task_file)

# Create the main window
root = tk.Tk()
root.title("To-Do List")

# Create a button to add tasks
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack()

# Create a button to edit tasks
edit_button = tk.Button(root, text="Edit Task", command=edit_task)
edit_button.pack()

# Create a listbox to display tasks
task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=40)
task_listbox.pack()

# Create a button to remove selected tasks
remove_button = tk.Button(root, text="Remove Task", command=remove_task)
remove_button.pack()

# Create a directory to store task files
if not os.path.exists("tasks"):
    os.makedirs("tasks")

# Load tasks from the "tasks" directory
for task_file in os.listdir("tasks"):
    if task_file.endswith(".txt"):
        task_name = os.path.splitext(task_file)[0]
        task_listbox.insert(tk.END, task_name)

# Start the main loop
root.mainloop()
