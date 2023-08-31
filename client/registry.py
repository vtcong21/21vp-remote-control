class Registry:
    def __init__(self, socket, window):
        self.window = window
        self.socket = socket
    
    def get_value(self, key_path, value_name):
        request = f"get {key_path} {value_name}"
        response = self.send_request(request)
        return response
    
    def set_value(self, key_path, value_name, value_data, value_type):
        request = f"set {key_path} {value_name} {value_data} {value_type}"
        response = self.send_request(request)
        return response
    
    def delete_value(self, key_path, value_name):
        request = f"delete {key_path} {value_name}"
        response = self.send_request(request)
        return response
    
    def create_key(self, key_path):
        request = f"create_key {key_path}"
        response = self.send_request(request)
        return response
    
    def delete_key(self, key_path):
        request = f"delete_key {key_path}"
        response = self.send_request(request)
        return response
    
    def send_request(self, request):
        # Gửi yêu cầu tới server thông qua socket
        self.socket.sendall(request.encode())
        
        # Nhận và trả về phản hồi từ server
        response = self.socket.recv(1024).decode()
        return response