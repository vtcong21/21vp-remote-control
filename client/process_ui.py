from process import Processes
import tkinter as tk
from tkinter import Frame
from PIL import Image, ImageTk
from io import BytesIO
import json

class ProcessUI(Processes):
    def __init__(self, socket, window):
        super().__init__(socket, window)

        # Tạo cửa sổ mới để hiển thị chức năng
        self.process_window = tk.Toplevel(self.window)
        self.process_window.geometry("400x90")
        self.process_window.title("List Process")

        # Tạo các nút "Kill", "Xem danh sách", "Xóa" và "Bắt đầu"
        self.kill_button = tk.Button(self.process_window, text="Kill", command=self.kill_button_click, width=11, height=3)
        self.kill_button.place(x=16, y=16)
        self.view_list_button = tk.Button(self.process_window, text="Show\nlist", command=self.show_list_button_click, width=11, height=3)
        self.view_list_button.place(x=110, y=16)
        self.delete_button = tk.Button(self.process_window, text="Clear", command=self.clear_button_click, width=11, height=3)
        self.delete_button.place(x=204, y=16)
        self.start_button = tk.Button(self.process_window, text="Start", command=self.start_button_click, width=11, height=3)
        self.start_button.place(x=298, y=16)


    def show_list_button_click(self):
        self.process_window.geometry("400x350")
        
        self.process_listbox = tk.Listbox(self.process_window, width=61, height=15)
        self.process_listbox.place(x=16, y=86)  

        # Tạo một thanh cuộn dọc và liên kết nó với Listbox
        scrollbar = tk.Scrollbar(self.process_window, command=self.process_listbox.yview)
        scrollbar.place(x=370, y=86, height=14*18)  # Đặt vị trí và chiều cao tương ứng với Listbox
        # Cài đặt thanh cuộn cho Listbox
        self.process_listbox.config(yscrollcommand=scrollbar.set)

        self.send_message("processus")  # Truyền socket vào hàm send_message
        self.process_data = self.receive_processus_data()  # Truyền socket vào hàm receive_processus_data

        if self.process_data:
            try:
                self.process_list = json.loads(self.process_data)
                # Tạo đầu cột
                header_row = "ProcessName".ljust(30) + "PID".ljust(15) + "ThreadCount"
                self.process_listbox.insert(tk.END, header_row)
                
                for self.process_info in self.process_list:
                    self.process_name = self.process_info.get("ProcessName", "N/A")
                    self.process_id = str(self.process_info.get("PID", "N/A")).ljust(15)
                    self.thread_count = str(self.process_info.get("ThreadCount", "N/A"))
                    self.formatted_row = self.process_name.ljust(30) + self.process_id + self.thread_count
                    self.process_listbox.insert(tk.END, self.formatted_row)

            except Exception as e:
                print(f"Lỗi khi hiển thị thông tin tiến trình: {str(e)}")


    def kill_button_click(self):
        # Tạo cửa sổ mới
        self.kill_process_window = tk.Toplevel(self.window)
        self.kill_process_window.geometry("390x60")
        self.kill_process_window.title("Kill Process")

        self.process_id_input = tk.Entry(self.kill_process_window)
        self.process_id_input.place(relx=0.05, rely=0.3, relwidth=0.65, relheight=0.45)
     
        self.process_id_input.insert(0, "Enter Process ID")
        self.process_id_input.config(fg="gray")  
        self.process_id_input.bind("<FocusIn>", self.kill_on_entry_click)
        self.process_id_input.bind("<FocusOut>", self.kill_on_focus_out)

        self.kill_process_button = tk.Button(self.kill_process_window, text="Kill", command=self.send_kill_request)
        self.kill_process_button.place(relx=0.73, rely=0.3, relwidth=0.22, relheight=0.45)


    def clear_button_click(self):
        self.process_listbox.delete(0, tk.END)

    def start_button_click(self):
        # Tạo cửa sổ mới
        self.start_process_window = tk.Toplevel(self.window)
        self.start_process_window.geometry("390x60")
        self.start_process_window.title("Start Process")

        self.start_name_input = tk.Entry(self.start_process_window)
        self.start_name_input.place(relx=0.05, rely=0.3, relwidth=0.65, relheight=0.45)
     
        self.start_name_input.insert(0, "Enter Process Name")
        self.start_name_input.config(fg="gray")  
        self.start_name_input.bind("<FocusIn>", self.start_on_entry_click)
        self.start_name_input.bind("<FocusOut>", self.start_on_focus_out)

        self.start_process_button = tk.Button(self.start_process_window, text="Start", command=self.send_start_request)
        self.start_process_button.place(relx=0.73, rely=0.3, relwidth=0.22, relheight=0.45)

    def send_kill_request(self):
        process_id = self.process_id_input.get()
        if process_id:
            # Gửi yêu cầu kết thúc quy trình đến máy chủ
            self.send_message(f"kill {process_id}")
    
    def send_start_request(self):
        start_id = self.start_name_entry.get()
        if start_id:
            # Gửi yêu cầu kết thúc quy trình đến máy chủ
            self.send_message(f"start {start_id}")

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
    
    # def receive_message(self):
    #     # Triển khai logic nhận dữ liệu từ máy chủ ở đây
    #     # Ví dụ: Sử dụng socket để nhận dữ liệu từ máy chủ
    #     try:
    #         received_data = self.socket.recv(1024)
    #         return received_data.decode('utf-8')
    #     except Exception as e:
    #         print(f"Lỗi khi nhận dữ liệu: {str(e)}")
    #         return None
    
    def kill_on_entry_click(self, event):
        if self.process_id_input.get() == "Enter Process ID":
            self.process_id_input.delete(0, "end")  # Xóa nội dung hiện tại
            self.process_id_input.config(fg="black")  # Đổi màu văn bản thành đen

    def kill_on_focus_out(self, event):
        if not self.process_id_input.get():
            self.process_id_input.insert(0, "Enter Process ID")
            self.process_id_input.config(fg="gray")
    
    def start_on_entry_click(self, event):
        if self.start_name_input.get() == "Enter Process Name":
            self.start_name_input.delete(0, "end")  # Xóa nội dung hiện tại
            self.start_name_input.config(fg="black")  # Đổi màu văn bản thành đen

    def start_on_focus_out(self, event):
        if not self.start_name_input.get():
            self.start_name_input.insert(0, "Enter Process Name")
            self.start_name_input.config(fg="gray")
    
    def receive_processus_data(self):
        try:
            process_data = ""
            while True:
                chunk = self.socket.recv(1024).decode()
                if chunk == "done":
                    break
                process_data += chunk

            return process_data

        except Exception as e:
            print(f"Error receiving processus data: {e}")
            return ""