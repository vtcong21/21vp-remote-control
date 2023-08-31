import tkinter as tk
from registry import Registry

class RegistryUI(Registry):
    def __init__(self, socket, window):
        super().__init__(socket, window)
        self.setup_ui()

    def setup_ui(self):
        self.top_window = tk.Toplevel(self.window)
        self.top_window.title("Registry Operations")

        # Create dropdown menu for selecting function
        functions = ["Get Value", "Set Value", "Delete Value", "Create Key", "Delete Key"]
        self.selected_function = tk.StringVar()
        self.selected_function.set(functions[0])  # Set default function

        dropdown_menu = tk.OptionMenu(self.top_window, self.selected_function, *functions, command=self.update_fields)
        dropdown_menu.pack()

        # Create labels and entry fields
        self.label_key_path = self.create_label("Key Path:")
        self.entry_key_path = self.create_entry()

        self.label_value_name = self.create_label("Value Name:")
        self.entry_value_name = self.create_entry()
        self.entry_value_name.pack_forget()  # Ẩn mặc định

        self.label_value_data = self.create_label("Value Data:")
        self.entry_value_data = self.create_entry()
        self.entry_value_data.pack_forget()  # Ẩn mặc định

        self.label_value_type = self.create_label("Value Type:")
        self.entry_value_type = self.create_entry()
        self.entry_value_type.pack_forget()  # Ẩn mặc định

        # Create buttons
        self.execute_button = tk.Button(self.top_window, text="Execute", command=self.execute_function)
        self.execute_button.pack()

        # Create log text widget
        self.log_text = self.create_text_widget()
        
        # Create scrollbar for the log text widget
        self.scrollbar = self.create_scrollbar()

        # Pack widgets
        self.label_key_path.pack()
        self.entry_key_path.pack()
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.execute_button.pack()

        # Initialize fields
        self.update_fields()

    def update_fields(self, *args):
        selected = self.selected_function.get()

        if selected == "Get Value":
            self.hide_fields([self.label_value_data, self.entry_value_data, self.label_value_type, self.entry_value_type])
            self.show_fields([self.label_value_name, self.entry_value_name])
        elif selected == "Set Value":
            self.show_fields([self.label_value_data, self.entry_value_data, self.label_value_type, self.entry_value_type, self.label_value_name, self.entry_value_name])
        elif selected == "Delete Value":
            self.hide_fields([self.label_value_data, self.entry_value_data, self.label_value_type, self.entry_value_type])
            self.show_fields([self.label_value_name, self.entry_value_name])
        elif selected == "Create Key":
            self.hide_fields([self.label_value_name, self.entry_value_name, self.label_value_data, self.entry_value_data, self.label_value_type, self.entry_value_type])
        elif selected == "Delete Key":
            self.hide_fields([self.label_value_name, self.entry_value_name, self.label_value_data, self.entry_value_data, self.label_value_type, self.entry_value_type])

    def hide_fields(self, fields):
        for field in fields:
            field.pack_forget()

    def show_fields(self, fields):
        for field in fields:
            field.pack()

    def create_label(self, text):
        return tk.Label(self.top_window, text=text)

    def create_entry(self):
        return tk.Entry(self.top_window)

    def create_text_widget(self):
        text_widget = tk.Text(self.top_window)
        text_widget.config(state=tk.DISABLED)
        return text_widget

    def create_scrollbar(self):
        scrollbar = tk.Scrollbar(self.top_window, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scrollbar.set)
        return scrollbar

    def execute_function(self):
        selected = self.selected_function.get()

        if selected == "Get Value":
            self.get_value_ui()
        elif selected == "Set Value":
            self.set_value_ui()
        elif selected == "Delete Value":
            self.delete_value_ui()
        elif selected == "Create Key":
            self.create_key_ui()
        elif selected == "Delete Key":
            self.delete_key_ui()

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)

    def get_value_ui(self):
        key_path = self.entry_key_path.get()
        value_name = self.entry_value_name.get()
        response = self.get_value(key_path, value_name)
        self.log(response)

    def set_value_ui(self):
        key_path = self.entry_key_path.get()
        value_name = self.entry_value_name.get()
        value_data = self.entry_value_data.get()
        value_type = self.entry_value_type.get()
        response = self.set_value(key_path, value_name, value_data, value_type)
        self.log(response)

    def delete_value_ui(self):
        key_path = self.entry_key_path.get()
        value_name = self.entry_value_name.get()
        response = self.delete_value(key_path, value_name)
        self.log(response)

    def create_key_ui(self):
        key_path = self.entry_key_path.get()
        response = self.create_key(key_path)
        self.log(response)

    def delete_key_ui(self):
        key_path = self.entry_key_path.get()
        response = self.delete_key(key_path)
        self.log(response)

