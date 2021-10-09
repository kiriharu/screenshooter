import os
import socket

# chrome doesn't work via hostname
try:
    CHROME_IP = socket.getaddrinfo("chromium", 0)[0][4][0]
except socket.gaierror:
    CHROME_IP = "127.0.0.1"
CHROME_ADDRESS = f"http://{CHROME_IP}:9222"
WAIT_FOR_LOAD = int(os.getenv("WAIT_FOR_LOAD", 1))
RESTRICTED_HOSTS: list[str] = os.getenv("RESTRICTED_HOSTS", "").split(";")
SCREENSHOTS_STATIC_DIR = "data"
SCREENSHOTS_DIR = f"./{SCREENSHOTS_STATIC_DIR}"
SCREENSHOT_CACHE_TTL = 100
