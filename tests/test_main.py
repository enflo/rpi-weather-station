"""
Tests for the main module.
"""
import sys
from unittest.mock import MagicMock, patch

import pytest

# Mock the hardware-dependent modules before importing the main module
sys.modules['board'] = MagicMock()
sys.modules['adafruit_bme280'] = MagicMock()
sys.modules['adafruit_bme280.advanced'] = MagicMock()
sys.modules['sds011'] = MagicMock()

from main import get_weather  # noqa: E402


@pytest.fixture
def mock_sensors():
    """Fixture to mock the sensor classes."""
    with patch('main.SDS011Sensor') as mock_sds, \
         patch('main.BME280Sensor') as mock_bme:
        # Configure the mock sensors
        mock_sds_instance = MagicMock()
        mock_sds_instance.get_measurement.return_value = {
            "sensor_air_quality": "sds011",
            "pm25": 10.5,
            "pm10": 25.0,
        }
        mock_sds.return_value = mock_sds_instance

        mock_bme_instance = MagicMock()
        mock_bme_instance.get_measurement.return_value = {
            "sensor_temp_hum": "bme280",
            "temperature_farenheit": 77.0,
            "temperature_celsius": 25.0,
            "humidity": 50.0,
            "pressure": 1013.25,
        }
        mock_bme.return_value = mock_bme_instance

        yield


@patch('main.time.time', return_value=1234567890.0)
def test_get_weather(mock_time, mock_sensors):
    """Test the get_weather function."""
    result = get_weather()

    # Check that the result contains the expected keys
    assert "timestamp" in result
    assert "sensor_air_quality" in result
    assert "pm25" in result
    assert "pm10" in result
    assert "sensor_temp_hum" in result
    assert "temperature_farenheit" in result
    assert "temperature_celsius" in result
    assert "humidity" in result
    assert "pressure" in result

    # Check the values
    assert result["timestamp"] == 1234567890.0
    assert result["sensor_air_quality"] == "sds011"
    assert result["pm25"] == 10.5
    assert result["pm10"] == 25.0
    assert result["sensor_temp_hum"] == "bme280"
    assert result["temperature_farenheit"] == 77.0
    assert result["temperature_celsius"] == 25.0
    assert result["humidity"] == 50.0
    assert result["pressure"] == 1013.25
