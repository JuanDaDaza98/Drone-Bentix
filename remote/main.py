from time import sleep
from threading import Thread
from joystick_reader import JoystickReader
from network_sender import DroneSender
from video_receiver import receive_video_stream

joystick = JoystickReader()
sender = DroneSender()

connected = True

def control_loop():
    global connected
    try:
        while True:
            y1, x2, y2, b1, b2 = joystick.read()
            data = [y1, x2, y2, b1, b2]

            try:
                sender.send_control(data)
                if not connected:
                    print("🔗 Reconectado con el dron.")
                    connected = True
            except Exception as e:
                if connected:
                    print(f"❌ Conexión perdida con el dron. Esperando reconexión... ({e})")
                    connected = False

            sleep(0.1)
    except KeyboardInterrupt:
        print("🛑 Finalizando controlador...")

if __name__ == "__main__":
    t_control = Thread(target=control_loop)

    while sender.get_video_socket() is None:
        print("⏳ Esperando conexión de video...")
        sleep(0.5)

    t_video = Thread(target=receive_video_stream, args=(sender.get_video_socket,))

    t_control.start()
    t_video.start()

    t_control.join()
    t_video.join()
