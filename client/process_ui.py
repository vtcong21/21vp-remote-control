from process import Processes
import tkinter as tk
# from tkinter import messagebox, filedialog
# from PIL import Image, ImageTk
# from io import BytesIO

class ProcessUI(Processes):
    def __init__(self, socket, window):
        self.socket = socket
        self.window = window

        # Tạo cửa sổ mới để hiển thị chức năng
        self.process_window = tk.Toplevel(self.window)
        self.process_window.title("Process")

        # Tạo các nút "Kill", "Xem danh sách", "Xóa" và "Bắt đầu"
        kill_button = tk.Button(self.process_window, text="Kill")
        view_list_button = tk.Button(self.process_window, text="Show list", command=self.show_list_button_click)
        delete_button = tk.Button(self.process_window, text="Delete")
        start_button = tk.Button(self.process_window, text="Start")
        
        kill_button.pack()
        view_list_button.pack()
        delete_button.pack()
        start_button.pack()

    
    def show_list_button_click(self):
        self.send_message("get_processes")
        self.process_data = self.receive_message()  # Thay đổi tên hàm theo tên thích hợp

        if self.process_data:
            try:
                # Xóa nội dung cửa sổ hiện tại (nếu có)
                for widget in self.process_window.winfo_children():
                    widget.destroy()

                # Hiển thị dữ liệu tiến trình trong một vùng văn bản
                process_text = tk.Text(self.window)
                process_text.pack()

                # Thêm dữ liệu tiến trình vào vùng văn bản
                process_text.insert(tk.END, self.process_data)

            except Exception as e:
                print(f"Lỗi khi hiển thị thông tin tiến trình: {str(e)}")

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