import tkinter as tk
from tkinter import messagebox
from client import Client
from keylogger_ui import KeyloggerUI
from screenshot_ui import ScreenshotUI
import socket

class ClientUI(Client):
    def __init__(self):
        super().__init__()

        self.window = tk.Tk()
        self.window.title("Client")
        self.window.geometry("400x300")
        self.keyloggerUI = None
        self.screenshotUI = None


        self.server_ip_label = tk.Label(self.window, text="Enter IP Address:")
        self.server_ip_label.pack()

        self.server_ip_entry = tk.Entry(self.window)
        self.server_ip_entry.pack()

        self.connect_button = tk.Button(self.window, text="Connect", command=self.connect_button_click)
        self.connect_button.pack()

    def connect_button_click(self):
        server_ip = self.server_ip_entry.get()
        try:
            self.connect_to_server(server_ip)
            if self.socket:
                self.render_home_window()
        except socket.gaierror:
            error_message = "Không thể kết nối tới server. Vui lòng kiểm tra địa chỉ IP và thử lại."
            self.show_error_message(error_message)
        except Exception as e:
            error_message = "Lỗi xảy ra: " + str(e)
            self.show_error_message(error_message)

    def quit_button_click(self):
        self.disconnect_from_server()
        if(self.keyloggerUI):
            self.keyloggerUI.stop_keylogger()
        
        self.window.quit()
    def run(self):
        self.window.mainloop()

    def show_error_message(self, message):
        messagebox.showerror("Lỗi", message)

    def render_home_window(self):
        if hasattr(self, "server_ip_label"):
            self.server_ip_label.destroy()
            self.server_ip_entry.destroy()
            self.connect_button.destroy()
        self.process_button = tk.Button(self.window, text="Running Processes")
        self.process_button.pack()
        #running apps
        self.app_button = tk.Button(self.window, text="Running Applications", command= self.running_app_button_click)
        self.app_button.pack()
        #keylog
        self.keystroke_button = tk.Button(self.window, text="Keystroke", command=self.keystroke_button_click)
        self.keystroke_button.pack()
        #shutdown
        self.shutdown_button = tk.Button(self.window, text="Shutdown", command=self.shutdown_button_click)
        self.shutdown_button.pack()
        #screenshot
        self.screenshot_button = tk.Button(self.window, text="Take Screenshot", command=self.take_screenshot_button_click)
        self.screenshot_button.pack()
        #quit
        self.quit_button = tk.Button(self.window, text="Quit", command=self.quit_button_click)
        self.quit_button.pack()
    def quit_button_click(self):
        pass
    def keystroke_button_click(self):
        self.keyloggerUI = KeyloggerUI(self.socket, self.window)
    def take_screenshot_button_click(self):
        self.screenshotUI = ScreenshotUI(self.socket, self.window)
    def running_app_button_click(self):
        pass
    def shutdown_button_click(self):
        self.send_message("shutdown")
    def processes_button_click(self):
        pass
    def send_message(self, message):
        if not self.socket:
            print("Not connected to the server.")
            return
        try:
            # Send a message to the server
            self.socket.sendall(message.encode())
            print("Message sent.")
        except OSError:
            print("Failed to send the message.")

# Script chạy
if __name__ == "__main__":
    client_ui = ClientUI()
    client_ui.run()
