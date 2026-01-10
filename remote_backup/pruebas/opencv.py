import cv2
import socket
import numpy as np

# Configura UDP socket
ip_local = '0.0.0.0'
puerto = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip_local, puerto))

# Configura ventana fullscreen
window_name = 'Video en vivo'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    # Recibe datos
    packet, addr = sock.recvfrom(65536)  # 64KB máx. tamaño de paquete UDP
    npdata = np.frombuffer(packet, dtype=np.uint8)

    # Decodifica JPEG
    frame = cv2.imdecode(npdata, cv2.IMREAD_COLOR)
    if frame is None:
        continue

    # Muestra en pantalla
    cv2.imshow(window_name, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

sock.close()
cv2.destroyAllWindows()
