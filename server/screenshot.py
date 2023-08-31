import io
from PIL import ImageGrab

class Screenshot:
    @staticmethod
    def capture_screenshot():
        try:
            # Chụp màn hình bằng cách sử dụng phương thức grab() từ thư viện ImageGrab
            screenshot = ImageGrab.grab()

            # Tạo một đối tượng BytesIO để lưu trữ dữ liệu hình ảnh dưới dạng bytes
            image_byte_array = io.BytesIO()

            # Lưu hình ảnh chụp màn hình vào đối tượng BytesIO với định dạng PNG
            screenshot.save(image_byte_array, format="PNG")

            # Trả về dữ liệu hình ảnh dưới dạng bytes
            return image_byte_array.getvalue()
        except Exception as e:
            # Xử lý ngoại lệ nếu có lỗi trong quá trình chụp màn hình
            return f"Error capturing screenshot: {str(e)}"
