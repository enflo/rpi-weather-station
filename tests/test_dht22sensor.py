"""
Tests for the DHT22Sensor class.
"""
import pytest
from unittest.mock import patch, MagicMock, PropertyMock

# Mock the hardware-dependent modules before importing the sensor class
import sys
sys.modules['board'] = MagicMock()
sys.modules['adafruit_dht'] = MagicMock()

from src.sensors.dht22sensor import DHT22Sensor


@pytest.fixture
def mock_adafruit_dht():
    """Fixture to mock the adafruit_dht module."""
    with patch('src.sensors.dht22sensor.adafruit_dht') as mock_dht, \
         patch('src.sensors.dht22sensor.board') as mock_board:
        # Configure the mock DHT22 instance
        mock_dht_instance = MagicMock()
        mock_dht_instance.temperature = 25.0
        mock_dht_instance.humidity = 50.0
        mock_dht.DHT22.return_value = mock_dht_instance

        # Configure the board pin
        mock_board.D4 = 4

        yield mock_dht_instance


def test_init(mock_adafruit_dht):
    """Test the initialization of the DHT22Sensor class."""
    sensor = DHT22Sensor()

    # Check that the DHT22 was initialized with the correct pin and use_pulseio=False
    from src.sensors.dht22sensor import adafruit_dht, board
    adafruit_dht.DHT22.assert_called_once_with(board.D4, False)


def test_get_measurement(mock_adafruit_dht):
    """Test the get_measurement method."""
    sensor = DHT22Sensor()
    result = sensor.get_measurement()

    # Check that the result contains the expected keys and values
    assert result["sensor_temp_hum"] == "dht22"
    assert result["temperature_farenheit"] == 77.0  # 25.0 * (9/5) + 32
    assert result["temperature_celsius"] == 25.0
    assert result["humidity"] == 50.0


def test_get_temperature_humidity(mock_adafruit_dht):
    """Test the get_temperature_humidity method."""
    sensor = DHT22Sensor()
    temperature_f, temperature_c, humidity = sensor.get_temperature_humidity()

    # Check that the correct values were returned
    assert temperature_f == 77.0  # 25.0 * (9/5) + 32
    assert temperature_c == 25.0
    assert humidity == 50.0


def test_get_temperature_humidity_runtime_error(mock_adafruit_dht):
    """Test the get_temperature_humidity method with a RuntimeError."""
    # Configure the mock to raise a RuntimeError when temperature is accessed
    type(mock_adafruit_dht).temperature = PropertyMock(side_effect=RuntimeError("Test error"))

    sensor = DHT22Sensor()
    temperature_f, temperature_c, humidity = sensor.get_temperature_humidity()

    # Check that None values were returned
    assert temperature_f is None
    assert temperature_c is None
    assert humidity is None


def test_get_temperature_humidity_exception(mock_adafruit_dht):
    """Test the get_temperature_humidity method with a general Exception."""
    # Configure the mock to raise an Exception when temperature is accessed
    type(mock_adafruit_dht).temperature = PropertyMock(side_effect=Exception("Test error"))

    sensor = DHT22Sensor()
    temperature_f, temperature_c, humidity = sensor.get_temperature_humidity()

    # Check that None values were returned
    assert temperature_f is None
    assert temperature_c is None
    assert humidity is None
