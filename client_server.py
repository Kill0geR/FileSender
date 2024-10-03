import socket
import os
from client import SendFiles
import time

class CoreServerClient:
    def __init__(self, send_directory, directory_server, ip, port):
        self.ip = ip
        self.port = port
        self.send_directory = send_directory
        self.directory_server = directory_server
        self.data = {"get_dir": self.directory_server}

    def send_data(self):
        if self.send_directory in os.listdir():
            os.chdir(self.send_directory)
        else:
            os.mkdir(self.send_directory)
            os.chdir(self.send_directory)

        for filename in os.listdir():
            with open(filename, SendFiles.check_file(filename)) as file:
                self.data[filename] = file.read()

        try:
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con.connect((self.ip, self.port))
            con.send(str(self.data).encode())
        except ConnectionRefusedError:
            print(f"Die Verbindung zum Server '{self.ip}' konnte nicht hergestellt werden".upper())


if __name__ == "__main__":
    data = CoreServerClient("Test", "All_files", "127.0.0.1", 1077)
    data.send_data()
