import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Import the send_data function
from src.communication.send_data import send_data

# Test data
test_data = {
    "temperature_celsius": 25.5,
    "humidity": 60.2,
    "pressure": 1013.25,
    "timestamp": "2023-06-15T12:34:56Z"
}

# Send the test data
print("Sending test data to PostgreSQL...")
send_data(test_data)
print("Test completed.")