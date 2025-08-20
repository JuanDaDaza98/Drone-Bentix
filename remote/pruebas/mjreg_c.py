import cv2
import socket
import struct
import numpy as np

HOST = '0.0.0.0'
PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
conn, addr = server_socket.accept()
connection = conn.makefile('rb')

cv2.namedWindow("Stream", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

try:
    while True:
        size_bytes = connection.read(4)
        if not size_bytes:
            break
        size = struct.unpack('<L', size_bytes)[0]
        frame_data = connection.read(size)
        frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        if frame is not None:
            cv2.imshow("Stream", frame)
        if cv2.waitKey(1) == 27:
            break
except Exception as e:
    print("Error:", e)
finally:
    connection.close()
    server_socket.close()
    cv2.destroyAllWindows()

