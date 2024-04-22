# ClearNote - A transparent, note-taking desktop application written in Python.
# Developer/Author: Leo Angelo Dulay Genota

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class ClearNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ClearNote")

        # Set window transparency (0 = fully transparent, 1 = fully opaque)
        self.root.attributes("-alpha", 0.5)
        
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Create a frame for each tab
        self.frames = []
        self.text_areas = []
        
        # Add initial tab
        self.add_tab()
        
        # Add a save button
        self.save_button = ttk.Button(self.root, text="Save", command=self.save_notes)
        self.save_button.pack(side="left", padx=10, pady=5)
        
        # Add a clear button
        self.clear_button = ttk.Button(self.root, text="Clear", command=self.clear_notes)
        self.clear_button.pack(side="left", padx=10, pady=5)
        
        # Add a new tab button
        self.new_tab_button = ttk.Button(self.root, text="New Tab", command=self.add_tab)
        self.new_tab_button.pack(side="left", padx=10, pady=5)
        
        # Add a close button
        self.close_button = ttk.Button(self.root, text="Close Tab", command=self.close_tab)
        self.close_button.pack(side="left", padx=10, pady=5)
        
        # Add a quit button
        self.quit_button = ttk.Button(self.root, text="Quit", command=self.confirm_quit)
        self.quit_button.pack(side="right", padx=10, pady=5)
        
    def add_tab(self):
        # Function to add a new tab
        frame = ttk.Frame(self.notebook)
        frame.pack(fill="both")
        
        text_area = tk.Text(frame, wrap="word")
        text_area.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.text_areas.append(text_area)
        self.frames.append(frame)
        
        self.notebook.add(frame, text=f"Tab {len(self.frames)}")
        self.notebook.select(len(self.frames) - 1)
        
    def close_tab(self):
        # Function to close the current tab
        index = self.notebook.index("current")

        # Check if the tab has text
        notes = self.text_areas[index].get("1.0", "end-1c").strip()
        if notes:  # If there are notes in the tab
            save_confirmation = messagebox.askyesnocancel("Save Confirmation", "Do you want to save your notes before closing the tab?")
            if save_confirmation is None:
                # User clicked cancel
                return
            elif save_confirmation:
                self.save_notes()

        # If closing the last tab, no need to adjust tab numbering
        if len(self.frames) == 1:
            # If only one tab is open and the user chose not to save, just return
            self.text_areas[index].delete("1.0", "end")
            return

        # Forget the current tab
        self.notebook.forget(index)
        self.frames.pop(index)
        self.text_areas.pop(index)

        # Renumber the remaining tabs
        for i, frame in enumerate(self.frames):
            tab_name = f"Tab {i + 1}"
            self.notebook.tab(frame, text=tab_name)

        
    def confirm_quit(self):
        # Function to confirm quitting the application
        save_confirmation = messagebox.askyesnocancel("Save Confirmation", "Do you want to save your notes before quitting?")
        if save_confirmation is None:
            # User clicked cancel
            return
        elif save_confirmation:
            self.save_notes()
        self.root.quit()
        
    def save_notes(self):
        # Function to save notes to a file
        current_tab_index = self.notebook.index("current")
        notes = self.text_areas[current_tab_index].get("1.0", "end-1c")  # Get text from current tab
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(notes)
                messagebox.showinfo("Success", "Notes saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save notes: {e}")

        
    def clear_notes(self):
        # Function to clear the text area of the current tab
        current_tab_index = self.notebook.index("current")
        self.text_areas[current_tab_index].delete("1.0", "end")
        messagebox.showinfo("Success", "Notes cleared!")

def main():
    root = tk.Tk()
    app = ClearNoteApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
