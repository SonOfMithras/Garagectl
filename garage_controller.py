import time
import threading
import logger

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    import mock_gpio as GPIO

# Pin Configuration (BCM Mode)
RELAY_PIN = 17       # Pin connected to Relay ch 1
# Sensor Pins: Bottom (0%), 25%, 50%, Top (100%)
# Logic: Closed = All Active. Open = Only Top Active (or none if fully clear) based on user req.
# User Req: 
# Closed: 1,2,3,4 Active
# Ajar: 2,3,4 Active
# Partial: 3,4 Active
# Open: 4 Active (or maybe none? User said "only sensor 4 is active = fully open")
SENSOR_PINS = [27, 22, 23, 24] 


# State Constants
DOOR_OPEN = "Open"
DOOR_CLOSED = "Closed"
DOOR_AJAR = "Ajar"
DOOR_PARTIAL = "Partially Open"
DOOR_OPEN = "Open"
DOOR_MOVING = "Moving"

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
    
    # Initialize all sensor pins as Input with Pull Up
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
    
    # Mock Simulation Logic: If using Mock GPIO, simulate travel
    if hasattr(GPIO, '_test_set_pin_state'):
        def _mock_door_travel():
            # Total travel time requested ~4s. We have 4 states to transition.
            # If Closed: Closed -> Ajar -> Partial -> Open
            # If Open: Open -> Partial -> Ajar -> Closed
            
            step_delay = 1.0 # 4 steps * 1s = 4s total
            
            is_opening = (current_state == DOOR_CLOSED or current_state == DOOR_AJAR) 
            
            if is_opening:
                # Sequence: 
                # Start: All Low (Closed)
                # Step 1: Pin 27 High (Ajar)
                time.sleep(step_delay)
                GPIO._test_set_pin_state(SENSOR_PINS[0], GPIO.HIGH)
                print("Mock: Uncovered Sensor 1 (Ajar)")

                # Step 2: Pin 22 High (Partial)
                time.sleep(step_delay)
                GPIO._test_set_pin_state(SENSOR_PINS[1], GPIO.HIGH)
                print("Mock: Uncovered Sensor 2 (Partial)")
                
                # Step 3: Pin 23 High (Open - waiting for last one?)
                # Logic says "Only Sensor 4 is active = Fully Open". 
                # So Sensor 3 must become Inactive (High).
                time.sleep(step_delay)
                GPIO._test_set_pin_state(SENSOR_PINS[2], GPIO.HIGH) 
                print("Mock: Uncovered Sensor 3 (Open)")
                
            else:
                # Closing Sequence: Re-activate sensors from top down
                # Start: Only 24 Low (Open)
                
                # Step 1: Activate 23 (Partial) -> Pin 23 Low
                time.sleep(step_delay)
                GPIO._test_set_pin_state(SENSOR_PINS[2], GPIO.LOW)
                print("Mock: Covered Sensor 3 (Partial)")

                # Step 2: Activate 22 (Ajar) -> Pin 22 Low
                time.sleep(step_delay)
                GPIO._test_set_pin_state(SENSOR_PINS[1], GPIO.LOW)
                print("Mock: Covered Sensor 2 (Ajar)")

                # Step 3: Activate 27 (Closed) -> Pin 27 Low
                time.sleep(step_delay)
                GPIO._test_set_pin_state(SENSOR_PINS[0], GPIO.LOW)
                print("Mock: Covered Sensor 1 (Closed)")

            
        threading.Thread(target=_mock_door_travel, daemon=True).start()
    
    return True

def get_door_status():
    """Reads the magnetic sensors to determine door state."""
    # Active = Low (GND)
    # Inactive = High (PullUp)
    
    s1 = GPIO.input(SENSOR_PINS[0]) # Bottom
    s2 = GPIO.input(SENSOR_PINS[1])
    s3 = GPIO.input(SENSOR_PINS[2])
    s4 = GPIO.input(SENSOR_PINS[3]) # Top
    
    # Logic:
    # Closed: All Low
    if s1 == GPIO.LOW and s2 == GPIO.LOW and s3 == GPIO.LOW and s4 == GPIO.LOW:
        return DOOR_CLOSED
    
    # Ajar: 1 High, rest Low
    if s1 == GPIO.HIGH and s2 == GPIO.LOW and s3 == GPIO.LOW and s4 == GPIO.LOW:
        return DOOR_AJAR
        
    # Partial: 1,2 High, rest Low
    if s1 == GPIO.HIGH and s2 == GPIO.HIGH and s3 == GPIO.LOW and s4 == GPIO.LOW:
        return DOOR_PARTIAL
        
    # Open: 1,2,3 High, 4 Low
    if s1 == GPIO.HIGH and s2 == GPIO.HIGH and s3 == GPIO.HIGH and s4 == GPIO.LOW:
        return DOOR_OPEN

    # If 4 is also High (Door totally gone?) -> Open? Or Moving?
    # Or intermediate states (e.g. 1 High, 2 Low, 3 High? Implementation error or Moving)
    return DOOR_MOVING

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
