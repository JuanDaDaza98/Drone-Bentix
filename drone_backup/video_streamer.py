import cv2
import struct
import time

def video_stream(client_socket):
    print("🎥 Iniciando transmisión de video desde la cámara...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error al capturar frame.")
                break

            _, buffer = cv2.imencode('.jpg', frame)
            data = buffer.tobytes()

            # Envía longitud del frame (4 bytes) + datos
            client_socket.sendall(len(data).to_bytes(4, 'big') + data)
            print(f"📤 Frame enviado: {len(data)} bytes")
            sleep(0.03)  # 30 FPS
    except Exception as e:
        print(f"⚠️ Error de transmisión: {e}")
    finally:
        cap.release()
        client_socket.close()
        print("🔁 Transmisión de video finalizada.")
