import cv2
import socket
import numpy as np
import struct

HOST = '0.0.0.0'
PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("🎥 Esperando transmisión de video...")

conn, addr = server_socket.accept()
print(f"✅ Conectado con {addr}")

data = b""
payload_size = struct.calcsize("<L")

cv2.namedWindow("Stream", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

try:
    while True:
        while len(data) < payload_size:
            data += conn.recv(4096)

        packed_size = data[:payload_size]
        data = data[payload_size:]
        frame_size = struct.unpack("<L", packed_size)[0]

        while len(data) < frame_size:
            data += conn.recv(4096)

        frame_data = data[:frame_size]
        data = data[frame_size:]

        frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        frame = cv2.resize(frame, (800, 480))

        cv2.namedWindow("Stream", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Stream", frame)

        if cv2.waitKey(1) == 27:  # ESC para salir
            break
except KeyboardInterrupt:
    print("\n📴 Visualización detenida")
finally:
    conn.close()
    server_socket.close()
    cv2.destroyAllWindows()
