#!/usr/bin/env python3
import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gst, Gtk, Gdk, GstVideo

# Inicializar GStreamer y GTK
Gst.init(None)
Gtk.init(None)

class VideoPlayer(Gtk.Window):
    def _init_(self):
        Gtk.Window._init_(self, title="Video Full Screen")
        self.connect("destroy", self.quit)
        self.fullscreen()

        # Crear y agregar un DrawingArea para incrustar el video
        self.da = Gtk.DrawingArea()
        self.add(self.da)

        # Obtener dimensiones de la pantalla utilizando Gdk.Screen
        screen = Gdk.Screen.get_default()
        width = screen.get_width()
        height = screen.get_height()
        # Opcionalmente, puedes configurar la ventana con estas dimensiones:
        self.set_size_request(width, height)
        
        # Construir el pipeline:
        # Se usa udpsrc para recibir los datos RTP, se desempaqueta y decodifica el H264,
        # se convierte el formato, se escala el video a la resolución de la pantalla y
        # finalmente se envía a glimagesink.
        pipeline_str = (
            "udpsrc port=5000 caps=\"application/x-rtp, media=video, encoding-name=H264, payload=96\" ! "
            "rtph264depay ! avdec_h264 ! videoconvert ! videoscale ! "
            f"video/x-raw,width={width},height={height} ! glimagesink"
        )
        self.pipeline = Gst.parse_launch(pipeline_str)

        # Configuramos el bus para recibir mensajes de error o fin de stream
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        # Mostramos la ventana y pasamos al estado PLAYING
        self.show_all()
        self.pipeline.set_state(Gst.State.PLAYING)

        # Conectar el video overlay para dibujar en el DrawingArea
        self.da.connect("realize", self.on_realize)

    def on_realize(self, widget):
        # Obtenemos el identificador de ventana (window handle)
        window = widget.get_window()
        if window:
            # En sistemas X11 se usa get_xid(); en Wayland podría requerirse otro método
            xid = window.get_xid()
            # Buscar en el pipeline el elemento que implemente la interfaz VideoOverlay
            video_overlay = self.pipeline.get_by_interface(GstVideo.VideoOverlay._gtype_)
            if video_overlay:
                video_overlay.set_window_handle(xid)

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error:", err, debug)
            self.quit()
        elif t == Gst.MessageType.EOS:
            print("End-of-stream")
            self.quit()

    def quit(self, widget=None):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

player = VideoPlayer()
Gtk.main()
