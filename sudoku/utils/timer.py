"""
Game timer module.
Provides timer functionality for tracking game duration.
"""

import threading
import time
from typing import Callable

class GameTimer:
    """
    Timer class for tracking game duration.
    Provides start, stop, pause, and reset functionality.
    """

    def __init__(self, callback: Callable[[int], None]):
        """
        Initialize timer.

        Args:
            callback (callable): Function to call with current time
        """
        self.callback = callback
        self.seconds = 0
        self._running = False
        self._paused = False
        self._stop_event = threading.Event()
        self._timer_thread = None

    def start(self) -> None:
        """Start or resume the timer."""
        if not self._running:
            self._running = True
            self._paused = False
            self._stop_event.clear()
            self._timer_thread = threading.Thread(target=self._run)
            self._timer_thread.daemon = True
            self._timer_thread.start()

    def stop(self) -> None:
        """Stop the timer."""
        self._running = False
        if self._timer_thread:
            self._stop_event.set()
            self._timer_thread.join()

    def pause(self) -> None:
        """Pause the timer."""
        self._paused = True

    def resume(self) -> None:
        """Resume the timer."""
        self._paused = False

    def reset(self) -> None:
        """Reset the timer to zero."""
        self.stop()
        self.seconds = 0
        self.callback(0)

    def _run(self) -> None:
        """Main timer loop."""
        while self._running and not self._stop_event.is_set():
            if not self._paused:
                time.sleep(1)
                if self._running and not self._paused:
                    self.seconds += 1
                    try:
                        self.callback(self.seconds)
                    except Exception:
                        # If callback fails, stop the timer
                        self._running = False
                        break

    @property
    def time(self) -> int:
        """
        Get current time in seconds.

        Returns:
            int: Elapsed time in seconds
        """
        return self.seconds

    def get_formatted_time(self) -> str:
        """
        Get formatted time string.

        Returns:
            str: Time formatted as MM:SS
        """
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
