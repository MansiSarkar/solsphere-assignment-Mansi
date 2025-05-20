from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

DATA_FILE = 'storage.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/report', methods=['POST'])
def report():
    incoming = request.json
    if 'machine_id' not in incoming:
        return jsonify({'error': 'Missing machine_id'}), 400

    data = load_data()
    machine_id = incoming['machine_id']
    incoming['last_check_in'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data[machine_id] = incoming
    save_data(data)
    return jsonify({'status': 'OK'})

@app.route('/ping')
def ping():
    return "pong"

@app.route('/machines', methods=['GET'])
def machines():
    data = load_data()
    return jsonify(list(data.values()))

if __name__ == '__main__':
    app.run(debug=True)
