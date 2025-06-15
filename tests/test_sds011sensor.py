"""
Tests for the SDS011Sensor class.
"""
import pytest
from unittest.mock import patch, MagicMock

# Mock the hardware-dependent modules before importing the sensor class
import sys
sys.modules['sds011'] = MagicMock()

from src.sensors.sds011sensor import SDS011Sensor


@pytest.fixture
def mock_sds011():
    """Fixture to mock the SDS011 module."""
    with patch('src.sensors.sds011sensor.SDS011') as mock_sds:
        # Configure the mock SDS011 instance
        mock_sds_instance = MagicMock()
        mock_sds_instance.query.return_value = (10.5, 25.0)  # PM2.5, PM10
        mock_sds.return_value = mock_sds_instance

        yield mock_sds


def test_init(mock_sds011):
    """Test the initialization of the SDS011Sensor class."""
    sensor = SDS011Sensor()

    # Check that the SDS011 was initialized with the correct device path
    mock_sds011.assert_called_once_with("/dev/ttyUSB0")

    # Check that the work period was set correctly
    mock_sds011.return_value.set_work_period.assert_called_once_with(work_time=15)


def test_get_measurement(mock_sds011):
    """Test the get_measurement method."""
    sensor = SDS011Sensor()
    result = sensor.get_measurement()

    # Check that the result contains the expected keys and values
    assert result["sensor_air_quality"] == "sds011"
    assert result["pm25"] == 10.5
    assert result["pm10"] == 25.0


def test_get_pm25_pm10(mock_sds011):
    """Test the get_pm25_pm10 method."""
    sensor = SDS011Sensor()
    pm25, pm10 = sensor.get_pm25_pm10()

    # Check that the query method was called
    mock_sds011.return_value.query.assert_called_once()

    # Check that the correct values were returned
    assert pm25 == 10.5
    assert pm10 == 25.0
