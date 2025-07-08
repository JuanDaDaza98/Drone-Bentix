import socket
import time

class DroneReceiver:
    def __init__(self, ip="192.168.4.3", port=5000):
        self.ip = ip
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.client_address = None
        self._setup_server()

    def _setup_server(self):
        if self.server_socket:
            self.server_socket.close()
        print("Iniciando servidor de red...")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(1)
        print("Esperando conexión del controlador...")
        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"Conectado con {self.client_address}")

    def receive(self):
        try:
            data = self.client_socket.recv(1024)
            if not data:
                raise ConnectionResetError
            return list(map(int, data.decode().split(',')))
        except (ConnectionResetError, BrokenPipeError, socket.error):
            print("❗ Conexión perdida. Reiniciando servidor...")
            self._setup_server()
            return []

    def close(self):
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()