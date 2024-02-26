import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def handle_get_request():
    try:
        with open('log.json', 'r') as data_log:
            data = json.load(data_log)
            data_log.close()
            return json.dumps(data)
    except Exception as e:
        print(f"Error loading json: {e}")

if __name__ == "__main__":
    app.run(port=5002, debug = True)