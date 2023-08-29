from server_ui import ServerUI
from tkinter import Tk
if __name__ == "__main__":
    root = Tk()
    server_ui = ServerUI(root)
    server_ui.server.get_running_processus()
    root.mainloop()