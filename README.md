# Home Environment Monitor

A lightweight home server that reads temperature and humidity from a DHT11 sensor via Arduino, logs the data to a SQLite database, and displays it on a live web dashboard.

## Features

- Live temperature and humidity readings updated every 5 seconds
- Historical data graph
- Data logged to SQLite every 30 seconds
- REST API for raw data access
- Fully containerised with Docker

## Hardware

| Component | Details |
|---|---|
| Sensor | DHT11 temperature and humidity sensor |
| Microcontroller | Arduino Uno R3 |
| Server | Raspberry Pi |

The Arduino reads from the DHT11 and sends data over serial to the Pi, which logs it to the database.

## Project Structure

```
home_server/
├── docker-compose.yml
├── classes.py              # Shared classes (Database, Analyser, DataLogger, etc.)
├── .env                    # Environment variables (not tracked in Git)
├── data/
│   └── weather.db          # SQLite database (not tracked in Git)
├── collector/
│   ├── Dockerfile
│   └── main.py             # Reads from Arduino, writes to database
├── web/
│   ├── Dockerfile
│   ├── app.py              # Flask web server
│   └── templates/
│       └── index.html      # Dashboard
└── cli/
    └── cli.py              # Local device manager CLI
```

## Running the Project

### Prerequisites
- Docker and Docker Compose installed
- Arduino connected via USB serial

### Setup

1. Clone the repository:
```bash
git clone git@github.com:yourusername/home_server.git
cd home_server
```

2. Create a `.env` file in the project root (see Environment Variables below)

3. Build and start the containers:
```bash
docker compose up --build
```

4. Open the dashboard in your browser:
```
http://<your-pi-ip>:5000
```

To run in the background:
```bash
docker compose up --build -d
```

To stop:
```bash
docker compose down
```

## Environment Variables

Create a `.env` file at the project root with the following:

```
DB_FILE=/app/data/weather.db
SERIAL_PORT=/dev/ttyACM0
FLASK_PORT=5000
```

| Variable | Description |
|---|---|
| `DB_FILE` | Path to the SQLite database inside the container |
| `SERIAL_PORT` | Serial port the Arduino is connected to |
| `FLASK_PORT` | Port the web dashboard is served on |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Web dashboard |
| GET | `/api/weather` | Latest temperature and humidity reading |
| GET | `/api/weather/history` | All historical readings |

### Example Response — `/api/weather`

```json
{
  "temperature": 22.4,
  "humidity": 54.1,
  "timestamp": "2026-04-06T13:07:02"
}
```

## Development Workflow

Changes are developed locally, pushed to GitHub, then pulled and rebuilt on the Pi:

```bash
# On your PC
git add .
git commit -m "your message"
git push

# On the Pi
git pull
docker compose up --build
```
