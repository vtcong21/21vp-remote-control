import threading
from tkinter import Tk, Button, messagebox
from server import Server

class ServerUI:
    def __init__(self, root):
        self.root = root
        self.server = Server()
        self.start_button = Button(root, text="Start Server", command=self.start_server)
        self.start_button.pack()

        # Xử lý sự kiện đóng cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    def start_server(self):
        self.start_button.config(state="disabled")  # Disable nút Start khi server đã được khởi động
        server_thread = threading.Thread(target=self.server.start_server)
        server_thread.start()

        messagebox.showinfo("Server", "Server đã được khởi động!")

    def close_window(self):
        if messagebox.askokcancel("Đóng Server", "Bạn có chắc chắn muốn đóng Server?"):
            self.server.stop_server()
            self.root.destroy()

# Script chạy
if __name__ == "__main__":
    root = Tk()
    server_ui = ServerUI(root)
    root.mainloop()