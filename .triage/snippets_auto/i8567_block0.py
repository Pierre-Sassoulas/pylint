import signal
import sys

def handle_signal():
    signal.signal(signal.SIGINT, lambda sig, frame: [print("Aborted using CTRL+C"), sys.exit(1)])
    print("Signal handler installed.")
