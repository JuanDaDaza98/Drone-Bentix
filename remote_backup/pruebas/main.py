#!/usr/bin/env python3
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

Gst.init(None)

# Reemplaza width y height por la resolución de tu pantalla
pipeline_str = (
    'udpsrc port=5000 caps="application/x-rtp, media=video, encoding-name=H264, payload=96" ! '
    'rtph264depay ! avdec_h264 ! videoconvert ! videoscale ! '
    'video/x-raw,width=800,height=480 ! kmssink'
)

print("Pipeline:", pipeline_str)
pipeline = Gst.parse_launch(pipeline_str)

bus = pipeline.get_bus()
bus.add_signal_watch()

def on_message(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print("Error:", err, debug)
        loop.quit()
    elif t == Gst.MessageType.EOS:
        print("Fin del stream")
        loop.quit()
    return True

bus.connect("message", on_message, None)

pipeline.set_state(Gst.State.PLAYING)
loop = GLib.MainLoop()
try:
    loop.run()
except KeyboardInterrupt:
    pass
pipeline.set_state(Gst.State.NULL)
