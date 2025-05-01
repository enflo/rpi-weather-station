# Raspberry Pi Weather Station Development Guidelines

This document provides guidelines and instructions for developing and maintaining the Raspberry Pi Weather Station project.

## Build/Configuration Instructions

### Environment Setup

1. **Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements/local.txt  # For development
   # or
   pip install -r requirements/requirements.txt  # For production
   ```

3. **Environment Variables**:
   - Create a `.env` file in the project root with the following variables:
     ```
     ENVIRONMENT=development
     LOOP_TIME=1
     
     # API Configuration (if needed)
     API_ENABLE=False
     API_METHOD=POST
     API_HOST=localhost
     API_HEADER_TOKEN=your_token
     API_URL_TOKEN=your_url_token
     
     # MQTT Configuration (if needed)
     MQTT_ENABLE=False
     MQTT_HOST=localhost
     MQTT_PORT=1883
     MQTT_TOPIC=weather
     MQTT_USER=your_user
     MQTT_PASSWORD=your_password
     
     # SQS Configuration (if needed)
     SQS_ENABLE=False
     SQS_URL=http://localhost:9324
     SQS_ACCESS_KEY=your_access_key
     SQS_SECRET_KEY=your_secret_key
     SQS_QUEUE_NAME=your_queue_name
     SQS_REGION=your_region
     ```

### Hardware Configuration

1. **Sensors**:
   - BME280 (Temperature, Humidity, Pressure): Connect via I2C (address 0x77)
   - SDS011 (Air Quality): Connect via USB (device path `/dev/ttyUSB0`)

2. **Raspberry Pi Setup**:
   - Enable I2C interface using `raspi-config`
   - Ensure USB ports are accessible

### Running the Application

1. **Manual Start**:
   ```bash
   python main.py
   ```

2. **Service Installation**:
   ```bash
   sudo cp scripts/weather.station.service /etc/systemd/system/
   sudo systemctl enable weather.station
   sudo systemctl start weather.station
   ```

## Testing Information

### Running Tests

1. **Install Test Dependencies**:
   ```bash
   pip install -r requirements/local.txt
   ```

2. **Run All Tests**:
   ```bash
   python -m pytest
   ```

3. **Run Specific Tests**:
   ```bash
   python -m pytest tests/test_utils.py
   ```

4. **Run Tests with Verbosity**:
   ```bash
   python -m pytest -v
   ```

### Adding New Tests

1. **Create Test Files**:
   - Place test files in the `tests` directory
   - Name test files with the prefix `test_`
   - Name test functions with the prefix `test_`

2. **Test Structure**:
   - Import the module to test
   - Write test functions that use assertions
   - Group related tests in the same file

3. **Example Test**:
   ```python
   # tests/test_example.py
   import pytest
   from src.module import function_to_test

   def test_function():
       assert function_to_test(input) == expected_output
   ```

4. **Mocking Sensors**:
   - For testing code that depends on physical sensors, use the `unittest.mock` module or `pytest-mock`
   - Example:
     ```python
     def test_sensor_reading(mocker):
         # Mock the sensor reading
         mocker.patch('src.sensors.bme280sensor.BME280Sensor._get_data', 
                     return_value=mock_data)
         
         # Test the function that uses the sensor
         result = get_weather()
         assert result['temperature_celsius'] == expected_value
     ```

## Code Style and Development Guidelines

### Code Formatting

1. **Run Formatters**:
   ```bash
   make format
   ```
   This will run:
   - `black`: Code formatter
   - `isort`: Import sorter
   - `flake8`: Linter

2. **Type Checking**:
   ```bash
   # Uncomment the mypy line in the Makefile first
   make format
   ```

### Development Workflow

1. **Feature Development**:
   - Create a new branch for each feature
   - Write tests before implementing features
   - Run tests frequently during development
   - Format code before committing

2. **Debugging**:
   - Check logs for errors
   - Use `print` statements or logging for debugging
   - For sensor issues, check connections and permissions

3. **Deployment**:
   - Test on a development Raspberry Pi first
   - Update the service file if necessary
   - Restart the service after deployment