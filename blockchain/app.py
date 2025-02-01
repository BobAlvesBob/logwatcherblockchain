from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable cross-origin requests

app = Flask(__name__)
CORS(app)

blockchain = []

@app.route('/block', methods=['POST'])
def add_block():
    block = request.get_json()
    blockchain.append(block)
    return jsonify({"status": "block added", "block": block})

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    return jsonify(blockchain)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
