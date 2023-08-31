from process import Processes
import tkinter as tk
from tkinter import ttk
import json

class ProcessUI(Processes):
    def __init__(self, socket, window):
        super().__init__(socket, window)

        # Tạo cửa sổ mới để hiển thị chức năng
        self.process_window = tk.Toplevel(self.window)
        self.process_window.geometry("400x90")
        self.process_window.title("List Processes")

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
        
        columns = ("Name Process", "ID Process", "Count Thread")
        self.process_tree = ttk.Treeview(self.process_window, columns=columns, show="headings")
        self.process_tree.configure(height=11)  # Đặt số dòng hiển thị là 15, thay đổi theo ý muốn
        
        # Đặt độ rộng cột và tiêu đề cho các cột
        column_widths = {"Name Process": 185, "ID Process": 100, "Count Thread": 80}
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=column_widths[col])
        self.process_tree.place(x=16, y=86)
        
        scrollbar = tk.Scrollbar(self.process_window, command=self.process_tree.yview)
        scrollbar.place(x=382, y=86, height=245)
        self.process_tree.config(yscrollcommand=scrollbar.set)

        self.send_message("processus")
        processus_data = self.receive_processus_data()

        if processus_data:
            try:
                process_list = json.loads(processus_data)
                
                for process_info in process_list:
                    process_name = process_info.get("ProcessName", "N/A")
                    process_id = str(process_info.get("PID", "N/A"))
                    thread_count = str(process_info.get("ThreadCount", "N/A"))
                    self.process_tree.insert("", "end", values=(process_name, process_id, thread_count))
                    
            except Exception as e:
                print(f"Error displaying progress information: {str(e)}")


    def kill_button_click(self):
        self.create_input_window("Kill Process", "Enter ID", "Kill")


    def start_button_click(self):
        self.create_input_window("Start Process", "Enter Name", "Start")


    def clear_button_click(self):
        self.process_tree.delete(*self.process_tree.get_children())


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
            process_data = ""
            while True:
                chunk = self.socket.recv(1024).decode()
                process_data += chunk

                if process_data.endswith("done"):
                    process_data = process_data[:-4]  # Loại bỏ chuỗi "done" ở cuối
                    break

            return process_data
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