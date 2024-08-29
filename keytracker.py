import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from pynput import keyboard
import datetime

class Keylogger:
    def __init__(self, root):
        self.root = root
        self.root.title("KeyTracker - Python key tracker")
        self.root.geometry("500x300")  
        self.root.resizable(False, False)
        self.log = []
        self.is_tracking = False


        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Trackear", command=self.start_tracking, bootstyle=SUCCESS, width=14)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = ttk.Button(button_frame, text="Detener", command=self.stop_tracking, bootstyle=DANGER, width=14)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)
        self.stop_button.config(state=DISABLED)
        
        self.export_button = ttk.Button(button_frame, text="Exportar Log", command=self.export_log, bootstyle=INFO, width=14)
        self.export_button.grid(row=0, column=2, padx=5, pady=5)
        self.export_button.config(state=DISABLED)

        self.clear_button = ttk.Button(button_frame, text="Borrar Log", command=self.clear_log, bootstyle=DANGER, width=14)
        self.clear_button.grid(row=0, column=3, padx=5, pady=5)

        self.log_label = ttk.Label(root, text="Registro de teclas:", font=("Helvetica", 12))
        self.log_label.pack(pady=10)

        self.log_text = ttk.Text(root, height=10, width=52, state=DISABLED)
        self.log_text.pack(pady=10)

    def start_tracking(self):
        self.is_tracking = True
        self.log = []
        self.start_button.config(state=DISABLED)
        self.stop_button.config(state=NORMAL)
        self.export_button.config(state=DISABLED)
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_tracking(self):
        self.is_tracking = False
        self.listener.stop()
        self.start_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)
        self.export_button.config(state=NORMAL)

    def on_press(self, key):
        if self.is_tracking:
            try:
                log_entry = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {key.char}"
                self.log.append(log_entry)
            except AttributeError:
                log_entry = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [{key}]"
                self.log.append(log_entry)
            
            self.log_text.config(state=NORMAL)
            self.log_text.insert(END, log_entry + "\n")
            self.log_text.config(state=DISABLED)

    def export_log(self):
        with open("keylog.txt", "w") as file:
            file.write('\n'.join(self.log))
        messagebox.showinfo("Exportar Log", "El log se ha exportado a keylog.txt")
        self.export_button.config(state=DISABLED)

    def clear_log(self):
        self.log = []
        self.log_text.config(state=NORMAL)
        self.log_text.delete(1.0, END)
        self.log_text.config(state=DISABLED)
        self.export_button.config(state=DISABLED)

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")  
    app = Keylogger(root)
    root.mainloop()
