"""
Tests for the SendDataPostgres class.
"""
import pytest
from unittest.mock import patch, MagicMock, call

from src.communication.postgres import SendDataPostgres


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


@patch('src.communication.postgres.psycopg2.connect')
@patch('src.communication.postgres.POSTGRES_USER', 'test_user')
@patch('src.communication.postgres.POSTGRES_PASSWORD', 'test_password')
@patch('src.communication.postgres.POSTGRES_HOST', 'db.example.com')
@patch('src.communication.postgres.POSTGRES_PORT', '5432')
@patch('src.communication.postgres.POSTGRES_DBNAME', 'test_db')
def test_get_connection(mock_connect):
    """Test the _get_connection method."""
    # Configure the mock
    mock_connection = MagicMock()
    mock_connect.return_value = mock_connection
    
    # Call the method
    connection = SendDataPostgres({})._get_connection()
    
    # Check that psycopg2.connect was called with the correct parameters
    mock_connect.assert_called_once_with(
        user='test_user',
        password='test_password',
        host='db.example.com',
        port='5432',
        dbname='test_db'
    )
    
    # Check that the connection was returned
    assert connection == mock_connection


@patch('src.communication.postgres.POSTGRES_TABLE', 'weather_data')
def test_insert_data(sample_data):
    """Test the _insert_data method."""
    # Create a mock cursor
    mock_cursor = MagicMock()
    
    # Call the method
    postgres = SendDataPostgres(sample_data)
    postgres._insert_data(mock_cursor)
    
    # Check that cursor.execute was called with the correct SQL query and values
    # Note: The order of columns and values in the SQL query is not guaranteed,
    # so we check that the query starts with "INSERT INTO weather_data" and contains
    # the correct number of placeholders
    execute_args = mock_cursor.execute.call_args[0]
    query = execute_args[0]
    values = execute_args[1]
    
    assert query.startswith("INSERT INTO weather_data (")
    assert query.endswith(")")
    assert query.count('%s') == len(sample_data)
    assert len(values) == len(sample_data)
    
    # Check that all values from sample_data are in the values list
    for value in sample_data.values():
        assert value in values


@patch.object(SendDataPostgres, '_get_connection')
@patch.object(SendDataPostgres, '_insert_data')
def test_send_success(mock_insert_data, mock_get_connection, sample_data):
    """Test the send method with a successful connection."""
    # Configure the mocks
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_get_connection.return_value = mock_connection
    
    # Call the method
    postgres = SendDataPostgres(sample_data)
    postgres.send()
    
    # Check that _get_connection was called
    mock_get_connection.assert_called_once()
    
    # Check that connection.cursor was called
    mock_connection.cursor.assert_called_once()
    
    # Check that _insert_data was called with the cursor
    mock_insert_data.assert_called_once_with(mock_cursor)
    
    # Check that connection.commit was called
    mock_connection.commit.assert_called_once()
    
    # Check that cursor.close and connection.close were called
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


@patch.object(SendDataPostgres, '_get_connection')
@patch('builtins.print')
def test_send_exception(mock_print, mock_get_connection, sample_data):
    """Test the send method with an exception."""
    # Configure the mock to raise an exception
    mock_get_connection.side_effect = Exception("Test error")
    
    # Call the method
    postgres = SendDataPostgres(sample_data)
    postgres.send()
    
    # Check that _get_connection was called
    mock_get_connection.assert_called_once()
    
    # Check that the error was printed
    mock_print.assert_called_once_with("Failed to send data to PostgreSQL: Test error")