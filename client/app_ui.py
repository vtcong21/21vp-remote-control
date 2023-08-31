from app import Application
import tkinter as tk
from tkinter import ttk
import json

class AppUI(Application):
    def __init__(self, socket, window):
        super().__init__(socket, window)

        # Tạo cửa sổ mới để hiển thị chức năng
        self.app_window = tk.Toplevel(self.window)
        self.app_window.geometry("400x90")
        self.app_window.title("List App")

        # Tạo các nút "Kill", "Xem danh sách", "Xóa" và "Bắt đầu"
        self.kill_button = tk.Button(self.app_window, text="Kill", command=self.kill_button_click, width=11, height=3)
        self.kill_button.place(x=16, y=16)
        self.view_list_button = tk.Button(self.app_window, text="Show\nlist", command=self.show_list_button_click, width=11, height=3)
        self.view_list_button.place(x=110, y=16)
        self.delete_button = tk.Button(self.app_window, text="Clear", command=self.clear_button_click, width=11, height=3)
        self.delete_button.place(x=204, y=16)
        self.start_button = tk.Button(self.app_window, text="Start", command=self.start_button_click, width=11, height=3)
        self.start_button.place(x=298, y=16)


    def show_list_button_click(self):
        self.app_window.geometry("400x350")
        
        columns = ("ProcessName", "ProcessID", "ThreadCount")
        self.app_tree = ttk.Treeview(self.app_window, columns=columns, show="headings")
        self.app_tree.configure(height=11)  # Đặt số dòng hiển thị là 15, thay đổi theo ý muốn
        
        # Đặt độ rộng cột và tiêu đề cho các cột
        column_widths = {"ProcessName": 185, "ProcessID": 100, "ThreadCount": 80}
        for col in columns:
            self.app_tree.heading(col, text=col)
            self.app_tree.column(col, width=column_widths[col])
        self.app_tree.place(x=16, y=86)
        
        scrollbar = tk.Scrollbar(self.app_window, command=self.app_tree.yview)
        scrollbar.place(x=382, y=86, height=245)
        self.app_tree.config(yscrollcommand=scrollbar.set)

        self.send_message("apps")
        self.app_data = self.receive_processus_data()

        if self.app_data:
            try:
                self.app_list = json.loads(self.app_data)
                
                for app_info in self.app_list:
                    app_name = app_info.get("ProcessName", "N/A")
                    app_id = str(app_info.get("PID", "N/A"))
                    thread_count = str(app_info.get("ThreadCount", "N/A"))
                    self.process_tree.insert("", "end", values=(app_name, app_id, thread_count))
                    
            except Exception as e:
                print(f"Lỗi khi hiển thị thông tin tiến trình: {str(e)}")


    def kill_button_click(self):
        # Tạo cửa sổ mới
        self.kill_app_window = tk.Toplevel(self.window)
        self.kill_app_window.geometry("390x60")
        self.kill_app_window.title("Kill Process")

        self.app_id_input = tk.Entry(self.kill_app_window)
        self.app_id_input.place(relx=0.05, rely=0.3, relwidth=0.65, relheight=0.45)
     
        self.app_id_input.insert(0, "Enter Process ID")
        self.app_id_input.config(fg="gray")  
        self.app_id_input.bind("<FocusIn>", self.kill_on_entry_click)
        self.app_id_input.bind("<FocusOut>", self.kill_on_focus_out)

        self.kill_app_button = tk.Button(self.kill_app_window, text="Kill", command=self.send_kill_request)
        self.kill_app_button.place(relx=0.73, rely=0.3, relwidth=0.22, relheight=0.45)


    def clear_button_click(self):
        self.app_tree.delete(*self.process_tree.get_children())

    def start_button_click(self):
        # Tạo cửa sổ mới
        self.start_app_window = tk.Toplevel(self.window)
        self.start_app_window.geometry("390x60")
        self.start_app_window.title("Start Process")

        self.app_name_input = tk.Entry(self.start_app_window)
        self.app_name_input.place(relx=0.05, rely=0.3, relwidth=0.65, relheight=0.45)
     
        self.app_name_input.insert(0, "Enter Process Name")
        self.app_name_input.config(fg="gray")  
        self.app_name_input.bind("<FocusIn>", self.start_on_entry_click)
        self.app_name_input.bind("<FocusOut>", self.start_on_focus_out)

        self.start_app_button = tk.Button(self.start_app_window, text="Start", command=self.send_start_request)
        self.start_app_button.place(relx=0.73, rely=0.3, relwidth=0.22, relheight=0.45)

    def send_kill_request(self):
        app_id = self.app_id_input.get()
        if app_id:
            # Gửi yêu cầu kết thúc quy trình đến máy chủ
            self.send_message(f"kill {app_id}")
    
    def send_start_request(self):
        app_name = self.app_name_input.get()
        if app_name:
            # Gửi yêu cầu kết thúc quy trình đến máy chủ
            self.send_message(f"start {app_name}")

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
    
    def kill_on_entry_click(self, event):
        if self.app_id_input.get() == "Enter Process ID":
            self.app_id_input.delete(0, "end")  # Xóa nội dung hiện tại
            self.app_id_input.config(fg="black")  # Đổi màu văn bản thành đen

    def kill_on_focus_out(self, event):
        if not self.app_id_input.get():
            self.app_id_input.insert(0, "Enter Process ID")
            self.app_id_input.config(fg="gray")
    
    def start_on_entry_click(self, event):
        if self.app_name_input.get() == "Enter Process Name":
            self.app_name_input.delete(0, "end")  # Xóa nội dung hiện tại
            self.app_name_input.config(fg="black")  # Đổi màu văn bản thành đen

    def start_on_focus_out(self, event):
        if not self.app_name_input.get():
            self.app_name_input.insert(0, "Enter Process Name")
            self.app_name_input.config(fg="gray")
    
    def receive_processus_data(self):
        try:
            app_data = ""
            while True:
                chunk = self.socket.recv(1024).decode()
                if chunk == "done":
                    break
                app_data += chunk

            return app_data

        except Exception as e:
            print(f"Error receiving processus data: {e}")
            return ""