from engine import Engine
import sys
import signal


def signal_handler(signal, frame):
        app._cleanup_interfaces()
        sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
app = Engine("Manual Test Setup :D", host="0.0.0.0", port="25500")


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


@app.register_trigger("game_started")
def gamestart(**kwargs):
        print("Game started")
        for key, value in kwargs.items():
                print("%s = %s" % (key, value))


@app.register_trigger("entity_registered")
def press(**kwargs):
        print("Entity registered")
        for key, value in kwargs.items():
                print("%s = %s" % (key, value))