import pytest
import requests
from unittest.mock import patch, Mock
from src.communication.sensor_community import SendDataSensorCommunity
from src.settings import SENSOR_COMMUNITY_SENSOR_SDS011_ID, SENSOR_COMMUNITY_SENSOR_BME280_ID

@pytest.fixture
def sample_data():
    return {
        "pm10": 12.5,
        "pm25": 5.0,
        "temperature_celsius": 22.0,
        "humidity": 45.0,
        "pressure": 1013.0,
    }

@patch('src.communication.sensor_community.requests.post')
def test_send_sensor_community_success(mock_post, sample_data):
    # Setup mock
    mock_response = Mock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Initialize and send
    sender = SendDataSensorCommunity(sample_data)
    sender.send()

    # Verify calls
    assert mock_post.call_count == 2

    # Verify PM call
    expected_headers_pm = {
        "X-PIN": "1",
        "X-Sensor": SENSOR_COMMUNITY_SENSOR_SDS011_ID,
        "Content-Type": "application/json"
    }
    expected_json_pm = {
        "software_version": "rpi-weather-station-1.0",
        "sensordatavalues": [
            {"value_type": "P1", "value": 12.5},
            {"value_type": "P2", "value": 5.0},
        ]
    }
    
    # PM is sent first in the code.
    call_args_list = mock_post.call_args_list
    
    # Check first call (PM)
    args, kwargs = call_args_list[0]
    assert args[0] == "https://api.sensor.community/v1/push-sensor-data/"
    assert kwargs['headers'] == expected_headers_pm
    assert kwargs['json'] == expected_json_pm
    assert kwargs['timeout'] == 10

    # Verify BME call
    expected_headers_bme = {
        "X-PIN": "11",
        "X-Sensor": SENSOR_COMMUNITY_SENSOR_BME280_ID,
        "Content-Type": "application/json"
    }
    expected_json_bme = {
        "software_version": "rpi-weather-station-1.0",
        "sensordatavalues": [
            {"value_type": "temperature", "value": 22.0},
            {"value_type": "humidity", "value": 45.0},
            {"value_type": "pressure", "value": 1013.0},
        ]
    }
    
    # Check second call (BME)
    args, kwargs = call_args_list[1]
    assert args[0] == "https://api.sensor.community/v1/push-sensor-data/"
    assert kwargs['headers'] == expected_headers_bme
    assert kwargs['json'] == expected_json_bme
    assert kwargs['timeout'] == 10

@patch('src.communication.sensor_community.requests.post')
def test_send_sensor_community_failure(mock_post, sample_data):
    # Setup mock to raise exception
    mock_post.side_effect = requests.exceptions.RequestException("Connection error")
    
    # Initialize and send
    sender = SendDataSensorCommunity(sample_data)
    # Should not raise exception as it is caught and logged
    sender.send()
    
    assert mock_post.call_count == 2
