import time
import threading
import logger

try:
    import RPi.GPIO as GPIO
except ImportError:
    import mock_gpio as GPIO

# Pin Configuration (BCM Mode)
RELAY_PIN = 17       # Pin connected to Relay ch 1
SENSOR_PIN = 27      # Pin connected to Reed Switch

# State Constants
DOOR_OPEN = "Open"
DOOR_CLOSED = "Closed"

_monitor_thread = None
_stop_monitoring = False
_last_known_state = None

def _monitor_door_loop():
    global _last_known_state
    while not _stop_monitoring:
        current_state = get_door_status()
        if _last_known_state is not None and current_state != _last_known_state:
            logger.log_event("State Change", current_state)
        _last_known_state = current_state
        time.sleep(1)

def setup_gpio():
    """Initialize GPIO pins."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    # Reed switch: Common to GND, NO/NC to Pin. Use Pull Up.
    # If switch is CLOSED (Magnet near), pin is grounded (LOW).
    # If switch is OPEN (Magnet away), pin is pulled up (HIGH).
    GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Ensure relay is OFF
    GPIO.output(RELAY_PIN, GPIO.LOW)

    # Start Monitor Thread
    global _monitor_thread, _stop_monitoring, _last_known_state
    # Initialize state so we don't log "change" on startup, just the first state
    _last_known_state = get_door_status()
    logger.log_event("System Startup", _last_known_state)
    
    if _monitor_thread is None or not _monitor_thread.is_alive():
        _stop_monitoring = False
        _monitor_thread = threading.Thread(target=_monitor_door_loop, daemon=True)
        _monitor_thread.start()

def toggle_door():
    """Activates the garage door relay for a short pulse."""
    print("Toggling Garage Door...")
    current_state = get_door_status()
    logger.log_event("User Toggle", f"Activating (from {current_state})")
    GPIO.output(RELAY_PIN, GPIO.HIGH) # Press
    time.sleep(0.5)                   # Hold
    GPIO.output(RELAY_PIN, GPIO.LOW)  # Release
    
    # Mock Simulation Logic: If using Mock GPIO, flip the sensor state after delays
    if hasattr(GPIO, '_test_set_pin_state'):
        def _mock_door_travel():
            time.sleep(2) # Simulate travel time
            # Flip logic: If Closed (Low/GND) -> Open (High/PullUp). If Open -> Closed.
            # Pin is Low when Magnet is near (Closed).
            new_val = GPIO.HIGH if current_state == DOOR_CLOSED else GPIO.LOW
            GPIO._test_set_pin_state(SENSOR_PIN, new_val)
            print(f"Mock Simulation: Door state flipped to {'Open' if new_val == GPIO.HIGH else 'Closed'}")
            
        threading.Thread(target=_mock_door_travel, daemon=True).start()
    
    return True

def get_door_status():
    """Reads the magnetic sensor to determine door state."""
    # Logic:
    # Closed Switch (Magnet present, Door Closed) -> Pin LOW (Connected to Ground)
    # Open Switch (Magnet away, Door Open) -> Pin HIGH (Pull Up Resistor)
    state = GPIO.input(SENSOR_PIN)
    
    if state == GPIO.LOW:
        return DOOR_CLOSED
    else:
        return DOOR_OPEN

def cleanup():
    global _stop_monitoring
    _stop_monitoring = True
    if _monitor_thread:
        _monitor_thread.join(timeout=2)
    GPIO.cleanup()

# For running this file directly for testing
if __name__ == "__main__":
    setup_gpio()
    try:
        print(f"Current Status: {get_door_status()}")
        toggle_door()
        print("Waiting 2 seconds...")
        time.sleep(2)
        print(f"Current Status: {get_door_status()}")
    finally:
        cleanup()
