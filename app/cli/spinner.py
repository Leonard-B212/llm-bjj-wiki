# Provides a lightweight terminal spinner for long-running CLI operations.
# Runs the animation in a background thread while application work continues normally.

import sys
import threading
import time


class Spinner:
    def __init__(self, message="Working...", interval=0.1):
        self.message = message
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread = None

    # Starts the spinner animation in a background thread.
    def start(self):
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._spin,
            daemon=True
        )
        self._thread.start()

    # Stops the spinner and clears the active terminal line.
    def stop(self):
        if not self._thread:
            return

        self._stop_event.set()
        self._thread.join()

        sys.stdout.write("\r" + " " * (len(self.message) + 4) + "\r")
        sys.stdout.flush()

    # Continuously renders spinner frames until the stop event is set.
    def _spin(self):
        frames = ["|", "/", "-", "\\"]
        index = 0

        while not self._stop_event.is_set():
            frame = frames[index % len(frames)]

            sys.stdout.write(f"\r{self.message} {frame}")
            sys.stdout.flush()

            index += 1
            time.sleep(self.interval)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()