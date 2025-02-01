import requests
import hashlib
from datetime import datetime

def hash_log(log, timestamp):
    # Compute SHA256 hash of log + timestamp
    return hashlib.sha256(f"{log}{timestamp}".encode()).hexdigest()

def send_log_to_B(log, timestamp):
    url = "http://machineb:5000/logs"
    data = {"log": log, "timestamp": timestamp}
    response = requests.post(url, json=data)
    return response.json()

def send_block_to_blockchain(block):
    # Send block to each blockchain node
    nodes = ["machinec", "machined", "machinee"]
    responses = {}
    for node in nodes:
        url = f"http://{node}:5000/block"
        res = requests.post(url, json=block)
        responses[node] = res.json()
    return responses

def main():
    log = "Test syslog entry from machine A"
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    # Send log to MachineB
    log_response = send_log_to_B(log, timestamp)
    print("Log response:", log_response)
    
    # Create block with log hash
    log_hash = hash_log(log, timestamp)
    previous_hash = "0000000000000000000000000000000000000000000000000000000000000000"
    block = {
        "timestamp": timestamp,
        "log_hash": log_hash,
        "previous_hash": previous_hash
    }
    
    blockchain_responses = send_block_to_blockchain(block)
    print("Blockchain responses:", blockchain_responses)

if __name__ == '__main__':
    main()
