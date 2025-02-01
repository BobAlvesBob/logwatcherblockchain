# Blockchain Log Verification System

This project is a multi-container system that simulates a simple blockchain-based log verification process using Docker Compose. The system consists of several services:

- **MachineA:**  
  Reads/simulates log entries from a syslog folder, sends them to MachineB, and creates a blockchain block (by computing a SHA-256 hash of the log and timestamp) which it sends to the blockchain nodes.

- **MachineB:**  
  Acts as a log storage service. It receives logs from MachineA via a REST API, stores them (keyed by timestamp), and exposes endpoints to retrieve single or all log entries.

- **Blockchain Nodes (MachineC, MachineD, MachineE):**  
  These nodes maintain the blockchain. Each node accepts blocks (containing the log hash, timestamp, and previous hash) via a REST API and provides a GET endpoint to view the current blockchain.

- **Frontend:**  
  A simple web GUI served via Nginx that displays the logs (fetched from MachineB) and blockchain blocks (fetched from one of the blockchain nodes, MachineC). It also computes the SHA-256 hash for each log and compares it with the hash stored in the blockchain, showing verification results.

## Folder Structure

project/ ├── docker-compose.yml ├── machineA/ │ ├── app.py │ ├── requirements.txt │ └── Dockerfile ├── machineB/ │ ├── app.py │ ├── requirements.txt │ └── Dockerfile ├── blockchain/ │ ├── app.py │ ├── requirements.txt │ └── Dockerfile └── frontend/ ├── index.html └── Dockerfile


## How It Works

1. **MachineA** simulates a log entry (e.g., "Test syslog entry from machine A") with a timestamp and:
   - Sends the log entry to **MachineB** via a POST request to `/logs`.
   - Computes a SHA-256 hash of the concatenation of the log and its timestamp.
   - Constructs a blockchain block that includes:
     - `timestamp`
     - `log_hash` (the computed hash)
     - `previous_hash` (a fixed value for simplicity)
   - Sends the block to all blockchain nodes (**MachineC**, **MachineD**, and **MachineE**) via POST requests to `/block`.

2. **MachineB** stores the received log entries and provides the following endpoints:
   - **POST** `/logs`: Store a log entry.
   - **GET** `/logs`: Return a list of all log entries.
   - **GET** `/logs/<timestamp>`: Return a single log entry for a given timestamp.

3. **Blockchain Nodes (MachineC, MachineD, MachineE)**:
   - Accept blocks via **POST** `/block` and add them to the local blockchain.
   - Provide a **GET** `/blockchain` endpoint to view the full blockchain.

4. **Frontend GUI**:
   - Fetches the logs from **MachineB** (at `http://localhost:5001/logs`).
   - Fetches the blockchain from **MachineC** (at `http://localhost:5002/blockchain`).
   - Computes the hash for each log (using the same algorithm as MachineA) and compares it to the corresponding blockchain block hash.
   - Displays the logs, blockchain, and verification results in a user-friendly HTML page.

## Running the System

1. **Clone the Repository**  
   Clone this repository to your local machine.

2. **Build and Start the Containers**  
   Open a terminal in the project directory and run:

   ```bash
   docker-compose up --build
