import threading
import time
import sys
from colors import Color


class Spinner:
    """Display a spinner/thinking animation while waiting for a task to complete."""

    def __init__(self, message: str | None = None, color: Color | None = None) -> None:
        self.color = color

        # Set default message with assistant prefix if color available
        if message is None:
            if color:
                self.message = color.magenta("Assistant: ", bold=True) + color.yellow(
                    "Thinking"
                )
            else:
                self.message = "Assistant: Thinking"
        else:
            self.message = message

        self.stop_event = threading.Event()
        self.spinner_thread = None

    def _spin(self) -> None:
        """The animation function that runs in a separate thread."""
        frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        i = 0

        # Display message with color if color is provided
        if self.color:
            sys.stdout.write(self.color.yellow(f"{self.message} "))
        else:
            sys.stdout.write(f"{self.message} ")

        while not self.stop_event.is_set():
            if self.color:
                sys.stdout.write(
                    self.color.yellow(frames[i % len(frames)] + " ", bold=True)
                )
            else:
                sys.stdout.write(frames[i % len(frames)] + " ")

            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b\b")
            i += 1

        # Clear the spinner
        sys.stdout.write(
            "\r\033[K"
        )  # \r moves cursor to start of line, \033[K clears to end of line
        sys.stdout.flush()

    def start(self) -> None:
        """Start the spinner animation in a separate thread."""
        self.spinner_thread = threading.Thread(target=self._spin)
        self.spinner_thread.daemon = True
        self.spinner_thread.start()
        return self

    def stop(self) -> None:
        """Stop the spinner animation."""
        if self.spinner_thread and self.spinner_thread.is_alive():
            self.stop_event.set()
            self.spinner_thread.join()

    def __enter__(self) -> "Spinner":
        """Support for 'with' context manager."""
        self.start()
        return self

    def __exit__(
        self, exc_type: type | None, exc_val: object | None, exc_tb: object | None
    ) -> None:
        """Support for 'with' context manager."""
        self.stop()
