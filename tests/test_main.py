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


@patch('main.time.time', return_value=1234567890.0)
def test_get_weather(mock_time):
    """Test the get_weather function."""
    
    # Create mock sensors
    mock_sds = MagicMock()
    mock_sds.get_measurement.return_value = {
        "sensor_air_quality": "sds011",
        "pm25": 10.5,
        "pm10": 25.0,
    }
    
    mock_bme = MagicMock()
    mock_bme.get_measurement.return_value = {
        "sensor_temp_hum": "bme280",
        "temperature_farenheit": 77.0,
        "temperature_celsius": 25.0,
        "humidity": 50.0,
        "pressure": 1013.25,
    }

    result = get_weather(mock_sds, mock_bme)

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

