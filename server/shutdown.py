import tkinter as tk  # Import thư viện tkinter với tên tắt là tk
from tkinter import messagebox  # Import module messagebox từ thư viện tkinter
import subprocess  # Import thư viện subprocess cho việc tương tác với hệ thống

class ServerShutdownWindow:
    def __init__(self, server):
        # Khởi tạo lớp ServerShutdownWindow với đối số đối tượng server.
        # Đối tượng server được truyền vào để tương tác với máy chủ.
        
        self.server = server
        
        # Tạo một cửa sổ giao diện đồ họa (Tkinter).
        self.window = tk.Tk()
        self.window.title("Server Shutdown")  # Đặt tiêu đề cửa sổ.
        
        # Tạo nhãn thông báo với nội dung "Server will be shutdown in 30 seconds."
        self.label = tk.Label(self.window, text="Server will be shutdown in 30 seconds.")
        self.label.pack()  # Hiển thị nhãn lên cửa sổ.
        
        # Khởi tạo biến lưu trữ thời gian còn lại là 30 giây.
        self.remaining_time = 30
        
        # Bắt đầu đếm ngược thời gian bằng cách gọi phương thức update_timer().
        self.update_timer()

    def update_timer(self):
        # Cập nhật đồng hồ đếm ngược.
        if self.remaining_time > 0:
            # Nếu thời gian còn lại lớn hơn 0:
            # Cập nhật nội dung của nhãn với thông tin thời gian còn lại.
            self.label.config(text=f"Server will be shutdown in {self.remaining_time} seconds.")
            self.remaining_time -= 1  # Giảm thời gian còn lại đi 1 giây.
            
            # Đặt thời gian chờ 1 giây trước khi gọi lại phương thức update_timer().
            self.window.after(1000, self.update_timer)
        else:
            # Khi thời gian đếm ngược kết thúc:
            # Đóng cửa sổ thông báo.
            self.window.destroy()
            
            # Thực hiện tắt máy chủ bằng cách gọi phương thức shutdown_system().
            self.shutdown_system()
            
            # Hiển thị thông báo "Server has been shutdown successfully."
            messagebox.showinfo("Server Shutdown", "Server has been shutdown successfully.")

    def shutdown_system(self):
        # Thực hiện tắt hệ thống máy chủ.
        try:
            # Gọi lệnh hệ thống để tắt máy chủ ngay lập tức.
            subprocess.call("shutdown /s /t 0", shell=True)
        except Exception as e:
            # Xử lý ngoại lệ nếu có lỗi xảy ra trong quá trình tắt máy chủ
            # và hiển thị thông báo lỗi.
            messagebox.showerror("Shutdown Error", f"Error shutting down system: {str(e)}")

    def start(self):
        # Bắt đầu vòng lặp chính của giao diện Tkinter.
        self.window.mainloop()

# Script chạy
if __name__ == "__main__":
    # Kiểm tra nếu mã được chạy trực tiếp (không được import bởi một tệp khác)
    
    # Tạo một đối tượng ServerShutdownWindow để quản lý cửa sổ tắt máy của máy chủ.
    root = tk.Tk()  # Tạo một cửa sổ giao diện người dùng mới bằng thư viện tkinter.
    server_shutdown_window = ServerShutdownWindow(root)  # Khởi tạo đối tượng ServerShutdownWindow với cửa sổ giao diện người dùng vừa tạo.
    server_shutdown_window.start()  # Bắt đầu hiển thị cửa sổ thông báo tắt máy của máy chủ.
    root.mainloop()  # Chạy vòng lặp chính của giao diện người dùng để duy trì hiển thị và phản hồi các sự kiện.
