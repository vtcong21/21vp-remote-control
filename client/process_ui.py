from process import Processes
import tkinter as tk
from tkinter import Frame
from PIL import Image, ImageTk
from io import BytesIO
import json

class ProcessUI(Processes):
    def __init__(self, socket, window):
        super().__init__(socket, window)
        self.process_window = None

        # Tạo cửa sổ mới để hiển thị chức năng
        self.process_window = tk.Toplevel(self.window)
        self.process_window.geometry("390x90")
        self.process_window.title("List Process")

        # Tạo các nút "Kill", "Xem danh sách", "Xóa" và "Bắt đầu"
        self.kill_button = tk.Button(self.process_window, text="Kill", width=10, height=3)
        self.kill_button.place(x=20, y=16)
        self.view_list_button = tk.Button(self.process_window, text="Show\nlist", command=self.show_list_button_click, width=10, height=3)
        self.view_list_button.place(x=110, y=16)
        self.delete_button = tk.Button(self.process_window, text="Clear", width=10, height=3)
        self.delete_button.place(x=200, y=16)
        self.start_button = tk.Button(self.process_window, text="Start", width=10, height=3)
        self.start_button.place(x=290, y=16)


    def show_list_button_click(self):
        # self.process_window.geometry("400x200")
        self.process_window.geometry("390x350")
        
        self.process_listbox = tk.Listbox(self.process_window, width=58, height=14)
        self.process_listbox.place(x=20, y=90)  # Đặt vị trí dựa trên tọa độ tương đối (0.1, 0.2)

        self.send_message("processus")
        self.process_data = self.receive_message()  # Thay đổi tên hàm theo tên thích hợp

        # if self.process_data:
            # try:
                # process_list = json.loads(self.process_data)
                # # Tạo đầu cột
                # header_row = "ProcessName".ljust(30) + "PID".ljust(15) + "ThreadCount"
                # self.process_listbox.insert(tk.END, header_row)
                
                # for self.process_info in self.process_list:
                #     self.process_name = self.process_info.get("ProcessName", "N/A")
                #     self.process_id = str(self.process_info.get("PID", "N/A")).ljust(15)
                #     self.thread_count = str(self.process_info.get("ThreadCount", "N/A"))
                #     self.formatted_row = self.process_name.ljust(30) + self.process_id + self.thread_count
                #     self.process_listbox.insert(tk.END, self.formatted_row)

            # except Exception as e:
            #     print(f"Lỗi khi hiển thị thông tin tiến trình: {str(e)}")

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
    
    def receive_message(self):
        # Triển khai logic nhận dữ liệu từ máy chủ ở đây
        # Ví dụ: Sử dụng socket để nhận dữ liệu từ máy chủ
        try:
            received_data = self.socket.recv(1024)
            return received_data.decode('utf-8')
        except Exception as e:
            print(f"Lỗi khi nhận dữ liệu: {str(e)}")
            return None