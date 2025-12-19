import logging
import time

from src.communication.send_data import send_data
from src.sensors.bme280sensor import BME280Sensor
from src.sensors.sds011sensor import SDS011Sensor
from src.settings import LOOP_TIME
from src.hardware import get_rpi_model

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_weather(sds_sensor, bme_sensor) -> dict:
    weather = {
        "timestamp": time.time(),
    }
    
    try:
        if sds_sensor:
            air_quality = sds_sensor.get_measurement()
            weather.update(air_quality)
    except Exception as e:
        logger.error(f"Error reading SDS011 sensor: {e}")

    try:
        if bme_sensor:
            temperature_humidity_pressure = bme_sensor.get_measurement()
            weather.update(temperature_humidity_pressure)
    except Exception as e:
        logger.error(f"Error reading BME280 sensor: {e}")

    return weather


if __name__ == "__main__":
    logger.info("Starting Weather Station")
    
    # Detect and log hardware info
    rpi_info = get_rpi_model()
    logger.info(f"Detected Hardware: {rpi_info['model']} (Family: {rpi_info['family']})")

    # Initialize sensors
    try:
        sds_sensor = SDS011Sensor()
    except Exception as e:
        logger.error(f"Failed to initialize SDS011Sensor: {e}")
        sds_sensor = None

    try:
        bme_sensor = BME280Sensor()
    except Exception as e:
        logger.error(f"Failed to initialize BME280Sensor: {e}")
        bme_sensor = None

    while True:
        try:
            result = get_weather(sds_sensor, bme_sensor)
            send_data(result)
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            
        time.sleep((LOOP_TIME * 60 * 60) / 4)  # 15 minutes
