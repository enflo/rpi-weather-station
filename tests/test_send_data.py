"""
Tests for the send_data module.
"""
import pytest
from unittest.mock import patch, MagicMock

from src.communication.send_data import send_data


@pytest.fixture
def sample_data():
    """Fixture to provide sample weather data."""
    return {
        "timestamp": 1234567890.0,
        "sensor_air_quality": "sds011",
        "pm25": 10.5,
        "pm10": 25.0,
        "sensor_temp_hum": "bme280",
        "temperature_farenheit": 77.0,
        "temperature_celsius": 25.0,
        "humidity": 50.0,
        "pressure": 1013.25,
    }


@patch('src.communication.send_data.API_ENABLE', True)
@patch('src.communication.send_data.MQTT_ENABLE', False)
@patch('src.communication.send_data.SQS_ENABLE', False)
@patch('src.communication.send_data.POSTGRES_ENABLE', False)
@patch('src.communication.send_data.SendDataAPI')
def test_send_data_api(mock_api, sample_data):
    """Test send_data function with API_ENABLE=True."""
    # Configure the mock
    mock_api_instance = MagicMock()
    mock_api.return_value = mock_api_instance
    
    # Call the function
    send_data(sample_data)
    
    # Check that SendDataAPI was called with the correct data
    mock_api.assert_called_once_with(sample_data)
    # Check that send() was called on the instance
    mock_api_instance.send.assert_called_once()


@patch('src.communication.send_data.API_ENABLE', False)
@patch('src.communication.send_data.MQTT_ENABLE', True)
@patch('src.communication.send_data.SQS_ENABLE', False)
@patch('src.communication.send_data.POSTGRES_ENABLE', False)
@patch('src.communication.send_data.SendDataMQTT')
def test_send_data_mqtt(mock_mqtt, sample_data):
    """Test send_data function with MQTT_ENABLE=True."""
    # Configure the mock
    mock_mqtt_instance = MagicMock()
    mock_mqtt.return_value = mock_mqtt_instance
    
    # Call the function
    send_data(sample_data)
    
    # Check that SendDataMQTT was called with the correct data
    mock_mqtt.assert_called_once_with(sample_data)
    # Check that send() was called on the instance
    mock_mqtt_instance.send.assert_called_once()


@patch('src.communication.send_data.API_ENABLE', False)
@patch('src.communication.send_data.MQTT_ENABLE', False)
@patch('src.communication.send_data.SQS_ENABLE', True)
@patch('src.communication.send_data.POSTGRES_ENABLE', False)
@patch('src.communication.send_data.SQSClient')
def test_send_data_sqs(mock_sqs, sample_data):
    """Test send_data function with SQS_ENABLE=True."""
    # Configure the mock
    mock_sqs_instance = MagicMock()
    mock_sqs.return_value = mock_sqs_instance
    
    # Call the function
    send_data(sample_data)
    
    # Check that SQSClient was called with the correct data
    mock_sqs.assert_called_once_with(sample_data)
    # Check that send() was called on the instance
    mock_sqs_instance.send.assert_called_once()


@patch('src.communication.send_data.API_ENABLE', False)
@patch('src.communication.send_data.MQTT_ENABLE', False)
@patch('src.communication.send_data.SQS_ENABLE', False)
@patch('src.communication.send_data.POSTGRES_ENABLE', True)
@patch('src.communication.send_data.SendDataPostgres')
def test_send_data_postgres(mock_postgres, sample_data):
    """Test send_data function with POSTGRES_ENABLE=True."""
    # Configure the mock
    mock_postgres_instance = MagicMock()
    mock_postgres.return_value = mock_postgres_instance
    
    # Call the function
    send_data(sample_data)
    
    # Check that SendDataPostgres was called with the correct data
    mock_postgres.assert_called_once_with(sample_data)
    # Check that send() was called on the instance
    mock_postgres_instance.send.assert_called_once()


@patch('src.communication.send_data.API_ENABLE', False)
@patch('src.communication.send_data.MQTT_ENABLE', False)
@patch('src.communication.send_data.SQS_ENABLE', False)
@patch('src.communication.send_data.POSTGRES_ENABLE', False)
@patch('builtins.print')
def test_send_data_print(mock_print, sample_data):
    """Test send_data function with all options disabled."""
    # Call the function
    send_data(sample_data)
    
    # Check that print was called with the correct data
    mock_print.assert_called_once_with(sample_data)