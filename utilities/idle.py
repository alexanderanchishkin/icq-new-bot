import os
import signal
import time


def signal_handler(sig, handler):
    os.kill(os.getpid(), signal.SIGTERM)


def our_idle():
    stop_signals = (signal.SIGINT, signal.SIGTERM, signal.SIGABRT)
    for sig in stop_signals:
        signal.signal(sig, signal_handler)

    while True:
        time.sleep(1)
