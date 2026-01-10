import struct
import numpy as np
import cv2
import time

def receive_video_stream(video_socket_getter):
    print("🎥 Receptor de video iniciado...")

    cv2.namedWindow("Video del Dron", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Video del Dron", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        try:
            video_socket = video_socket_getter()
            if video_socket is None:
                print("⏳ Esperando socket de video...")
                time.sleep(1)
                continue

            data = b""
            payload_size = struct.calcsize("<L")

            while True:
                # Leer encabezado del frame (4 bytes)
                while len(data) < payload_size:
                    packet = video_socket.recv(4096)
                    if not packet:
                        raise ConnectionError("❌ Conexión cerrada por el dron.")
                    data += packet

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("<L", packed_msg_size)[0]

                # Leer el contenido del frame JPEG
                while len(data) < msg_size:
                    packet = video_socket.recv(4096)
                    if not packet:
                        raise ConnectionError("❌ Conexión cerrada por el dron.")
                    data += packet

                frame_data = data[:msg_size]
                data = data[msg_size:]

                # Decodificar y mostrar
                frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
                frame = cv2.resize(frame, (800, 480))

                if frame is not None:
                    cv2.imshow("Video del Dron", frame)

#                cv2.waitKey(1)
#                data = b""

                if cv2.waitKey(1) == ord('q'):
                    return

        except Exception as e:
            print(f"⚠️ Error de recepción de video: {e}")
            print("🔁 Reintentando conexión en 3 segundos...")
            time.sleep(3)
            continue
        finally:
            cv2.destroyAllWindows()
