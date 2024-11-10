import subprocess
import threading
import atexit
import signal
import sys

class WSLProcessSingleton:
    _instance = None
    _lock = threading.Lock()
    _process = None

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    print("Creating new instance of WSLProcessSingleton...")
                    cls._instance = super(WSLProcessSingleton, cls).__new__(cls)
                    cls._instance._start_wsl()
                    atexit.register(cls._instance.stop_wsl)  # Register the cleanup function
                    signal.signal(signal.SIGINT, cls._instance._signal_handler)
                    signal.signal(signal.SIGTERM, cls._instance._signal_handler)
        return cls._instance

    def _start_wsl(self):
        command = "wsl"
        self._process = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'  # Set encoding to UTF-8
        )
        print("WSL process started, ready for interaction...")

    def stop_wsl(self):
        # Shutting down WSL using the 'wsl --shutdown' command
        print("Shutting down WSL...")
        shutdown_command = "wsl --shutdown"
        subprocess.run(shutdown_command, shell=True)
        print("WSL has been shut down.")

    def _signal_handler(self, signum, frame):
        print(f"Signal {signum} received, stopping WSL...")
        self.stop_wsl()
        sys.exit(0)  # Exit the program


if __name__ == "__main__":
    # Example usage:
    wsl_instance = WSLProcessSingleton()

    # Send a command to WSL (You can replace this with any command you want to execute)
    # response = wsl_instance.execute("echo 'Hello from WSL!'")
    # print(f"Response from WSL: {response}")

    # Send a message to the WSL terminal (example: list files)
    # response = wsl_instance.send_message("ls")
    # print(f"Response from WSL: {response}")

    # Clear the terminal (if you have a clear function)
    # wsl_instance.clear()

    # Stop the WSL instance on exit
    wsl_instance.stop_wsl()
