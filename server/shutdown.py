import tkinter as tk
from tkinter import  messagebox
import subprocess
class ServerShutdownWindow:
    def __init__(self, server):
        self.server = server
        self.window = tk.Tk()
        self.window.title("Server Shutdown")
        self.label = tk.Label(self.window, text="Server will be shutdown in 30 seconds.")
        self.label.pack()
        self.remaining_time = 30
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.label.config(text=f"Server will be shutdown in {self.remaining_time} seconds.")
            self.remaining_time -= 1
            self.window.after(1000, self.update_timer)
        else:
            self.window.destroy()
            self.shutdown_system()
            messagebox.showinfo("Server Shutdown", "Server has been shutdown successfully.")

    def shutdown_system(self):
        try:
            subprocess.call("shutdown /s /t 0", shell=True)
        except Exception as e:
            messagebox.showerror("Shutdown Error", f"Error shutting down system: {str(e)}")

    def start(self):
        self.window.mainloop()