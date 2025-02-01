from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

logs = {}  # Logs stored as key-value pairs (timestamp: log)

@app.route('/logs', methods=['POST'])
def store_log():
    data = request.get_json()
    log = data.get("log")
    timestamp = data.get("timestamp")
    logs[timestamp] = log
    return jsonify({"status": "log stored", "timestamp": timestamp})

@app.route('/logs/<timestamp>', methods=['GET'])
def get_log(timestamp):
    log = logs.get(timestamp)
    if log:
        return jsonify({"timestamp": timestamp, "log": log})
    else:
        return jsonify({"error": "log not found"}), 404

@app.route('/logs', methods=['GET'])
def list_logs():
    result = []
    for timestamp, log in logs.items():
        result.append({"timestamp": timestamp, "log": log})
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
