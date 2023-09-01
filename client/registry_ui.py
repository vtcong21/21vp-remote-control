import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from registry import Registry

class RegistryUI(Registry):
    def __init__(self, socket, window):
        super().__init__(socket, window)
        self.setup_ui()

    def setup_ui(self):
        self.top_window = tk.Toplevel(self.window)
        self.top_window.geometry("400x360")
        self.top_window.title("Registry Operations")

        # Apply the "arc" theme to the top window
        style = ThemedStyle(self.window)
        style.set_theme("arc")

        # Create dropdown menu for selecting function
        functions = ["Get Value", "Get Value", "Set Value", "Delete Value", "Create Key", "Delete Key"]
        self.selected_function = tk.StringVar()
        self.selected_function.set(functions[0])  # Set default function

        dropdown_menu = ttk.OptionMenu(self.top_window, self.selected_function, *functions, command=self.update_fields)
        dropdown_menu.place(relx=0.05, rely=0.03, relwidth=0.9)

        # Create labels and entry fields
        self.label_key_path = self.create_label("Key Path:")
        self.entry_key_path = self.create_entry()
   
        self.label_value_name = self.create_label("Value Name:")
        self.entry_value_name = self.create_entry()
        self.entry_value_name.place_forget()  # Ẩn mặc định

        self.label_value_data = self.create_label("Value Data:")
        self.entry_value_data = self.create_entry()
        self.entry_value_data.place_forget()  # Ẩn mặc định

        self.label_value_type = self.create_label("Value Type:")
        self.entry_value_type = self.create_entry()
        self.entry_value_type.place_forget()  # Ẩn mặc định

        # Create buttons
        self.execute_button = ttk.Button(self.top_window, text="Execute", command=self.execute_function)

        # Create log text widget
        self.log_text = self.create_text_widget()
        
        # Create scrollbar for the log text widget
        self.scrollbar = self.create_scrollbar()

        # Pack widgets
        self.label_key_path.place(relx=0.05, rely=0.12)
        self.entry_key_path.place(relx=0.05, rely=0.16, relwidth=0.9)
        self.log_text.place(relx=0.05, rely=0.38, relwidth=0.9, relheight=0.48)
        self.scrollbar.place(relx=0.95, rely=0.38, relheight=0.48)
        self.execute_button.place(relx=0.25, rely=0.88, relwidth=0.5)

        # Initialize fields
        self.update_fields()

    def update_fields(self, *args):
        selected = self.selected_function.get()

        if selected == "Get Value":
            self.fields_1()
        elif selected == "Set Value":
            self.fields_2()
        elif selected == "Delete Value":
            self.fields_1()
        elif selected == "Create Key":
            self.fields_3()
        elif selected == "Delete Key":
            self.fields_3()

    def fields_1(self):
        self.label_value_name.place(relx=0.05, rely=0.24, relwidth=0.28)
        self.entry_value_name.place(relx=0.05, rely=0.28, relwidth=0.28)
        self.label_value_data.place_forget()
        self.entry_value_data.place_forget()
        self.label_value_type.place_forget()
        self.entry_value_type.place_forget()
    
    def fields_2(self):
        self.label_value_name.place(relx=0.05, rely=0.24, relwidth=0.28)
        self.entry_value_name.place(relx=0.05, rely=0.28, relwidth=0.28)
        self.label_value_data.place(relx=0.36, rely=0.24, relwidth=0.28)
        self.entry_value_data.place(relx=0.36, rely=0.28, relwidth=0.28)
        self.label_value_type.place(relx=0.67, rely=0.24, relwidth=0.28)
        self.entry_value_type.place(relx=0.67, rely=0.28, relwidth=0.28)

    def fields_3(self):
        self.label_value_name.place_forget()
        self.entry_value_name.place_forget()
        self.label_value_data.place_forget()
        self.entry_value_data.place_forget()
        self.label_value_type.place_forget()
        self.entry_value_type.place_forget()
        
    def create_label(self, text):
        return ttk.Label(self.top_window, text=text)

    def create_entry(self):
        return ttk.Entry(self.top_window)

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

