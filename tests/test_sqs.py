"""
Tests for the SQSClient class.
"""
import pytest
from unittest.mock import patch, MagicMock

from src.communication.sqs import SQSClient


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


@patch('src.communication.sqs.boto3.resource')
@patch('src.communication.sqs.SQS_URL', 'https://sqs.example.com')
@patch('src.communication.sqs.SQS_ACCESS_KEY', 'test_access_key')
@patch('src.communication.sqs.SQS_SECRET_KEY', 'test_secret_key')
@patch('src.communication.sqs.SQS_REGION', 'us-west-2')
def test_sqs_client(mock_resource):
    """Test the _sqs_client method."""
    # Configure the mock
    mock_sqs_resource = MagicMock()
    mock_resource.return_value = mock_sqs_resource
    
    # Call the method
    sqs_client = SQSClient({})._sqs_client()
    
    # Check that boto3.resource was called with the correct parameters
    mock_resource.assert_called_once_with(
        'sqs',
        endpoint_url='https://sqs.example.com',
        aws_access_key_id='test_access_key',
        aws_secret_access_key='test_secret_key',
        region_name='us-west-2',
    )
    
    # Check that the SQS resource was returned
    assert sqs_client == mock_sqs_resource


@patch.object(SQSClient, '_sqs_client')
@patch('src.communication.sqs.SQS_QUEUE_NAME', 'test-queue')
def test_get_queue(mock_sqs_client, sample_data):
    """Test the _get_queue method."""
    # Configure the mock
    mock_sqs_resource = MagicMock()
    mock_queue = MagicMock()
    mock_sqs_resource.get_queue_by_name.return_value = mock_queue
    mock_sqs_client.return_value = mock_sqs_resource
    
    # Call the method
    queue = SQSClient(sample_data)._get_queue()
    
    # Check that _sqs_client was called
    mock_sqs_client.assert_called_once()
    
    # Check that get_queue_by_name was called with the correct queue name
    mock_sqs_resource.get_queue_by_name.assert_called_once_with(QueueName='test-queue')
    
    # Check that the queue was returned
    assert queue == mock_queue


@patch('json.dumps')
def test_publish_dict(mock_dumps, sample_data):
    """Test the _publish method with a dictionary payload."""
    # Configure the mock
    mock_dumps.return_value = '{"key": "value"}'
    
    # Create a mock queue
    mock_queue = MagicMock()
    
    # Call the method
    SQSClient({})._publish(mock_queue, sample_data)
    
    # Check that json.dumps was called with the correct data
    mock_dumps.assert_called_once_with(sample_data)
    
    # Check that queue.send_message was called with the correct parameters
    mock_queue.send_message.assert_called_once_with(MessageBody='{"key": "value"}')


def test_publish_string():
    """Test the _publish method with a string payload."""
    # Create a mock queue
    mock_queue = MagicMock()
    
    # Call the method
    SQSClient({})._publish(mock_queue, "test message")
    
    # Check that queue.send_message was called with the correct parameters
    mock_queue.send_message.assert_called_once_with(MessageBody="test message")


@patch.object(SQSClient, '_get_queue')
@patch.object(SQSClient, '_publish')
def test_send(mock_publish, mock_get_queue, sample_data):
    """Test the send method."""
    # Configure the mocks
    mock_queue = MagicMock()
    mock_get_queue.return_value = mock_queue
    
    # Call the method
    sqs = SQSClient(sample_data)
    sqs.send()
    
    # Check that _get_queue was called
    mock_get_queue.assert_called_once()
    
    # Check that _publish was called with the correct parameters
    mock_publish.assert_called_once_with(mock_queue, sample_data)