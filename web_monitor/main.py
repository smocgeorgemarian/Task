import logging
import os

from web_monitor.location_monitor import LocationMonitor


logging.basicConfig(level=logging.INFO)

def main():
    monitor = LocationMonitor(location=os.path.join(".", "..", "resources"), api_URL="http://127.0.0.1:8000")
    monitor.run()


if __name__ == "__main__":
    main()
