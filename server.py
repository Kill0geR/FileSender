import socket
import ast
import os


class ServerSendedFiles:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    @staticmethod
    def collect_data(connection):
        full_msg = ""
        while True:
            msg = connection.recv(8192).decode()
            if len(msg) <= 0: break
            full_msg += msg

        return full_msg

    @staticmethod
    def check_mode(f):
        if f.endswith(".py") or f.endswith(".txt"):
            return "a+"
        else:
            return "ab+"

    def show_data(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, self.port))
        server.listen(100)

        while True:
            print("Wait for data....")
            client_socket, ip_address = server.accept()
            print(f"Connected with {ip_address}")

            full_msg = self.collect_data(client_socket)
            collect_all_data = ast.literal_eval(full_msg)

            collect_dir = collect_all_data["get_dir"]
            if collect_dir in os.listdir():
                print("works")
                os.chdir(collect_dir)

            else:
                os.mkdir(collect_dir)
                os.chdir(collect_dir)

            for filename, data in collect_all_data.items():
                if filename == "get_dir":
                    continue
                else:
                    name = filename
                    if "/" in filename:
                        name = filename.split("/")[-1]
                    with open(name, self.check_mode(name)) as file:
                        file.write(data)

            print("Alles hat funktioniert")


get_data = ServerSendedFiles("127.0.0.1", 1077)
get_data.show_data()
