import tkinter as tk
from tkinter import filedialog
import socket

data = []


class SendFiles:
    def __init__(self, get_directory, ip, port):
        self.get_directory = get_directory
        self.ip = ip
        self.port = port

    @staticmethod
    def browse_files():
        file_paths = filedialog.askopenfilenames(title="Dateien auswählen", filetypes=(("Alle Dateien", "*.*"), ("Textdateien", "*.txt")))

        for file in file_paths:
            if file not in data:
                print(file)
                data.append(file)

        selected_files.set(file_paths)

    @staticmethod
    def check_file(f):
        if f.endswith(".py") or f.endswith(".txt"):
            return "r+"
        else:
            return "rb+"

    def send_data(self):
        server_data = {filename: open(filename, self.check_file(filename)).read() for filename in data}
        real_server_data = {"get_dir": self.get_directory}
        real_server_data.update(server_data)

        connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect.connect((self.ip, self.port))
        connect.send(str(real_server_data).encode())

        print("Allen Daten wurden geschickt")
        quit()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    root.title("Dateien auswählen")

    selected_files = tk.StringVar()

    send_file = SendFiles("Flask_Website/templates", "192.168.0.132", 1077)
    browse_button = tk.Button(root, text="Dateien auswählen", command=send_file.browse_files)
    sendet_data = tk.Button(root, text="Send Data", command=send_file.send_data)

    selected_files_label = tk.Label(root, textvariable=selected_files)

    browse_button.pack(pady=75)
    sendet_data.pack(pady=70)

    selected_files_label.pack(pady=10)

    root.mainloop()
    print(data)
