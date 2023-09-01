from screenshot import Screenshot
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from io import BytesIO
class ScreenshotUI(Screenshot):
    def __init__(self, socket, window):
        super().__init__(socket, window)
        self.frame = None
        self.screenshot_window = None
        self.screenshot_label = None
        self.screenshot_image = None
        self.screenshot_data = None


    # Gửi yêu cầu chụp màn hình tới server
        self.send_message("screenshot")
        # Nhận dữ liệu hình ảnh đã chụp từ server
        self.screenshot_data = self.receive_screenshot()
        if self.screenshot_data:
            try:
                self.screenshot_img = Image.open(BytesIO(self.screenshot_data))
                # Thay đổi kích thước hình ảnh để thu nhỏ
                width, height = self.screenshot_img.size
                new_width = 400  # Độ rộng mới
                new_height = (height * new_width) // width
                self.screenshot_img.thumbnail((new_width, new_height))

                # Tạo cửa sổ mới để hiển thị hình ảnh
                self.screenshot_window = tk.Toplevel(self.window)
                self.screenshot_window.geometry("420x285")
                self.screenshot_window.title("Screenshot")

                # Tạo một Frame trong cửa sổ mới để bố trí hình ảnh
                self.frame = tk.Frame(self.screenshot_window)
                self.frame.pack()

                # Hiển thị hình ảnh thu nhỏ trong cửa sổ mới
                self.screenshot_image = ImageTk.PhotoImage(self.screenshot_img)
                self.screenshot_label = tk.Label(self.frame, image=self.screenshot_image)
                self.screenshot_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)  # Hiển thị hình ảnh ở hàng 0, cột 0 và 1

                # Tạo nút "Chụp" và "Lưu" trong cửa sổ mới
                # capture_button = tk.Button(self.frame, text="Chụp", command=lambda: self.capture_screenshot())
                # save_button = tk.Button(self.frame, text="Lưu", command=self.save_screenshot)

                capture_button = tk.Button(self.screenshot_window, text="Chụp", command=lambda:self.capture_screenshot(), width=33, height=1)
                capture_button.place(x=10, y=245)
                save_button = tk.Button(self.screenshot_window, text="Lưu", command=self.save_screenshot, width=19, height=1)
                save_button.place(x=264, y=245)

                # Đặt cùng độ rộng cho cả nút "Chụp" và nút "Lưu"
                # capture_button.grid(row=1, column=0, padx=10, pady=10)
                # save_button.grid(row=1, column=1, padx=10, pady=10)

                # Đặt các cột có cùng độ rộng để nút "Chụp" và nút "Lưu" có kích thước bằng nhau
                self.frame.columnconfigure(0, weight=1)
                self.frame.columnconfigure(1, weight=1)


            except Exception as e:
                print(f"Lỗi khi hiển thị hình ảnh: {str(e)}")

    def capture_screenshot(self):
        # Gửi lại yêu cầu chụp màn hình để cập nhật hình ảnh
        self.send_message("screenshot")
        # Nhận dữ liệu hình ảnh đã chụp từ server
        self.screenshot_data = self.receive_screenshot()
        if self.screenshot_data:
            try:
                self.screenshot_img = Image.open(BytesIO(self.screenshot_data))
                # Thay đổi kích thước hình ảnh để thu nhỏ
                width, height = self.screenshot_img.size
                new_width = 400  # Độ rộng mới
                new_height = (height * new_width) // width
                self.screenshot_img.thumbnail((new_width, new_height))

                # Cập nhật hình ảnh trong label hiện tại
                self.screenshot_image = ImageTk.PhotoImage(self.screenshot_img)
                self.screenshot_label.configure(image=self.screenshot_image)

            except Exception as e:
                print(f"Lỗi khi hiển thị hình ảnh: {str(e)}")

    def receive_screenshot(self):
        try:
            screenshot_size = int(self.socket.recv(1024))
            screenshot_data = b""
            while screenshot_size > 0:
                chunk = self.socket.recv(4096)
                screenshot_data += chunk
                screenshot_size -= len(chunk)
            return screenshot_data
        except Exception as e:
            print(f"Lỗi khi nhận hình ảnh màn hình: {str(e)}")
            return None

    def save_screenshot(self):
        # Lưu hình ảnh đã chụp vào tệp
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            try:
                with open(file_path, "wb") as file:
                    file.write(self.screenshot_data)
                    messagebox.showinfo("Thông báo", "Hình ảnh đã được lưu thành công.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi lưu hình ảnh: {str(e)}")

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