import socket
import threading
from time import sleep

class DroneReceiver:
    def __init__(self, ip="192.168.4.3", port_control=5000, port_video=6000):
        self.ip = ip
        self.port_control = port_control
        self.port_video = port_video

        self.control_socket = None
        self.control_client = None

        self.video_socket = None
        self.video_client = None

        # Iniciar hilos para ambos servidores
        threading.Thread(target=self._setup_control_server, daemon=True).start()
        threading.Thread(target=self._setup_video_server, daemon=True).start()

    def wait_for_connections(self):
        while self.control_client is None:
            sleep(0.1)
        while self.video_client is None:
            sleep(0.1)

    def wait_for_video_connection(self):
        if self.video_client:
            try:
                self.video_client.close()
            except:
                pass
        print("🔁 Esperando reconexión de video...")
        self.video_client, _ = self.video_socket.accept()
        print("✅ Cliente de video reconectado.")


    def _setup_control_server(self):
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.control_socket.bind((self.ip, self.port_control))
        self.control_socket.listen(1)
        print("🎮 Esperando conexión de control...")
        self.control_client, _ = self.control_socket.accept()
        print("✅ Cliente de control conectado.")

    def _setup_video_server(self):
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.video_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.video_socket.bind((self.ip, self.port_video))
        self.video_socket.listen(1)
        print("🎥 Esperando conexión de video...")
        self.video_client, _ = self.video_socket.accept()
        print("✅ Cliente de video conectado.")

    def receive_video_frame(self):
        self.video_client.settimeout(1.0)
        try:
            return self.video_client.recv(4096)
        except (socket.timeout, ConnectionResetError, BrokenPipeError, OSError):
            print("❌ Conexión de video perdida.")
            self.wait_for_video_connection()
            return None

    def receive_control_data(self):
        try:
            data = self.control_client.recv(1024)
            if not data:
                raise ConnectionResetError
            self.control_client.send(b"ACK\n")
            return list(map(int, data.decode().split(',')))
        except (ConnectionResetError, BrokenPipeError, socket.error, ValueError):
            print("❗ Conexión de control perdida. Esperando reconexión...")
            self._setup_control_server()
            return []

    def close(self):
        if self.control_client:
            self.control_client.close()
        if self.control_socket:
            self.control_socket.close()
        if self.video_client:
            self.video_client.close()
        if self.video_socket:
            self.video_socket.close()
