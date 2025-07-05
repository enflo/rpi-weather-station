"""
Tests for the SendDataMQTT class.
"""
from unittest.mock import MagicMock, patch

import pytest
from src.communication.mqtt import SendDataMQTT


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


@patch('src.communication.mqtt.mqtt.Client')
@patch('src.communication.mqtt.MQTT_USER', 'test_user')
@patch('src.communication.mqtt.MQTT_PASSWORD', 'test_password')
@patch('src.communication.mqtt.MQTT_HOST', 'mqtt.example.com')
@patch('src.communication.mqtt.MQTT_PORT', '8883')
def test_mqtt_client(mock_client):
    """Test the _mqtt_client method."""
    # Configure the mock
    mock_client_instance = MagicMock()
    mock_client.return_value = mock_client_instance
    
    # Call the method
    client = SendDataMQTT({})._mqtt_client()
    
    # Check that the client was created with the correct transport
    mock_client.assert_called_once_with(transport="websockets")
    
    # Check that TLS was set
    mock_client_instance.tls_set.assert_called_once()
    
    # Check that username and password were set
    mock_client_instance.username_pw_set.assert_called_once_with('test_user', 'test_password')
    
    # Check that connect was called with the correct parameters
    mock_client_instance.connect.assert_called_once_with('mqtt.example.com', 8883, 30)
    
    # Check that the client was returned
    assert client == mock_client_instance


@patch('json.dumps')
def test_publish(mock_dumps, sample_data):
    """Test the _publish method."""
    # Configure the mock
    mock_dumps.return_value = '{"key": "value"}'
    
    # Create a mock client
    mock_client = MagicMock()
    mock_publish_result = MagicMock()
    mock_client.publish.return_value = mock_publish_result
    
    # Call the method
    SendDataMQTT({})._publish(mock_client, 'test/topic', sample_data)
    
    # Check that json.dumps was called with the correct data
    mock_dumps.assert_called_once_with(sample_data)
    
    # Check that client.publish was called with the correct parameters
    mock_client.publish.assert_called_once_with('test/topic', '{"key": "value"}')
    
    # Check that wait_for_publish was called
    mock_publish_result.wait_for_publish.assert_called_once()


@patch.object(SendDataMQTT, '_mqtt_client')
@patch.object(SendDataMQTT, '_publish')
@patch('src.communication.mqtt.MQTT_TOPIC', 'weather/data')
def test_send(mock_publish, mock_mqtt_client, sample_data):
    """Test the send method."""
    # Configure the mocks
    mock_client = MagicMock()
    mock_mqtt_client.return_value = mock_client
    
    # Call the method
    mqtt = SendDataMQTT(sample_data)
    mqtt.send()
    
    # Check that _mqtt_client was called
    mock_mqtt_client.assert_called_once()
    
    # Check that client.loop_start was called
    mock_client.loop_start.assert_called_once()
    
    # Check that _publish was called with the correct parameters
    mock_publish.assert_called_once_with(mock_client, 'weather/data', sample_data)
    
    # Check that client.disconnect was called
    mock_client.disconnect.assert_called_once()