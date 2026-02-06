import sys
from unittest.mock import MagicMock, patch

# Mock influxdb_client before importing the module under test
# This is necessary because the package might not be installed in the test environment
mock_influxdb = MagicMock()
sys.modules["influxdb_client"] = mock_influxdb
sys.modules["influxdb_client.client"] = MagicMock()
sys.modules["influxdb_client.client.write_api"] = MagicMock()
sys.modules["influxdb_client.rest"] = MagicMock()

import pytest
from src.communication.influxdb import InfluxDBWrapper, SendDataInfluxDB

@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset the singleton instance before each test."""
    from src.communication import influxdb
    influxdb._influx_wrapper_instance = None
    yield
    influxdb._influx_wrapper_instance = None

@pytest.fixture
def sample_data():
    return {
        "sensor_temp_hum": "bme280",
        "temperature_celsius": 25.0,
        "humidity": 50.0,
        "pressure": 1013.25,
        "pm25": 10.5,
        "pm10": 25.0,
        "sensor_air_quality": "sds011",
    }

@patch("src.communication.influxdb.InfluxDBClient")
def test_connect(mock_client_class):
    """Test connection initialization."""
    # Mock health check to pass
    mock_client = MagicMock()
    mock_client.health.return_value.status = "pass"
    mock_client_class.return_value = mock_client

    wrapper = InfluxDBWrapper()
    wrapper.connect()
    
    mock_client_class.assert_called_once()
    assert wrapper._client is not None
    mock_client.write_api.assert_called_once()

@patch("src.communication.influxdb.InfluxDBClient")
def test_write_data(mock_client_class, sample_data):
    """Test writing data to InfluxDB."""
    mock_client = MagicMock()
    mock_write_api = MagicMock()
    mock_client.write_api.return_value = mock_write_api
    mock_client.health.return_value.status = "pass"
    mock_client_class.return_value = mock_client
    
    wrapper = InfluxDBWrapper()
    wrapper.write_data(sample_data)
    
    mock_write_api.write.assert_called_once()
    args, kwargs = mock_write_api.write.call_args
    assert kwargs['bucket'] == wrapper.bucket
    assert len(kwargs['record']) == 1
    
    # Check that points were created correctly
    point = kwargs['record'][0]
    # Depending on implementation, we can check basic properties if accessible
    # But usually just ensuring write is called with a list of points is enough for unit test

def test_validate_data_valid(sample_data):
    """Test data validation with valid data."""
    wrapper = InfluxDBWrapper()
    assert wrapper.validate_data(sample_data) is True

def test_validate_data_invalid():
    """Test data validation with invalid data."""
    wrapper = InfluxDBWrapper()
    assert wrapper.validate_data({}) is False
    assert wrapper.validate_data(None) is False
    assert wrapper.validate_data({"unknown_field": 123}) is False
    # Data with some valid fields should be valid
    assert wrapper.validate_data({"temperature_celsius": 20}) is True

@patch("src.communication.influxdb.InfluxDBWrapper")
def test_send_data_influxdb(mock_wrapper_class, sample_data):
    """Test the SendDataInfluxDB adapter."""
    mock_wrapper = MagicMock()
    mock_wrapper_class.return_value = mock_wrapper
    
    sender = SendDataInfluxDB(sample_data)
    sender.send()
    
    mock_wrapper.write_data.assert_called_once_with(sample_data)

@patch("src.communication.influxdb.InfluxDBClient")
def test_read_data(mock_client_class):
    """Test reading data."""
    mock_client = MagicMock()
    mock_query_api = MagicMock()
    mock_client.query_api.return_value = mock_query_api
    mock_client.health.return_value.status = "pass"
    mock_client_class.return_value = mock_client
    
    wrapper = InfluxDBWrapper()
    query = 'from(bucket: "test") |> range(start: -1h)'
    wrapper.read_data(query)
    
    mock_query_api.query.assert_called_once_with(org=wrapper.org, query=query)
