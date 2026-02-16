import time
import threading
import logger

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    import mock_gpio as GPIO

# Pin Configuration (BCM Mode)
RELAY_PIN = 17       # Pin connected to Relay ch 1
# Sensor Pins: Only Sensor 1 (Bottom/Closed) is used.
# Logic: Closed = Sensor 1 Active (Low). Open = Sensor 1 Inactive (High).
SENSOR_PINS = [27] 


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
            # If state changes to Open and we didn't just trigger it, it's a manual open.
            # The logger already logs "State Change". usage of this function is consistent to requirements.
            logger.log_event("State Change", current_state)
        _last_known_state = current_state
        time.sleep(1)

def setup_gpio():
    """Initialize GPIO pins."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    
    # Initialize sensor pin as Input with Pull Up
    for pin in SENSOR_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
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
    
    # Mock Simulation Logic
    if hasattr(GPIO, '_test_set_pin_state'):
        def _mock_door_travel():
            # Simulation of door travel.
            # User request: ~8-10 seconds for full travel.
            travel_time = 10.0 
            
            is_closed = (current_state == DOOR_CLOSED)
            
            if is_closed:
                # Opening: Sensor 1 (Closed) becomes Inactive immediately or after a short delay?
                # Usually as soon as door moves, sensor 1 opens. 
                # But to simulate "travel", we can wait a bit or just set it immediately implies "Opening".
                # For this simple logic: 
                # Closed -> (Door Moves) -> Sensor 1 Open -> State becomes OPEN immediately.
                # However, to simulate 'travel' visually if we had intermediate sensors, we'd wait.
                # With 1 sensor: 
                # State is Closed.
                # Relay triggers.
                # Door moves. Magnet leaves Sensor 1.
                # State becomes "Open" (or at least "Not Closed").
                
                # Let's delay slighly to simulate the mechanical startup
                time.sleep(1.0) 
                GPIO._test_set_pin_state(SENSOR_PINS[0], GPIO.HIGH) # Magnet gone
                print(f"Mock: Sensor 1 Deactivated (Door Opening/Open)")
                
                # Wait rest of travel time just for internal simulation consistency if we add more later
                time.sleep(travel_time)
                print("Mock: Door fully open (simulated time end)")

            else:
                # Closing: Door is Open (Sensor 1 High).
                # It takes ~10s to close. Sensor 1 will only trigger at the VERY END.
                print(f"Mock: Door Closing... waiting {travel_time}s")
                time.sleep(travel_time)
                
                GPIO._test_set_pin_state(SENSOR_PINS[0], GPIO.LOW) # Magnet returns
                print("Mock: Sensor 1 Activated (Door Closed)")

            
        threading.Thread(target=_mock_door_travel, daemon=True).start()
    
    return True

def get_door_status():
    """Reads the magnetic sensors to determine door state."""
    # Active = Low (GND) -> Closed
    # Inactive = High (PullUp) -> Open (or at least Not Closed)
    
    if GPIO.input(SENSOR_PINS[0]) == GPIO.LOW:
        return DOOR_CLOSED
    else:
        return DOOR_OPEN

def get_sensor_states():
    """Returns the state of the single sensor."""
    return {
        "sensor_1_bottom": GPIO.input(SENSOR_PINS[0]),
        # Keep other keys for API compatibility if needed, but set to None or 1?
        # Let's remove them to be clean, frontend handles checks.
        "sensor_2_quarter": 1,
        "sensor_3_half": 1,
        "sensor_4_top": 1
    }

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
