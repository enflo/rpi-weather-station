import logging
import time
import atexit
from datetime import datetime
from typing import Dict, List, Optional, Union, Any

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import WriteType
from influxdb_client.rest import ApiException
from urllib3.exceptions import NewConnectionError

from src.settings import (
    INFLUXDB_BUCKET,
    INFLUXDB_ORG,
    INFLUXDB_TIMEOUT,
    INFLUXDB_TOKEN,
    INFLUXDB_URL,
    INFLUXDB_VERIFY_SSL,
)

logger = logging.getLogger(__name__)

_influx_wrapper_instance = None

def close_influxdb_client():
    """
    Helper function to close the InfluxDB client instance if it exists.
    """
    global _influx_wrapper_instance
    if _influx_wrapper_instance:
        logger.info("Closing InfluxDB client...")
        _influx_wrapper_instance.close()

class InfluxDBWrapper:
    """
    Wrapper for InfluxDB client with batch processing, retries and error handling.
    Implemented as a Singleton to ensure connection reuse and proper cleanup.
    """

    def __new__(cls):
        global _influx_wrapper_instance
        if _influx_wrapper_instance is None:
            _influx_wrapper_instance = super(InfluxDBWrapper, cls).__new__(cls)
            _influx_wrapper_instance._initialized = False
        return _influx_wrapper_instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        
        self.url = INFLUXDB_URL
        self.token = INFLUXDB_TOKEN
        self.org = INFLUXDB_ORG
        self.bucket = INFLUXDB_BUCKET
        self.timeout = INFLUXDB_TIMEOUT
        self.verify_ssl = INFLUXDB_VERIFY_SSL
        self._client: Optional[InfluxDBClient] = None
        self._write_api = None
        self._query_api = None
        
        self._initialized = True
        atexit.register(self.close)

    def connect(self):
        """
        Establish connection to InfluxDB.
        """
        if self._client:
            return

        try:
            self._client = InfluxDBClient(
                url=self.url,
                token=self.token,
                org=self.org,
                timeout=self.timeout,
                verify_ssl=self.verify_ssl,
            )
            
            # Configure batch writes
            # flush_interval: Default 1000ms
            # batch_size: Default 1000
            # retry_interval: Default 5000ms
            write_options = WriteOptions(
                batch_size=500,
                flush_interval=1000,
                jitter_interval=0,
                retry_interval=5000,
                max_retries=5,
                max_retry_delay=30000,
                exponential_base=2
            )
            
            self._write_api = self._client.write_api(write_options=write_options)
            self._query_api = self._client.query_api()
            
            # Verify connection
            health = self._client.health()
            if health.status != "pass":
                logger.error(f"InfluxDB health check failed: {health.message}")
            else:
                logger.info("Successfully connected to InfluxDB")

        except Exception as e:
            logger.error(f"Failed to connect to InfluxDB: {e}")
            raise

    def close(self):
        """
        Close the connection.
        """
        if self._write_api:
            self._write_api.close()
        if self._client:
            self._client.close()
        self._client = None
        self._write_api = None
        self._query_api = None

    def validate_data(self, data: Optional[Dict[str, Any]]) -> bool:
        """
        Validate data before insertion.
        Ensure it has at least one field and expected structure.
        """
        if not data:
            logger.warning("Empty data received")
            return False

        # Define valid fields and tags (simplified schema validation)
        valid_fields = [
            "temperature_celsius", "temperature_farenheit", "humidity", "pressure", 
            "pm25", "pm10"
        ]
        
        has_field = False
        for key in data:
            if key in valid_fields:
                has_field = True
                # Type check (simple)
                if not isinstance(data[key], (int, float)) and data[key] is not None:
                     logger.warning(f"Invalid type for field {key}: {type(data[key])}")
                     return False
        
        if not has_field:
            logger.warning("Data contains no valid fields for InfluxDB")
            return False

        return True

    def _convert_to_point(self, data: Dict[str, Any]) -> Point:
        """
        Convert dictionary data to InfluxDB Point.
        """
        point = Point("weather_data")
        
        # Add tags
        if "sensor_temp_hum" in data:
            point.tag("sensor_temp_hum", data["sensor_temp_hum"])
        if "sensor_air_quality" in data:
            point.tag("sensor_air_quality", data["sensor_air_quality"])
            
        # Add fields
        fields_added = False
        for key, value in data.items():
            if key in ["temperature_celsius", "temperature_farenheit", "humidity", "pressure", "pm25", "pm10"]:
                if value is not None:
                    point.field(key, float(value))
                    fields_added = True
        
        # Add timestamp (server time by default, but we could add it if provided)
        # point.time(datetime.utcnow(), WritePrecision.NS)
        
        return point if fields_added else None

    def write_data(self, data: Union[Dict[str, Any], List[Dict[str, Any]]]):
        """
        Write data to InfluxDB.
        Accepts a dictionary or a list of dictionaries.
        """
        try:
            self.connect()
            
            points = []
            if isinstance(data, dict):
                if self.validate_data(data):
                    point = self._convert_to_point(data)
                    if point:
                        points.append(point)
            elif isinstance(data, list):
                for item in data:
                    if self.validate_data(item):
                        point = self._convert_to_point(item)
                        if point:
                            points.append(point)
            
            if not points:
                logger.warning("No valid points to write")
                return

            self._write_api.write(bucket=self.bucket, org=self.org, record=points)
            logger.debug(f"Written {len(points)} points to InfluxDB")

        except (ApiException, NewConnectionError) as e:
            logger.error(f"Error writing to InfluxDB: {e}")
            # Retry logic is handled by WriteOptions, but we log the error here.
        except Exception as e:
            logger.error(f"Unexpected error writing to InfluxDB: {e}")

    def read_data(self, query: str):
        """
        Read data from InfluxDB using Flux query.
        """
        try:
            self.connect()
            result = self._query_api.query(org=self.org, query=query)
            return result
        except Exception as e:
            logger.error(f"Error reading from InfluxDB: {e}")
            raise

    def get_latest_measurements(self, minutes: int = 60):
        """
        Get latest measurements for the last N minutes.
        Example of an optimized query.
        """
        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: -{minutes}m)
          |> filter(fn: (r) => r["_measurement"] == "weather_data")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> sort(columns: ["_time"], desc: true)
        '''
        return self.read_data(query)


class SendDataInfluxDB:
    """
    Adapter class to match the interface used in send_data.py
    """
    def __init__(self, data):
        self.data = data
        self.client = InfluxDBWrapper()

    def send(self):
        self.client.write_data(self.data)
        # We don't close the connection here if we want to reuse it, 
        # but the wrapper handles singleton-like behavior if instantiated once.
        # Since send_data instantiates SendDataInfluxDB every time, 
        # connection pooling inside InfluxDBClient handles this.
