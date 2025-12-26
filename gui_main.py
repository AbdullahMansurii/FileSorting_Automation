import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import sort_Downloads
import os

class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Sorter Pro")
        self.root.geometry("600x450")
        
        # Dark Theme Colors
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.accent_color = "#007acc"
        self.text_area_bg = "#1e1e1e"
        
        self.root.configure(bg=self.bg_color)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 10))
        self.style.configure("TButton", padding=6, relief="flat", background=self.accent_color, foreground=self.fg_color, font=("Segoe UI", 10, "bold"))
        self.style.map("TButton", background=[('active', '#005f9e')])
        self.style.configure("TFrame", background=self.bg_color)
        
        # Layout
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20, padx=20, fill="x")
        
        title_label = ttk.Label(header_frame, text="Local File Direct Sorter", font=("Segoe UI", 16, "bold"))
        title_label.pack(side="left")
        
        # Folder Selection
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(control_frame, text="Target Folder:").pack(anchor="w", pady=(0, 5))
        
        self.path_var = tk.StringVar()
        # default to Downloads if possible, else empty
        default_dl = os.path.join(os.path.expanduser("~"), "Downloads")
        if os.path.isdir(default_dl):
            self.path_var.set(default_dl)
            
        self.entry_path = tk.Entry(control_frame, textvariable=self.path_var, font=("Consolas", 10), bg=self.text_area_bg, fg=self.fg_color, insertbackground="white", relief="flat", borderwidth=5)
        self.entry_path.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(control_frame, text="Browse", command=self.browse_folder)
        browse_btn.pack(side="right")
        
        # Action Button
        action_frame = ttk.Frame(self.root)
        action_frame.pack(pady=10, padx=20, fill="x")
        
        self.sort_btn = ttk.Button(action_frame, text="START SORTING", command=self.start_sorting_thread)
        self.sort_btn.pack(fill="x")
        
        # Logs Area
        log_frame = ttk.Frame(self.root)
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        ttk.Label(log_frame, text="Activity Log:").pack(anchor="w", pady=(0, 5))
        
        self.log_text = tk.Text(log_frame, bg=self.text_area_bg, fg="#00ff00", font=("Consolas", 9), relief="flat", state="disabled")
        self.log_text.pack(fill="both", expand=True)
        
        # Scrollbar for logs
        scrollbar = ttk.Scrollbar(self.log_text, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_var.set(folder_selected)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def start_sorting_thread(self):
        target_path = self.path_var.get()
        if not target_path or not os.path.isdir(target_path):
            messagebox.showerror("Error", "Please select a valid folder first.")
            return
            
        self.sort_btn.config(state="disabled", text="Sorting...")
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, "end")
        self.log_text.config(state="disabled")
        
        # Run in background to keep GUI responsive
        threading.Thread(target=self.run_sort, args=(target_path,), daemon=True).start()

    def run_sort(self, target_path):
        try:
            # We pass self.log as the callback
            # Because self.log is thread-safe enough for simple Tkinter appends usually, 
            # but technically we should wrap in after() for strict safety. 
            # For this simple script, direct call often works, but let's be safe.
            
            def thread_safe_log(msg):
                self.root.after(0, lambda: self.log(msg))
                
            sort_Downloads.sort_downloads(target_path, log_callback=thread_safe_log)
            
            self.root.after(0, lambda: messagebox.showinfo("Done", "Sorting Complete!"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
            
        finally:
            self.root.after(0, self.reset_btn)

    def reset_btn(self):
        self.sort_btn.config(state="normal", text="START SORTING")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()
