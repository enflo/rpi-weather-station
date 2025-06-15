# Raspberry Pi Weather Station

A comprehensive weather station project for Raspberry Pi that collects data from various sensors and can send it to different destinations like APIs, MQTT brokers, SQS queues, or PostgreSQL databases.

## Features

- Collects temperature, humidity, and pressure data from BME280 sensors
- Measures air quality (PM2.5 and PM10) using SDS011 sensors
- Flexible data output options:
  - Console output
  - API endpoints
  - MQTT brokers
  - AWS SQS queues
  - PostgreSQL databases
- Configurable measurement intervals
- Runs as a system service

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- BME280 sensor (for temperature, humidity, and pressure)
- SDS011 sensor (for air quality measurements)
- Appropriate wiring and connections

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/rpi-weather-station.git
cd rpi-weather-station
```

### Set Up Environment

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

2. Install dependencies:

```bash
pip install -r requirements/requirements.txt  # For production
# or
pip install -r requirements/local.txt  # For development
```

3. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your specific configuration
```

### Install as a Service (Optional)

To run the weather station as a system service on boot:

```bash
sudo cp scripts/weather.station.service /etc/systemd/system/
sudo systemctl enable weather.station
sudo systemctl start weather.station
```

## Configuration

All configuration is done through environment variables in the `.env` file. See [Environment Variables](#environment-variables) for details.

### Environment Variables

#### General Configuration
- `ENVIRONMENT`: Set to "development" or "production" (default: "development")
- `LOOP_TIME`: Time in seconds between sensor readings (default: 1)

#### API Configuration
- `API_ENABLE`: Enable/disable API integration (default: False)
- `API_METHOD`: HTTP method for API requests (default: "POST")
- `API_HOST`: API host URL (default: "localhost")
- `API_HEADER_TOKEN`: API header token for authentication (default: None)
- `API_URL_TOKEN`: API URL token (default: "")

#### MQTT Configuration
- `MQTT_ENABLE`: Enable/disable MQTT integration (default: False)
- `MQTT_HOST`: MQTT broker host (default: "localhost")
- `MQTT_PORT`: MQTT broker port (default: 1883)
- `MQTT_TOPIC`: MQTT topic to publish to (default: "topic")
- `MQTT_USER`: MQTT username (default: "user")
- `MQTT_PASSWORD`: MQTT password (default: "password")

#### SQS Configuration
- `SQS_ENABLE`: Enable/disable SQS integration (default: False)
- `SQS_URL`: SQS URL (default: "http://localhost:9324")
- `SQS_ACCESS_KEY`: SQS access key (default: "access_key")
- `SQS_SECRET_KEY`: SQS secret key (default: "secret_key")
- `SQS_QUEUE_NAME`: SQS queue name (default: "queue_name")
- `SQS_REGION`: SQS region (default: "fr-par")

#### PostgreSQL Configuration
- `POSTGRES_ENABLE`: Enable/disable PostgreSQL integration (default: False)
- `POSTGRES_USER`: PostgreSQL username (default: "postgres")
- `POSTGRES_PASSWORD`: PostgreSQL password (default: "postgres")
- `POSTGRES_HOST`: PostgreSQL host (default: "localhost")
- `POSTGRES_PORT`: PostgreSQL port (default: "5432")
- `POSTGRES_DBNAME`: PostgreSQL database name (default: "postgres")
- `POSTGRES_TABLE`: PostgreSQL table name for storing data (default: "weather_data")

## Usage

### Running Manually

```bash
python main.py
```

### Checking Service Status

If installed as a service:

```bash
sudo systemctl status weather.station
```

## Development

### Setting Up Development Environment

```bash
pip install -r requirements/local.txt
```

### Code Formatting and Linting

```bash
make format
```

### Running Tests

```bash
make test
# or
python -m pytest
```

The project includes comprehensive tests for all modules and methods. The tests use pytest fixtures and unittest.mock to mock external dependencies, allowing the tests to run without needing the actual hardware sensors or external services.

#### Test Coverage

- **Utility Functions**: Tests for temperature conversion functions
- **Sensor Classes**: Tests for BME280, SDS011, and DHT22 sensor classes
- **Communication Classes**: Tests for API, MQTT, PostgreSQL, and SQS communication
- **Main Module**: Tests for the main weather data collection function

#### Writing New Tests

When adding new functionality, please also add corresponding tests. Follow these guidelines:

1. Create a test file in the `tests` directory with the naming convention `test_*.py`
2. Use pytest fixtures to set up test dependencies
3. Use unittest.mock to mock external dependencies
4. Test both normal operation and error handling
5. Run the tests to ensure they pass

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all the contributors who have helped with this project
- Inspiration from various weather station projects
