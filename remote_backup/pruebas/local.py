import cv2

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

# Resolución alta (ajusta según tu cámara)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Codec y archivo de salida
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (480, 320))

# Ventana en fullscreen
cv2.namedWindow('Grabar Video', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Grabar Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: No se pudo recibir el frame.")
        break

    out.write(frame)
    cv2.imshow('Grabar Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
