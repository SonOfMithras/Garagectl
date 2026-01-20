import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MockGPIO")

BCM = "BCM"
OUT = "OUT"
IN = "IN"
HIGH = 1
LOW = 0
PUD_UP = "PUD_UP"

_pin_states = {}

def setmode(mode):
    logger.info(f"Set mode to {mode}")

def setup(pin, mode, pull_up_down=None):
    mode_str = "OUT" if mode == OUT else "IN"
    pud_str = f" with {pull_up_down}" if pull_up_down else ""
    logger.info(f"Setup Pin {pin} as {mode_str}{pud_str}")
    
    # Initialize state (Default to LOW for OUT, HIGH for IN if PUD_UP is used - simplifying assumption)
    if pin not in _pin_states:
        _pin_states[pin] = LOW

def output(pin, state):
    state_str = "HIGH" if state == HIGH else "LOW"
    logger.info(f"Set Pin {pin} to {state_str}")
    _pin_states[pin] = state

def input(pin):
    val = _pin_states.get(pin, LOW)
    # logger.info(f"Read Pin {pin}: {val}") # Commented out to reduce noise during polling
    return val

def cleanup():
    logger.info("Cleanup GPIO")
    _pin_states.clear()

# Helper for testing to manually set state
def _test_set_pin_state(pin, state):
    logger.info(f"[TEST] Manually setting mock pin {pin} to {state}")
    _pin_states[pin] = state
