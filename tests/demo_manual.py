from engine import Engine
import sys
import signal


def signal_handler(signal, frame):
        app.cleanup_interfaces()
        sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
app = Engine("Manual Test Setup :D")


@app.register_trigger("button_pressed")
def press(**kwargs):
        print("Button pressed")
        for key, value in kwargs.items():
                print("%s = %s" % (key, value))


@app.register_trigger("button_released")
def press(**kwargs):
        print("Button released")
        for key, value in kwargs.items():
                print("%s = %s" % (key, value))