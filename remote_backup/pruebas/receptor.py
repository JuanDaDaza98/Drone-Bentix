#!/usr/bin/env python3

import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gst, Gtk, Gdk

Gst.init(None)
Gtk.init(None)

class VideoPlayer:
    def __init__(self):
        # Crear ventana
        self.window = Gtk.Window()
        self.window.connect("destroy", self.quit)
        self.window.fullscreen()

        # Obtener resolución de pantalla con Gdk.Display
        display = Gdk.Display.get_default()
        monitor = display.get_monitor(0)
        geometry = monitor.get_geometry()
        width = geometry.width
        height = geometry.height
        self.window.set_size_request(width, height)

        # Crear pipeline de GStreamer para pantalla completa
        self.pipeline = Gst.parse_launch(
            "udpsrc port=5000 caps=\"application/x-rtp, media=video, encoding-name=H264, payload=96\" "
            "! rtph264depay ! avdec_h264 ! videoconvert ! glimagesink force-aspect-ratio=true"
        )

        # Mostrar ventana y reproducir el pipeline
        self.window.show_all()
        self.pipeline.set_state(Gst.State.PLAYING)

    def quit(self, widget):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

player = VideoPlayer()
Gtk.main()
