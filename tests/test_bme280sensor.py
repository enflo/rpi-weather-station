"""
Tests for the BME280Sensor class.
"""
import pytest
from unittest.mock import patch, MagicMock

# Mock the hardware-dependent modules before importing the sensor class
import sys
sys.modules['board'] = MagicMock()
sys.modules['adafruit_bme280'] = MagicMock()
sys.modules['adafruit_bme280.advanced'] = MagicMock()

from src.sensors.bme280sensor import BME280Sensor


@pytest.fixture
def mock_adafruit_bme280():
    """Fixture to mock the adafruit_bme280 module."""
    with patch('src.sensors.bme280sensor.adafruit_bme280') as mock_bme280, \
         patch('src.sensors.bme280sensor.board') as mock_board:
        # Configure the mock I2C
        mock_i2c = MagicMock()
        mock_board.I2C.return_value = mock_i2c

        # Configure the mock sensor
        mock_sensor = MagicMock()
        mock_sensor.temperature = 25.0
        mock_sensor.humidity = 50.0
        mock_sensor.pressure = 1013.25

        # Configure the mock Adafruit_BME280_I2C class
        mock_bme280.Adafruit_BME280_I2C.return_value = mock_sensor

        # Set up the mode constants
        mock_bme280.MODE_NORMAL = 1
        mock_bme280.STANDBY_TC_500 = 2
        mock_bme280.IIR_FILTER_X16 = 3
        mock_bme280.OVERSCAN_X16 = 4
        mock_bme280.OVERSCAN_X1 = 5
        mock_bme280.OVERSCAN_X2 = 6

        yield mock_sensor


def test_init(mock_adafruit_bme280):
    """Test the initialization of the BME280Sensor class."""
    sensor = BME280Sensor()

    # Check that the sensor was initialized with the correct address
    assert sensor.address == 0x77

    # Check that the sensor was configured correctly
    assert sensor.sensor.sea_level_pressure == 1013.25
    assert sensor.sensor.mode == 1  # MODE_NORMAL
    assert sensor.sensor.standby_period == 2  # STANDBY_TC_500
    assert sensor.sensor.iir_filter == 3  # IIR_FILTER_X16
    assert sensor.sensor.overscan_pressure == 4  # OVERSCAN_X16
    assert sensor.sensor.overscan_humidity == 5  # OVERSCAN_X1
    assert sensor.sensor.overscan_temperature == 6  # OVERSCAN_X2


def test_get_measurement(mock_adafruit_bme280):
    """Test the get_measurement method."""
    sensor = BME280Sensor()
    result = sensor.get_measurement()

    # Check that the result contains the expected keys and values
    assert result["sensor_temp_hum"] == "bme280"
    assert result["temperature_farenheit"] == 77.0  # 25.0 * (9/5) + 32
    assert result["temperature_celsius"] == 25.0
    assert result["humidity"] == 50.0
    assert result["pressure"] == 1013.25


def test_get_data(mock_adafruit_bme280):
    """Test the _get_data method."""
    sensor = BME280Sensor()
    result = sensor._get_data()

    # Check that the result is the sensor object
    assert result == sensor.sensor
