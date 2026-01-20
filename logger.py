import logging
import os
from datetime import datetime

LOG_FILE = "garage_events.log"

# Setup Logger
logger = logging.getLogger("GarageLogger")
logger.setLevel(logging.INFO)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(LOG_FILE)

c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
# format: [2023-10-27 10:00:00] - ACTION: Opened - STATE: Open
log_format = logging.Formatter('[%(asctime)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
c_handler.setFormatter(log_format)
f_handler.setFormatter(log_format)

# Add handlers to the logger
if not logger.handlers:
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

def log_event(action, state):
    """
    Logs an event.
    :param action: What happened (e.g., "Toggle Triggered", "Sensor Change")
    :param state: Current state of the door (e.g., "Open", "Closed")
    """
    message = f"ACTION: {action} - STATE: {state}"
    logger.info(message)

def get_recent_logs(limit=10):
    """
    Reads the last N lines from the log file.
    """
    if not os.path.exists(LOG_FILE):
        return []
    
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()
        recent = lines[-limit:]
        recent.reverse() # Newest first
        return recent
