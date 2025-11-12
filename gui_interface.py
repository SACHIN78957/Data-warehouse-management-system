import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
from threading import Thread
import os
import sys

class DataWarehouseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce ETL Pipeline Dashboard")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.main_script_path = os.path.join(base_dir, "reports", "main.py")
        
        self.run_button = tk.Button(root, text="🚀 RUN FULL ETL PIPELINE 🚀", command=self.start_pipeline_thread, font=('Arial', 14, 'bold'), bg='#4CAF50', fg='white')
        self.run_button.pack(pady=15, padx=20, fill=tk.X)

        tk.Label(root, text="Pipeline Status & Analysis Output:", font=('Arial', 12, 'underline')).pack(pady=(10, 5))
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=25, width=80, font=('Consolas', 10), bg='#1e1e1e', fg='#00ff00')
        self.output_text.pack(padx=20, pady=(0, 20), fill=tk.BOTH, expand=True)
        self.output_text.insert(tk.END, "Ready to run the Data Warehouse ETL and Analysis pipeline.\n\n")

    def start_pipeline_thread(self):
        """Starts the ETL pipeline in a separate thread to keep the GUI responsive."""
        self.run_button['state'] = tk.DISABLED
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Pipeline execution started...\n\n")

        process_thread = Thread(target=self.run_pipeline)
        process_thread.start()

    def run_pipeline(self):
        """Executes the main script using subprocess and captures output."""
        try:
            command = [sys.executable, self.main_script_path]
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            with process.stdout:
                for line in iter(process.stdout.readline, ''):
                    self.update_output(line)

            process.wait() 
            
            if process.returncode == 0:
                self.update_output("\n Pipeline completed successfully.\n")
            else:
                self.update_output(f"\n Pipeline failed with exit code {process.returncode}.\n")

        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            self.update_output(f"\nFATAL ERROR: {error_message}\n")
            messagebox.showerror("Pipeline Error", error_message)
        finally:
            self.root.after(0, lambda: self.run_button.config(state=tk.NORMAL))

    def update_output(self, text):
        """Thread-safe way to update the Tkinter Text widget."""
        self.output_text.insert(tk.END, text)
        self.output_text.yview(tk.END)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataWarehouseGUI(root)
    root.mainloop()