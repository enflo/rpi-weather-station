from sds011 import SDS011


class AirQualityMonitor:
    def __init__(self):
        self.sds = SDS011("/dev/ttyUSB0")
        self.sds.set_work_period(work_time=15)

    def get_measurement(self):
        pm25, pm10 = self.get_pm25_pm10()
        return {
            "sensor_air_quality": "sds011",
            "pm25": pm25,
            "pm10": pm10,
        }

    def get_pm25_pm10(self):
        pm25, pm10 = self.sds.query()
        return pm25, pm10
