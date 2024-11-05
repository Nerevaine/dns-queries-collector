# DNS Queries Collector

DNS Queries Collector is a Python application that parses DNS query logs from a BIND server, processes the data, and sends it in batches to the Lumu Custom Collector API. Additionally, the application generates statistics on the data, including rankings of client IPs and queried hosts.

## Project Structure

- `config/`: Configuration management for environment variables.
- `utils/`: Utility modules, including logging configuration.
- `log_parser.py`: Parses DNS query logs and extracts relevant data.
- `lumu_api_client.py`: Manages communication with the Lumu API, sending data in batches with retry logic.
- `stats.py`: Generates and displays statistics on parsed DNS data, including rankings.

## Computational Complexity

The ranking algorithm in `stats.py` uses Python’s `Counter` from the `collections` module to calculate the frequency of each IP address and host in the parsed data. The complexity of this operation is as follows:

1. **Counting Frequencies**:
   - Each record is processed once, resulting in **O(n)** complexity, where `n` is the number of records.

2. **Ranking**:
   - Sorting the frequency counts for the top results (e.g., top 5) is **O(k log k)**, where `k` is the number of unique IPs or hosts.
   - Since `k` is generally much smaller than `n`, the overall complexity remains **O(n)**, making the algorithm efficient for large datasets.

## Setup and Installation

### Prerequisites

- **Python 3.8+**
- **Docker** and **Docker Compose** (optional for containerized deployment)

### Local Installation

1. **Clone the repository**:
```bash
   git clone https://github.com/Nerevaine/dns-queries-collector.git
   cd dns-queries-collector
```

2. **Create a virtual environment**:

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Set up the .env file**:

Create a .env file in the project root with the following variables:

```bash
LUMU_CLIENT_KEY=your-lumu-client-key
COLLECTOR_ID=your-collector-id
BATCH_SIZE=500
LOG_LEVEL=INFO
LOG_FILE=app.log
```

## Running the Application

To execute the application locally:

```bash
python src/main.py
```

This command processes the default data/sample.log file, sends the data to the Lumu API, and prints statistics in the console.

## Docker Deployment

### Dockerfile

The Dockerfile uses Python 3.8 as the base image, installs dependencies, and copies the application files. The .env file is required to pass sensitive data without hardcoding keys directly in the Dockerfile.

### Docker Compose

The docker-compose.yml file simplifies deployment. Environment variables are passed to the container from the .env file, and the data/ directory is mounted for log access.

Running with Docker Compose

1. **Build and run the container**:

```bash
docker-compose up --build
``` 
This command builds the Docker image, starts the container, and mounts the data/ directory inside the container at /app/data.

2.	**Accessing Logs**:
Check app.log as specified in the .env file, or view logs directly in the console when using Docker Compose.

