from flask import Flask, render_template, jsonify, request
import garage_controller
import threading
import time

app = Flask(__name__)

# Initialize hardware on startup
garage_controller.setup_gpio()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    status = garage_controller.get_door_status()
    # In a real scenario, we might want to know if it's "Opening" or "Closing"
    # based on time since last toggle, but for now just raw sensor state.
    return jsonify({'status': status})

@app.route('/api/toggle', methods=['POST'])
def toggle_door():
    garage_controller.toggle_door()
    # Return new status immediately? It might not have changed yet if physical door is slow.
    # But we return success.
    return jsonify({'success': True, 'message': 'Door toggled'})

@app.route('/api/logs')
def get_logs():
    import logger
    logs = logger.get_recent_logs()
    return jsonify({'logs': logs})

# For testing: Route to manually set sensor state (Mock only)
@app.route('/api/debug/set_sensor/<state>')
def debug_set_sensor(state):
    """
    Debug endpoint to simulate door opening/closing.
    state: 'open' or 'closed'
    """
    try:
        import mock_gpio
        # If we are using mock_gpio, we can manipulate it.
        pin = garage_controller.SENSOR_PIN
        val = mock_gpio.LOW if state == 'closed' else mock_gpio.HIGH
        mock_gpio._test_set_pin_state(pin, val)
        return jsonify({'success': True, 'new_mock_state': state})
    except ImportError:
        return jsonify({'success': False, 'message': 'Mock GPIO not available'})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        garage_controller.cleanup()
