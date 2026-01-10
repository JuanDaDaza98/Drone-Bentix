import socket
import time

class DroneSender:
    def __init__(self, ip="192.168.4.3", control_port=5000, video_port=6000):
        self.ip = ip
        self.control_port = control_port
        self.video_port = video_port
        self.control_socket = None
        self.video_socket = None
        self._setup_control_connection()
        self._setup_video_connection()

    def _setup_control_connection(self):
        if self.control_socket:
            try:
                self.control_socket.close()
            except:
                pass

        while True:
            try:
                print("📡 Intentando conectar al dron (controles)...")
                self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.control_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.control_socket.settimeout(3.0)
                self.control_socket.connect((self.ip, self.control_port))
                self.control_socket.settimeout(None)
                print("✅ Conectado al dron (controles).")
                break
            except socket.error as e:
                print(f"⏳ Esperando conexión de controles... ({e})")
                time.sleep(2)

    def _setup_video_connection(self):
        if self.video_socket:
            try:
                self.video_socket.close()
            except:
                pass

        while True:
            try:
                print("📺 Intentando conectar al dron (video)...")
                self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.video_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.video_socket.settimeout(3.0)
                self.video_socket.connect((self.ip, self.video_port))
                self.video_socket.settimeout(None)
                print("✅ Conectado al dron (video).")
                break
            except socket.error as e:
                print(f"⏳ Esperando conexión de video... ({e})")
                time.sleep(2)

    def send_control(self, data_list):
        try:
            message = ",".join(map(str, data_list))
            self.control_socket.sendall(message.encode())

            # Esperar confirmación del dron
            self.control_socket.settimeout(2.0)
            ack = self.control_socket.recv(16)
            if b"ACK" not in ack:
                raise ConnectionResetError("No se recibió ACK del dron")
            self.control_socket.settimeout(None)

        except (socket.timeout, BrokenPipeError, ConnectionResetError, socket.error, OSError) as e:
            print(f"❌ Conexión perdida en controles. Reintentando... ({e})")
            try:
                self.control_socket.close()
            except:
                pass
            self._setup_control_connection()
            raise e  # Propagar al main

    def get_video_socket(self):
        return self.video_socket
