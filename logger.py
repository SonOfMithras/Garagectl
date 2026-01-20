import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

LOG_FILE = "garage_events.log"

# Setup Logger
logger = logging.getLogger("GarageLogger")
logger.setLevel(logging.INFO)

# Create handlers
c_handler = logging.StreamHandler()
# Daily rotation at midnight, keep last 30 days
f_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight", interval=1, backupCount=30)
f_handler.suffix = "%Y-%m-%d" # Suffix format: garage_events.log.2023-10-27

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

def parse_log_line(line):
    """
    Parses a log line into a dictionary.
    Returns None if parsing fails.
    """
    # Regex to parse: [TIMESTAMP] - ACTION: ... - STATE: ...
    # Example: [2026-01-19 23:54:48] - ACTION: User Toggle - STATE: Activating (from Closed)
    regex = r"\[(.*?)\] - ACTION: (.*?) - STATE: (.*)"
    match = re.search(regex, line)
    if match:
        timestamp_str = match.group(1)
        action = match.group(2)
        state = match.group(3)
        return {
            "timestamp": timestamp_str,
            "action": action,
            "state": state,
            "raw": line.strip()
        }
    return None

def get_recent_logs(limit=10):
    """
    Reads the last N lines from the current log file and parses them.
    """
    if not os.path.exists(LOG_FILE):
        return []
    
    parsed_logs = []
    with open(LOG_FILE, 'r') as f:
        # Read all lines is safest for small logs
        lines = f.readlines()
        # Take last N
        relevant_lines = lines[-limit:]
        
        for line in relevant_lines:
            parsed = parse_log_line(line)
            if parsed:
                parsed_logs.append(parsed)
            else:
                 # Fallback for unexpected format
                parsed_logs.append({"timestamp": "", "action": "Unknown", "state": "", "raw": line.strip()})
        
        parsed_logs.reverse() # Newest first
        return parsed_logs

def get_archived_logs():
    """
    Returns a list of archived log files (rotated files).
    """
    archives = []
    # List all files in directory
    for f in os.listdir("."):
        if f.startswith(LOG_FILE + "."):
            # f is like garage_events.log.2023-10-27
            archives.append(f)
    archives.sort(reverse=True) # Newest first
    return archives

def read_log_file(filename):
    """
    Reads a specific log file (current or archive) and returns parsed contents.
    """
    # Security check: filename must be basename only
    if os.path.dirname(filename) != "":
        return []
    
    if not os.path.exists(filename):
        return []
        
    parsed_logs = []
    with open(filename, 'r') as f:
        for line in f:
            parsed = parse_log_line(line)
            if parsed:
                parsed_logs.append(parsed)
    
    parsed_logs.reverse()
    return parsed_logs
