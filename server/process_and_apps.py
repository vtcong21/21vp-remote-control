import subprocess
import json

class ProcessManager:
    @staticmethod
    def get_running_processes():
        try:
            # Sử dụng PowerShell để lấy thông tin về các tiến trình và số luồng
            powershell_command = "Get-Process | Select-Object ProcessName, Id, Threads | ConvertTo-Json"
            result = subprocess.run(["powershell", "-Command", powershell_command], capture_output=True, text=True, check=True)

            # Phân tích kết quả JSON
            processes = json.loads(result.stdout)

            # Tạo danh sách mới chứa thông tin về số luồng của từng tiến trình
            process_list = []

            for process in processes:
                process_name = process['ProcessName']
                pid = process['Id']
                thread_count = len(process['Threads'])

                # Thêm thông tin vào danh sách mới
                process_list.append({'ProcessName': process_name, 'PID': pid, 'ThreadCount': thread_count})

            return process_list

        except subprocess.CalledProcessError as e:
            print(f"Lỗi: {e}")
            return []

    @staticmethod
    def kill_process(pid):
        try:
            # Sử dụng subprocess để kết thúc tiến trình bằng PID
            command = f"Stop-Process -Id {pid}"
            result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, check=True)

            if result.returncode == 0:
                return f"Tiến trình với PID {pid} đã bị kết thúc."
            else:
                error_message = f"Lỗi khi kết thúc tiến trình với PID {pid}: {result.stderr}"
                print(error_message)
                return error_message

        except subprocess.CalledProcessError as e:
            error_message = f"Lỗi khi kết thúc tiến trình với PID {pid}: {str(e)}"
            print(error_message)
            return error_message

    @staticmethod
    def start_process(name):
        try:
            # Sử dụng subprocess để khởi chạy ứng dụng bằng tên ứng dụng
            command = f"Start-Process {name}"
            result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, check=True)

            if result.returncode == 0:
                return f"{name} đã được khởi chạy."
            else:
                error_message = f"Lỗi khi khởi chạy {name}: {result.stderr}"
                print(error_message)
                return error_message

        except subprocess.CalledProcessError as e:
            error_message = f"Lỗi khi khởi chạy {name}: {str(e)}"
            print(error_message)
            return error_message

class AppManager:
    @staticmethod
    def get_running_applications():
        try:
            # Sử dụng PowerShell để lấy thông tin về các tiến trình và số luồng
            powershell_command = "Get-Process | Where-Object { $_.MainWindowTitle -ne '' } | Select-Object ProcessName, Id, Threads | ConvertTo-Json"
            result = subprocess.run(["powershell", "-Command", powershell_command], capture_output=True, text=True, check=True)

            # Phân tích kết quả JSON
            processes = json.loads(result.stdout)

            # Tạo danh sách mới chứa thông tin về số luồng của từng tiến trình
            app_list = []

            for process in processes:
                process_name = process['ProcessName']
                pid = process['Id']
                thread_count = len(process['Threads'])

                # Thêm thông tin vào danh sách mới
                app_list.append({'ProcessName': process_name, 'PID': pid, 'ThreadCount': thread_count})

            return app_list

        except subprocess.CalledProcessError as e:
            print(f"Lỗi: {e}")
            return []