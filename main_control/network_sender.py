import socket
import time

class DroneSender:
    def __init__(self, ip="192.168.4.3", port=5000):
        self.ip = ip
        self.port = port
        self.socket = None
        self.connect()

    def connect(self):
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.ip, self.port))
                print("✅ Conectado al dron.")
                break
            except socket.error:
                print("⏳ Esperando conexión al dron...")
                time.sleep(2)

    def send(self, data_list):
        try:
            message = ",".join(map(str, data_list))
            self.socket.send(message.encode())
        except (BrokenPipeError, ConnectionResetError, socket.error):
            print("❌ Conexión perdida. Reintentando...")
            self.connect()