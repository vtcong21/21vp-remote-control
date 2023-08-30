# from process import Processes
import tkinter as tk
# from tkinter import messagebox, filedialog
# from PIL import Image, ImageTk
# from io import BytesIO

class ProcessUI():
    def _init_(self):
        # Tạo cửa sổ mới để hiển thị chức năng
        process_window = tk.Toplevel(self.window)
        process_window.title("Các Tiến Trình Hoạt Động")

        # Tạo các nút "Kill", "Xem danh sách", "Xóa" và "Bắt đầu"
        kill_button = tk.Button(process_window, text="Kill", command=self.kill_button_click)
        view_list_button = tk.Button(process_window, text="Xem danh sách", command=self.view_list_button_click)
        delete_button = tk.Button(process_window, text="Xóa", command=self.delete_button_click)
        start_button = tk.Button(process_window, text="Bắt đầu", command=self.start_button_click)
        
        kill_button.pack()
        view_list_button.pack()
        delete_button.pack()
        start_button.pack()