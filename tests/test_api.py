"""
Tests for the SendDataAPI class.
"""
from unittest.mock import patch

import pytest
from src.communication.api import SendDataAPI


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


@patch('src.communication.api.API_HOST', 'https://example.com')
@patch('src.communication.api.API_URL_TOKEN', '/api/weather')
def test_get_url():
    """Test the _get_url method."""
    api = SendDataAPI({})
    url = api._get_url()
    assert url == 'https://example.com/api/weather'


@patch('src.communication.api.API_HEADER_TOKEN', None)
def test_get_headers_no_token():
    """Test the _get_headers method with no token."""
    api = SendDataAPI({})
    headers = api._get_headers()
    assert headers == {'Content-Type': 'application/json'}


@patch('src.communication.api.API_HEADER_TOKEN', {'Authorization': 'Bearer token123'})
def test_get_headers_with_token():
    """Test the _get_headers method with a token."""
    api = SendDataAPI({})
    headers = api._get_headers()
    assert headers == {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer token123'
    }


@patch('src.communication.api.requests.request')
@patch.object(SendDataAPI, '_get_url', return_value='https://example.com/api/weather')
@patch.object(SendDataAPI, '_get_headers', return_value={'Content-Type': 'application/json'})
@patch('src.communication.api.API_METHOD', 'POST')
def test_make_request(mock_get_headers, mock_get_url, mock_request, sample_data):
    """Test the _make_request method."""
    api = SendDataAPI(sample_data)
    api._make_request()
    
    # Check that requests.request was called with the correct arguments
    mock_request.assert_called_once_with(
        method='POST',
        url='https://example.com/api/weather',
        headers={'Content-Type': 'application/json'},
        json=sample_data
    )


@patch.object(SendDataAPI, '_make_request')
def test_send(mock_make_request, sample_data):
    """Test the send method."""
    api = SendDataAPI(sample_data)
    api.send()
    
    # Check that _make_request was called
    mock_make_request.assert_called_once()