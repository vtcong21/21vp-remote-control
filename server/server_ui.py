# Import các thư viện và lớp cần thiết
import threading  # Thư viện cho việc tạo và quản lý luồng
from tkinter import Tk, Button, messagebox  # Thư viện cho giao diện người dùng
from server import Server  # Import lớp Server từ module server

class ServerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Server")  # Đặt tiêu đề cho cửa sổ gốc
        self.root.geometry("160x70")  # Đặt kích thước cho cửa sổ gốc

        self.server = Server()  # Khởi tạo một đối tượng của lớp Server
        self.start_button = Button(root, text="Start Server", command=self.start_server)  # Tạo nút "Start Server" trên giao diện
        self.start_button.place(relx=0.08, rely=0.11, relwidth=0.85, relheight=0.7)  # Đặt vị trí và kích thước của nút

        # Xử lý sự kiện đóng cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    def start_server(self):
        self.start_button.config(state="disabled")  # Vô hiệu hóa nút "Start" khi máy chủ đã khởi động
        server_thread = threading.Thread(target=self.server.start_server)  # Tạo luồng mới để chạy máy chủ
        server_thread.start()  # Khởi động luồng
        messagebox.showinfo("Server", "Server đã được khởi động!")  # Hiển thị thông báo khi máy chủ đã khởi động

    def close_window(self):
        if messagebox.askokcancel("Đóng Server", "Bạn có chắc chắn muốn đóng Server?"):
            self.server.stop_server()  # Dừng máy chủ
            self.root.destroy()  # Đóng cửa sổ gốc

# Script chạy
if __name__ == "__main__":
    root = Tk()  # Tạo một đối tượng gốc (root window) của giao diện
    server_ui = ServerUI(root)  # Tạo một đối tượng của lớp ServerUI để hiển thị giao diện máy chủ
    root.mainloop()  # Bắt đầu vòng lặp chạy giao diện