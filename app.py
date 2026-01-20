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
    limit = request.args.get('limit', default=10, type=int)
    logs = logger.get_recent_logs(limit=limit)
    return jsonify({'logs': logs})

@app.route('/api/archives')
def get_archives():
    import logger
    archives = logger.get_archived_logs()
    return jsonify({'archives': archives})

@app.route('/api/archives/<filename>')
def get_archive_content(filename):
    import logger
    logs = logger.read_log_file(filename)
    return jsonify({'logs': logs})



if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        garage_controller.cleanup()
