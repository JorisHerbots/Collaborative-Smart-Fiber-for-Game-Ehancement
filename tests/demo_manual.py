from engine import Engine
import sys
import signal


def signal_handler(signal, frame):
        app.cleanup_interfaces()
        sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
app = Engine("Manual Test Setup :D")
