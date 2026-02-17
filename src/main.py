import os
import keyboard
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

OPEN_FILE_TXT = "src\open_file.txt"
filepath = ''

def check_open_files(window, text_edit, directory_label):
    try:
        with open(OPEN_FILE_TXT, 'r') as f:
            global filepath
            filepath = f.read()

            if not filepath:
                return
            
            directory_label.config(text=filepath)

            if os.path.exists(filepath):
                with open(filepath, 'r') as file:
                    content = file.read()
                    text_edit.delete("1.0", tk.END)
                    text_edit.insert(tk.END, content)
                    window.title(f"{filepath}")
            else:
                with open(OPEN_FILE_TXT, 'w') as f:
                    f.seek(0)
                    f.truncate()

                filepath = ''

                return check_open_files(window, text_edit, directory_label)
    except:
        return

def new_file(window, text_edit, directory_label):
    window.title("New file")
    
    global filepath
    filepath = ''
    directory_label.config(text='Unsaved file')

    text_edit.delete("1.0", tk.END)

def open_file(window, text_edit, directory_label):
    selected_filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])

    if not selected_filepath:
        return

    with open(selected_filepath, 'r') as file:
        content = file.read()
        text_edit.delete("1.0", tk.END)
        text_edit.insert(tk.END, content)
        window.title(f"{selected_filepath}")

    with open(OPEN_FILE_TXT, 'w') as file:
        file.seek(0)
        file.truncate()
        file.write(selected_filepath)

    global filepath
    filepath = selected_filepath
    directory_label.config(text=filepath)

def save_as_file(window, text_edit, directory_label):
    selected_filepath = asksaveasfilename(filetypes=[("Text Files", "*.txt")])

    if not selected_filepath:
        return
    
    with open(selected_filepath, 'w') as file:
        content = text_edit.get("1.0", tk.END)
        file.write(content)
        window.title(f"{selected_filepath}")

    with open(OPEN_FILE_TXT, 'w') as file:
        file.seek(0)
        file.truncate()
        file.write(selected_filepath)

    global filepath
    filepath = selected_filepath
    directory_label.config(text=filepath)

def save_file(window, text_edit, directory_label, event):
    if len(str(event.name)) > 1:
        return
    elif not (ord(event.name) >= 32 and ord(event.name) <= 126):
        return
    
    if filepath == '':
        return

    with open(filepath, 'w') as f:
        content = text_edit.get("1.0", tk.END)
        f.seek(0)
        f.truncate()
        f.write(content)

def main():
    window = tk.Tk()
    window.rowconfigure(0, minsize=400, weight=1)
    window.columnconfigure(0, minsize=110, weight=1)
    window.columnconfigure(1, minsize=150, weight=500)
    window.title(filepath if not filepath else "New file ")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    window.option_add("*insertBackground", "white")

    window.configure(bg="black")

    # text area
    text_frame = tk.Frame(window)
    text_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    text_frame.configure(bg="gray15")

    directory_label = tk.Label(text_frame, font="Helvetica 10", text="Unsaved file")
    directory_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
    directory_label.configure(bg="gray15", fg="gray60")

    text_edit = tk.Text(text_frame, font="Arial 13", bd=0)
    text_edit.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
    text_edit.configure(bg="gray15", fg="white")

    # Sidebar
    sidebar = tk.Frame(window)
    sidebar.configure(bg="gray15")
    sidebar.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

    new_btn = tk.Button(sidebar, text="New", width=10, command=lambda: new_file(window, text_edit, directory_label))
    open_btn = tk.Button(sidebar, text="Open", width=10, command=lambda: open_file(window, text_edit, directory_label))
    # save_btn = tk.Button(sidebar, text="Save", width=10, command=lambda: save_file(window, text_edit))
    save_as_btn = tk.Button(sidebar, text="Save as", width=10, command=lambda: save_as_file(window, text_edit, directory_label))

    new_btn.grid(column=0, row=0, padx=5, pady=5)
    open_btn.grid(column=0, row=1, padx=5, pady=5)
    # save_btn.grid(column=0, row=2, padx=5, pady=5)
    save_as_btn.grid(column=0, row=2, padx=5, pady=5)

    new_btn.configure(bg="gray10", fg="white", activebackground="gray15", activeforeground="white")
    open_btn.configure(bg="gray10", fg="white", activebackground="gray15", activeforeground="white")
    # save_btn.configure(bg="gray10", fg="white", activebackground="gray15", activeforeground="white")
    save_as_btn.configure(bg="gray10", fg="white", activebackground="gray15", activeforeground="white")

    check_open_files(window, text_edit, directory_label)

    keyboard.on_press(lambda event: save_file(window, text_edit, directory_label, event))

    window.bind("<Control-s>", lambda x: save_file(window, text_edit, directory_label) if filepath else save_as_file(window, text_edit, directory_label))
    window.bind("<Control-n>", lambda x: new_file(window, text_edit, directory_label))
    window.bind("<Control-o>", lambda x: open_file(window, text_edit, directory_label))

    window.mainloop()
    
if __name__ == "__main__":
    main()