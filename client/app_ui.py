from app import Applications
import tkinter as tk
from tkinter import ttk
import json

class AppUI(Applications):
    def __init__(self, socket, window):
        super().__init__(socket, window)

        # Tạo cửa sổ mới để hiển thị chức năng
        self.app_window = tk.Toplevel(self.window)
        self.app_window.geometry("400x90")
        self.app_window.title("List Applications")

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
        
        columns = ("Name Application", "ID Application", "Count Thread")
        self.app_tree = ttk.Treeview(self.app_window, columns=columns, show="headings")
        self.app_tree.configure(height=11)  # Đặt số dòng hiển thị là 15, thay đổi theo ý muốn
        
        # Đặt độ rộng cột và tiêu đề cho các cột
        column_widths = {"Name Application": 185, "ID Application": 100, "Count Thread": 80}
        for col in columns:
            self.app_tree.heading(col, text=col)
            self.app_tree.column(col, width=column_widths[col])
        self.app_tree.place(x=16, y=86)
        
        scrollbar = tk.Scrollbar(self.app_window, command=self.app_tree.yview)
        scrollbar.place(x=382, y=86, height=245)
        self.app_tree.config(yscrollcommand=scrollbar.set)

        self.send_message("apps")
        app_data = self.receive_processus_data()

        if app_data:
            try:
                app_list = json.loads(app_data)
                
                for app_info in app_list:
                    app_name = app_info.get("ProcessName", "N/A")
                    app_id = str(app_info.get("PID", "N/A"))
                    thread_count = str(app_info.get("ThreadCount", "N/A"))
                    self.process_tree.insert("", "end", values=(app_name, app_id, thread_count))
                    
            except Exception as e:
                print(f"Lỗi khi hiển thị thông tin tiến trình: {str(e)}")


    def kill_button_click(self):
        self.create_input_window("Kill Application", "Enter ID", "Kill")


    def start_button_click(self):
        self.create_input_window("Start Application", "Enter Name", "Start")


    def clear_button_click(self):
        self.app_tree.delete(*self.app_tree.get_children())


    def create_input_window(self, title, entry_text, request):
        self.child_window = tk.Toplevel(self.window)
        self.child_window.geometry("390x60")
        self.child_window.title(title)

        self.input_entry = tk.Entry(self.child_window)
        self.input_entry.place(relx=0.05, rely=0.3, relwidth=0.65, relheight=0.45)
        self.input_entry.insert(0, entry_text)
        self.input_entry.config(fg="gray")  
        self.input_entry.bind("<FocusIn>", lambda event: self.on_entry_click(entry_text))
        self.input_entry.bind("<FocusOut>", lambda event: self.on_focus_out(entry_text))

        self.input_button = tk.Button(self.child_window, text=request, command=lambda: self.send_request(self.input_entry, request))
        self.input_button.place(relx=0.73, rely=0.3, relwidth=0.22, relheight=0.45)


    def send_request(self, data_input, request):
        value = data_input.get()
        if value:
            if request == "Kill":
                self.send_message(f"kill {value}")
            elif request == "Start":
                self.send_message(f"start {value}")

            # Nhận phản hồi từ máy chủ
            response = self.receive_message()
            print(response)  # In phản hồi ra màn hình


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

    
    def on_entry_click(self, default_text):
        if self.input_entry.get() == default_text:
            self.input_entry.delete(0, "end")  # Xóa nội dung hiện tại
            self.input_entry.config(fg="black")  # Đổi màu văn bản thành đen

    def on_focus_out(self, default_text):
        if not self.input_entry.get():
            self.input_entry.insert(0, default_text)
            self.input_entry.config(fg="gray")

    
    def receive_processus_data(self):
        try:
            app_data = ""
            while True:
                chunk = self.socket.recv(1024).decode()
                app_data += chunk
                
                if app_data.endswith("done"):
                    app_data = app_data[:-4]  # Loại bỏ chuỗi "done" ở cuối
                    break

            return app_data

        except Exception as e:
            print(f"Error receiving processus data: {e}")
            return ""
        

    def receive_message(self):
        if not self.socket:
            print("Not connected to the server.")
            return None
        try:
            # Nhận dữ liệu từ máy chủ
            received_data = self.socket.recv(1024)
            return received_data.decode('utf-8')
        except Exception as e:
            print(f"Lỗi khi nhận dữ liệu: {str(e)}")
            return None