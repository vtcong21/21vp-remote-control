import socket
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
            return 1
        except ConnectionRefusedError:
            print("Không thể kết nối tới server.")
            return 

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

   