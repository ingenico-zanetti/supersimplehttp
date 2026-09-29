import sys
import threading
from collections import deque
from flask import Flask, Response

app = Flask(__name__)

# Automatically maintains only the last 8 lines in memory
lines_queue = deque(maxlen=8)
queue_lock = threading.Lock()

def stdin_reader_thread():
    """Blocks on stdin and appends raw text lines to the queue."""
    for line in sys.stdin:
        with queue_lock:
            lines_queue.append(line)

@app.route('/metrics', methods=['GET'])
def get_metrics():
    def generate_lines():
        # Safely snapshot the lines under lock to prevent mid-stream modifications
        with queue_lock:
            snapshot = list(lines_queue)
        
        # Yield each line directly to the streaming engine without joining
        for line in snapshot:
            yield line

    # Return a streaming response
    return Response(generate_lines(), mimetype='text/plain')

if __name__ == '__main__':
    watcher = threading.Thread(target=stdin_reader_thread, daemon=True)
    watcher.start()
    
    app.run(host='0.0.0.0', port=8080)

