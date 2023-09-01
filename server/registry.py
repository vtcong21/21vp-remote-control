import subprocess
class RegistryManager:
    @staticmethod
    def get_registry_value(key_path, value_name):
        try:
            # Sử dụng subprocess để chạy reg query để lấy giá trị từ Registry
            command = f'reg query "{key_path}" /v "{value_name}"'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                return result.stdout
            else:
                error_message = f"Lỗi khi lấy giá trị Registry: {result.stderr}"
                print(error_message)
                return error_message
        except Exception as e:
            error_message = f"Lỗi khi lấy giá trị Registry: {str(e)}"
            print(error_message)
            return error_message

    @staticmethod
    def set_registry_value(key_path, value_name, value_data, value_type):
        try:
            # Sử dụng subprocess để chạy reg add để thiết lập giá trị trong Registry
            command = f'reg add "{key_path}" /v "{value_name}" /d "{value_data}" /t {value_type} /f'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                return f"Giá trị Registry {value_name} đã được thiết lập thành công."
            else:
                error_message = f"Lỗi khi thiết lập giá trị Registry: {result.stderr}"
                print(error_message)
                return error_message
        except Exception as e:
            error_message = f"Lỗi khi thiết lập giá trị Registry: {str(e)}"
            print(error_message)
            return error_message

    @staticmethod
    def delete_registry_value(key_path, value_name):
        try:
            # Sử dụng subprocess để chạy reg delete để xóa giá trị khỏi Registry
            
            command = f'reg delete "{key_path}" /v "{value_name}" /f'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                return f"Giá trị Registry {value_name} đã được xóa thành công."
            else:
                error_message = f"Lỗi khi xóa giá trị Registry: {result.stderr}"
                print(error_message)
                return error_message
        except Exception as e:
            error_message = f"Lỗi khi xóa giá trị Registry: {str(e)}"
            print(error_message)
            return error_message

    @staticmethod
    def create_registry_key(key_path):
        try:
            # Sử dụng subprocess để chạy reg add để tạo khóa trong Registry
            command = f'reg add "{key_path}" /f'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                return f"Khóa Registry {key_path} đã được tạo thành công."
            else:
                error_message = f"Lỗi khi tạo khóa Registry: {result.stderr}"
                print(error_message)
                return error_message
        except Exception as e:
            error_message = f"Lỗi khi tạo khóa Registry: {str(e)}"
            print(error_message)
            return error_message

    @staticmethod
    def delete_registry_key(key_path):
        try:
            print(key_path)
            # Sử dụng subprocess để chạy reg delete để xóa khóa khỏi Registry
            command = f'reg delete "{key_path}" /f'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                return f"Khóa Registry {key_path} đã được xóa thành công."
            else:
                error_message = f"Lỗi khi xóa khóa Registry: {result.stderr}"
                print(error_message)
                return error_message
        except Exception as e:
            error_message = f"Lỗi khi xóa khóa Registry: {str(e)}"
            print(error_message)
            return error_message
    @staticmethod
    def apply_registry_patch(patch_file_path):
        try:
            # Sử dụng subprocess để chạy regedit để áp dụng patch Registry
            command = f'regedit /s "{patch_file_path}"'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                return "Registry patch applied successfully."
            else:
                return result.stderr
        except Exception as e:
            return f"Error applying registry patch: {str(e)}"