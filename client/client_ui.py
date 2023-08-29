import tkinter as tk
from tkinter import messagebox
from client import Client
from keylogger_ui import KeyloggerUI
from screenshot_ui import ScreenshotUI
import socket

class ClientUI(Client):
    def __init__(self):
        super().__init__()

        self.window = tk.Tk()
        self.window.title("Client")
        self.window.geometry("400x300")
        self.keyloggerUI = None
        self.screenshotUI = None


        self.server_ip_label = tk.Label(self.window, text="Enter IP Address:")
        self.server_ip_label.pack()

        self.server_ip_entry = tk.Entry(self.window)
        self.server_ip_entry.pack()

        self.connect_button = tk.Button(self.window, text="Connect", command=self.connect_button_click)
        self.connect_button.pack()

    def connect_button_click(self):
        server_ip = self.server_ip_entry.get()
        try:
            self.connect_to_server(server_ip)
            if self.socket:
                self.render_home_window()
        except socket.gaierror:
            error_message = "Không thể kết nối tới server. Vui lòng kiểm tra địa chỉ IP và thử lại."
            self.show_error_message(error_message)
        except Exception as e:
            error_message = "Lỗi xảy ra: " + str(e)
            self.show_error_message(error_message)

    def quit_button_click(self):
        self.disconnect_from_server()
        self.window.quit()
    def run(self):
        self.window.mainloop()

    def show_error_message(self, message):
        messagebox.showerror("Lỗi", message)

    def render_home_window(self):
        if hasattr(self, "server_ip_label"):
            self.server_ip_label.destroy()
            self.server_ip_entry.destroy()
            self.connect_button.destroy()
        self.process_button = tk.Button(self.window, text="Running Processes")
        self.process_button.pack()
        #running apps
        self.app_button = tk.Button(self.window, text="Running Applications", command= self.running_app_button_click)
        self.app_button.pack()
        #keylog
        self.keystroke_button = tk.Button(self.window, text="Keystroke", command=self.keystroke_button_click)
        self.keystroke_button.pack()
        #shutdown
        self.shutdown_button = tk.Button(self.window, text="Shutdown")
        self.shutdown_button.pack()
        #screenshot
        self.screenshot_button = tk.Button(self.window, text="Take Screenshot", command=self.take_screenshot_button_click)
        self.screenshot_button.pack()
        #quit
        self.quit_button = tk.Button(self.window, text="Quit", command=self.quit_button_click)
        self.quit_button.pack()
    def running_app_button_click(self):
        pass
    def shutdown_button_click(self):
        pass
    def quit_button_click(self):
        pass
    def keystroke_button_click(self):
        self.keyloggerUI = KeyloggerUI(self.socket, self.window)
    def take_screenshot_button_click(self):
        self.screenshotUI = ScreenshotUI(self.socket, self.window)
    #     # Gửi yêu cầu chụp màn hình tới server
    #     self.send_message("screenshot")
    #     # Nhận dữ liệu hình ảnh đã chụp từ server
    #     self.screenshot_data = self.receive_screenshot()
    #     if self.screenshot_data:
    #         try:
    #             screenshot = Image.open(BytesIO(self.screenshot_data))

    #             # Thay đổi kích thước hình ảnh để thu nhỏ
    #             width, height = screenshot.size
    #             new_width = 400  # Độ rộng mới
    #             new_height = (height * new_width) // width
    #             screenshot.thumbnail((new_width, new_height))

    #             # Tạo cửa sổ mới để hiển thị hình ảnh
    #             screenshot_window = tk.Toplevel(self.window)
    #             screenshot_window.title("Screenshot")

    #             # Tạo một Frame trong cửa sổ mới để bố trí hình ảnh
    #             frame = tk.Frame(screenshot_window)
    #             frame.pack()

    #             # Hiển thị hình ảnh thu nhỏ trong cửa sổ mới
    #             self.screenshot_image = ImageTk.PhotoImage(screenshot)
    #             screenshot_label = tk.Label(frame, image=self.screenshot_image)
    #             screenshot_label.grid(row=0, column=0)

            
    #             # Tạo nút "Chụp" và "Lưu" trong cửa sổ mới
    #             capture_button = tk.Button(frame, text="Chụp", command=lambda: self.capture_screenshot(screenshot_window))
    #             save_button = tk.Button(frame, text="Lưu", command=self.save_screenshot)  # Thay đổi ở đây
    #             capture_button.grid(row=1, column=0)
    #             save_button.grid(row=1, column=1)


    #         except Exception as e:
    #             print(f"Lỗi khi hiển thị hình ảnh: {str(e)}")

    # def capture_screenshot(self, screenshot_window):
    #     # Gửi lại yêu cầu chụp màn hình để cập nhật hình ảnh
    #     self.send_message("screenshot")
        
    #     # Nhận dữ liệu hình ảnh đã chụp từ server
    #     self.screenshot_data = self.receive_screenshot()
    #     if self.screenshot_data:
    #         try:
    #             screenshot = Image.open(BytesIO(self.screenshot_data))

    #             # Cập nhật hình ảnh hiển thị trong cửa sổ chụp màn hình
    #             self.screenshot_image = ImageTk.PhotoImage(screenshot)
    #             screenshot_window.configure(image=self.screenshot_image)

    #         except Exception as e:
    #             print(f"Lỗi khi hiển thị hình ảnh: {str(e)}")


    # def save_screenshot(self):
    #     # Lưu hình ảnh đã chụp vào tệp
    #     file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    #     if file_path:
    #         try:
    #             with open(file_path, "wb") as file:
    #                 file.write(self.screenshot_data)
    #                 messagebox.showinfo("Thông báo", "Hình ảnh đã được lưu thành công.")
    #         except Exception as e:
    #             messagebox.showerror("Lỗi", f"Lỗi khi lưu hình ảnh: {str(e)}")
    def shutdown_button_click(self):
        pass
    def processes_button_click(self):
        pass
    def apps_button_click(self):
        pass

# Script chạy
if __name__ == "__main__":
    client_ui = ClientUI()
    client_ui.run()
