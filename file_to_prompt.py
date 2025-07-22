import tkinter as tk
from tkinter import filedialog

# Keep track of selected files
file_list = []

def add_files():
    """Open file dialog and add selected files to the list (no duplicates)."""
    new_files = filedialog.askopenfilenames(title="Select Files")
    for f in new_files:
        if f not in file_list:
            file_list.append(f)
            listbox.insert(tk.END, f)

def remove_files():
    """Remove selected entries from the list."""
    selected = listbox.curselection()
    for idx in reversed(selected):
        listbox.delete(idx)
        del file_list[idx]

def transform_to_prompt():
    """Read each file and display its path and contents in the text area."""
    result_text.delete("1.0", tk.END)
    for fpath in file_list:
        result_text.insert(tk.END, f"```{fpath}\n")
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f"{f.read()}```"
        except Exception as e:
            content = f"[Error reading file: {e}]"
        result_text.insert(tk.END, content + "\n\n")

def copy_to_clipboard():
    """Copy the contents of the result_text to the clipboard."""
    data = result_text.get("1.0", tk.END)
    if data.strip():
        root.clipboard_clear()
        root.clipboard_append(data)
        # Optional: give the user feedback
        status_label.config(text="Prompt copied to clipboard!", fg="green")
    else:
        status_label.config(text="Nothing to copy.", fg="red")

# Build the UI
root = tk.Tk()
root.title("File to Prompt Transformer")
root.geometry("800x600")

# --- File list with scrollbar ---
list_frame = tk.Frame(root)
list_frame.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)

list_scroll = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
listbox = tk.Listbox(
    list_frame,
    selectmode=tk.EXTENDED,
    yscrollcommand=list_scroll.set,
    width=100,
    height=8
)
list_scroll.config(command=listbox.yview)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
list_scroll.pack(side=tk.RIGHT, fill=tk.Y)

# --- Buttons ---
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, padx=5, pady=5)

btn_add      = tk.Button(button_frame, text="Add Files",            command=add_files)
btn_remove   = tk.Button(button_frame, text="Remove Selected",      command=remove_files)
btn_transform= tk.Button(button_frame, text="Transform to Prompt",  command=transform_to_prompt)
btn_copy     = tk.Button(button_frame, text="Copy Prompt",          command=copy_to_clipboard)

btn_add.pack(side=tk.LEFT,   padx=5)
btn_remove.pack(side=tk.LEFT,padx=5)
btn_transform.pack(side=tk.LEFT, padx=5)
btn_copy.pack(side=tk.LEFT,    padx=5)

# Status label for copy feedback
status_label = tk.Label(button_frame, text="", anchor="w")
status_label.pack(side=tk.LEFT, padx=10)

# --- Result text area with scrollbar ---
result_frame = tk.Frame(root)
result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

text_scroll = tk.Scrollbar(result_frame, orient=tk.VERTICAL)
result_text = tk.Text(
    result_frame,
    wrap=tk.WORD,
    yscrollcommand=text_scroll.set
)
text_scroll.config(command=result_text.yview)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()